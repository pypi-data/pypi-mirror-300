from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generator, Tuple

import numpy as np
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models import QuerySet
from shapely import wkb
from shapely.geometry import LineString, MultiPoint, MultiPolygon, Point
from sklearn.cluster import DBSCAN

from .values import ClusteringOutput

if TYPE_CHECKING:
    from .values import BaseViewPort
    from .views import MapFeaturesBaseView


class BaseClustering:
    def find_clusters(
        self, view: MapFeaturesBaseView, viewport: BaseViewPort, items
    ) -> Generator[ClusteringOutput, None, None]:
        raise NotImplementedError()


class DatabaseClustering(BaseClustering):
    DEFAULT_GEOMETRY_FIELD = "position"
    DEFAULT_NUM_CLUSTERS = 1
    DEFAULT_RADIUS = 18
    DEFAULT_MIN_CLUSTER_SIZE = 3

    @dataclass
    class Cluster:
        count: int
        centroid: Point
        shape: MultiPolygon

    def get_clustering_config(self, view, viewport):  # pylint: disable=unused-argument
        return {
            "include_orphans": True,
            "geometry_field": self.DEFAULT_GEOMETRY_FIELD,
            "min_cluster_size": self.DEFAULT_MIN_CLUSTER_SIZE,
            "num_clusters": self.DEFAULT_NUM_CLUSTERS,
            "radius": self.DEFAULT_RADIUS,
            "db_alias": None,
        }

    def get_clustering_function_sql_with_params(
        self, config
    ) -> Tuple[str, Tuple[Any, ...]]:
        geometry_field = config["geometry_field"]
        num_clusters = config["num_clusters"]
        radius = config["radius"]
        sql = f"ST_ClusterKMeans({geometry_field}::geometry, %s, %s)"
        params = (num_clusters, radius)
        return sql, params

    def find_clusters(  # pylint: disable=too-many-locals
        self,
        view: MapFeaturesBaseView,
        viewport: BaseViewPort,
        items,
    ) -> Generator[ClusteringOutput, None, None]:
        if isinstance(items, (tuple, list)) and not items:
            return

        if not isinstance(items, QuerySet):
            raise ValueError("Database clustering requires QuerySet on input")

        config = self.get_clustering_config(view, viewport)

        include_orphans = config["include_orphans"]
        geometry_field = config["geometry_field"]
        min_cluster_size = config["min_cluster_size"]
        db_alias = config["db_alias"] or items.db or DEFAULT_DB_ALIAS

        viewport_wkb = None
        if viewport:
            viewport_polygon = viewport.to_polygon()
            viewport_wkb = wkb.dumps(viewport_polygon, include_srid=True)

        sql, sql_params = items.query.sql_with_params()
        (
            clustering_sql,
            clustering_sql_params,
        ) = self.get_clustering_function_sql_with_params(config)

        if include_orphans:
            items_outside_clusters_raw_sql = f"""
                WITH clustered_items AS (
                    SELECT *, {clustering_sql} OVER () as cluster_label FROM ({sql}) AS orm_sq
                )
                SELECT * FROM (
                    SELECT *
                    FROM clustered_items
                    WHERE cluster_label NOT IN (
                        SELECT cluster_label
                        FROM clustered_items
                        WHERE cluster_label IS NOT NULL
                        GROUP BY cluster_label
                        HAVING COUNT(*) >= %s
                )) AS sq
                WHERE (%s IS NULL OR ST_Intersects({geometry_field}::geometry, %s::geometry));
            """
            items_outside_clusters_raw_sql_params = (
                clustering_sql_params
                + sql_params
                + (
                    min_cluster_size,
                    viewport_wkb,
                    viewport_wkb,
                )
            )
            items_outside_clusters = items.model.objects.using(db_alias).raw(
                items_outside_clusters_raw_sql,
                items_outside_clusters_raw_sql_params,
            )

            for item in items_outside_clusters.iterator():
                yield ClusteringOutput(
                    is_cluster=False,
                    item=item,
                )

        clusters_raw_sql = f"""
            WITH clustered_items AS (
                SELECT *, {clustering_sql} OVER () as cluster_label FROM ({sql}) AS orm_sq
            )
            SELECT
                COUNT(*) as cluster_item_count,
                ST_Collect({geometry_field}::geometry) as cluster_geometry
            FROM clustered_items
            WHERE cluster_label IS NOT NULL
            GROUP BY cluster_label
            HAVING COUNT(*) >= %s
                AND (%s IS NULL OR ST_Intersects(ST_Collect({geometry_field}::geometry)::geometry, %s::geometry));
        """

        clusters_raw_sql_params = (
            clustering_sql_params
            + sql_params
            + (
                min_cluster_size,
                viewport_wkb,
                viewport_wkb,
            )
        )

        connection = connections[db_alias]
        with connection.cursor() as cursor:
            cursor.execute(clusters_raw_sql, clusters_raw_sql_params)
            while row := cursor.fetchone():
                cluster_shape = wkb.loads(row[1]).convex_hull
                if isinstance(cluster_shape, (LineString, Point)):
                    cluster_shape = cluster_shape.buffer(0.1).convex_hull
                shape = MultiPolygon([cluster_shape])

                yield ClusteringOutput(
                    is_cluster=True,
                    item=self.Cluster(
                        count=row[0],
                        shape=shape,
                        centroid=shape.centroid,
                    ),
                )

        for cluster in []:
            yield ClusteringOutput(
                is_cluster=True,
                item=cluster,
            )


class BasicClustering:
    @dataclass
    class Cluster:
        centroid: Point
        shape: MultiPolygon
        items: list

    def get_clustering_config(self, view, viewport):  # pylint: disable=unused-argument
        def default_item_to_point(item):
            try:
                geom = view.serializer.get_geometry(item)
                return geom.centroid
            except (ValueError, AttributeError):
                return None

        return {
            "include_orphans": False,
            "item_to_point": default_item_to_point,
            "eps": 3,
            "p": 2,
            "min_samples": 5,
        }

    def find_clusters(  # pylint: disable=too-many-locals
        self,
        view: MapFeaturesBaseView,
        viewport: BaseViewPort,
        items,
    ) -> Generator[ClusteringOutput, None, None]:
        config = self.get_clustering_config(view, viewport)

        include_orphans = config["include_orphans"]
        item_to_point = config["item_to_point"]

        items_to_cluster = []
        points_to_cluster = []
        for item in items:
            point = item_to_point(item)

            if point:
                items_to_cluster.append(item)
                points_to_cluster.append(point)
            else:
                if include_orphans:
                    yield ClusteringOutput(
                        is_cluster=False,
                        item=item,
                    )

        if not points_to_cluster:
            return

        dataset = np.array(points_to_cluster)

        clustering = DBSCAN(
            eps=config["eps"],
            p=config["p"],
            min_samples=config["min_samples"],
        ).fit(dataset)

        labels = clustering.labels_

        clusters = {}
        for label, item, point in zip(labels, items_to_cluster, points_to_cluster):
            if label < 0:
                if include_orphans:
                    yield ClusteringOutput(
                        is_cluster=False,
                        item=item,
                    )
            else:
                if label not in clusters:
                    clusters[label] = {"points": [], "items": []}
                clusters[label]["points"].append(point)
                clusters[label]["items"].append(item)

        for cluster in clusters.values():
            multipoint = MultiPoint(cluster["points"])
            multipolygon = MultiPolygon([multipoint.convex_hull])
            cluster_obj = self.Cluster(
                centroid=multipolygon.centroid,
                shape=multipolygon,
                items=cluster["items"],
            )
            yield ClusteringOutput(
                is_cluster=True,
                item=cluster_obj,
            )

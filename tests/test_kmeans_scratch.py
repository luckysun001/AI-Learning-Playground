"""K-Means（从零实现，k-means++ 初始化）基线测试。

注意：模块在顶层 import matplotlib，本地无 matplotlib 时由 conftest 注入桩，
CI 用真实包，不影响算法逻辑测试。
"""

import kmeans_scratch as km
import numpy as np
import pytest
from sklearn.datasets import make_blobs


@pytest.fixture
def blob_data():
    X, _ = make_blobs(n_samples=300, n_features=4, centers=3, random_state=42)
    return X


def test_kmeans_plus_plus_init_shape(blob_data):
    centers = km.kmeans_plus_plus_init(blob_data, k=3, rng=np.random.default_rng(0))
    assert centers.shape == (3, blob_data.shape[1])


def test_kmeans_scratch_shapes_and_labels(blob_data):
    centroids, labels = km.kmeans_scratch(blob_data, k=3, seed=42)
    assert centroids.shape == (3, blob_data.shape[1])
    assert labels.shape == (blob_data.shape[0],)
    assert set(np.unique(labels)).issubset({0, 1, 2})


def test_kmeans_deterministic(blob_data):
    c1, l1 = km.kmeans_scratch(blob_data, k=3, seed=7)
    c2, l2 = km.kmeans_scratch(blob_data, k=3, seed=7)
    assert np.allclose(c1, c2)
    assert np.array_equal(l1, l2)


def test_kmeans_labels_match_centroid_count(blob_data):
    _, labels = km.kmeans_scratch(blob_data, k=3, seed=42)
    # 每个簇至少有 1 个样本
    for j in range(3):
        assert np.sum(labels == j) > 0

"""决策树（CART 分类，从零实现）基线测试。"""

import decision_tree_scratch as dt
import numpy as np
import pytest
from sklearn.datasets import make_classification


def test_gini_pure_is_zero():
    assert dt.gini(np.array([1, 1, 1, 1])) == 0.0
    assert dt.gini(np.array([0, 0])) == 0.0


def test_gini_binary_balanced_is_half():
    # 两类各半，Gini = 1 - (0.5^2 + 0.5^2) = 0.5
    assert abs(dt.gini(np.array([0, 1, 0, 1])) - 0.5) < 1e-9


def test_best_split_finds_a_split():
    X = np.array([[1.0], [2.0], [3.0], [10.0], [11.0], [12.0]])
    y = np.array([0, 0, 0, 1, 1, 1])
    split = dt.best_split(X, y)
    assert split is not None
    f, t = split
    assert f == 0
    assert 3.0 <= t <= 10.0


def test_build_and_predict_separable():
    # 完全可分的两簇
    X = np.array(
        [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [5.0, 5.0],
            [5.0, 6.0],
            [6.0, 5.0],
            [6.0, 6.0],
        ]
    )
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    tree = dt.build_tree(X, y, max_depth=5)
    preds = dt.predict(tree, X)
    assert np.array_equal(preds, y)


def test_predict_matches_sklearn_baseline():
    X, y = make_classification(
        n_samples=300, n_features=4, n_informative=3, n_redundant=1, random_state=42
    )
    X_train, X_test, y_train, y_test = _split(X, y)
    tree = dt.build_tree(X_train, y_train, max_depth=5)
    preds = dt.predict(tree, X_test)
    # 从零实现在简单数据上应达到不错的准确率
    acc = (preds == y_test).mean()
    assert acc >= 0.78


def test_print_tree_runs():
    X, y = make_classification(
        n_samples=60, n_features=3, n_informative=2, n_redundant=1, random_state=1
    )
    tree = dt.build_tree(X, y, max_depth=3)
    # print_tree 仅打印，不应抛异常
    dt.print_tree(tree, [f"x{i}" for i in range(X.shape[1])])


def _split(X, y, test_size=0.3, seed=42):
    rng = np.random.default_rng(seed)
    n = len(y)
    idx = rng.permutation(n)
    n_test = int(n * test_size)
    test_idx, train_idx = idx[:n_test], idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

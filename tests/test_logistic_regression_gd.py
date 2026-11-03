"""逻辑回归（从零梯度下降）基线测试。"""

import logistic_regression_gd
import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@pytest.fixture
def clf_data():
    X, y = make_classification(
        n_samples=2000, n_features=10, n_informative=5, n_redundant=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    Xtr = np.c_[np.ones(X_train.shape[0]), scaler.fit_transform(X_train)]
    Xte = np.c_[np.ones(X_test.shape[0]), scaler.transform(X_test)]
    return Xtr, Xte, y_train, y_test


def test_sigmoid_properties():
    z = np.array([-1000.0, -1.0, 0.0, 1.0, 1000.0])
    s = logistic_regression_gd.sigmoid(z)
    assert s[0] < 1e-6  # 大负数 -> 趋近 0
    assert abs(s[2] - 0.5) < 1e-9  # 0 -> 0.5
    assert s[-1] > 1 - 1e-6  # 大正数 -> 趋近 1
    assert np.all(np.diff(s) > 0)  # 单调递增


def test_theta_shape_and_predict_labels(clf_data):
    Xtr, Xte, y_train, _ = clf_data
    theta = logistic_regression_gd.logistic_regression_gd(
        Xtr, y_train, lr=0.1, epochs=3000
    )
    assert theta.shape == (Xtr.shape[1],)
    preds = logistic_regression_gd.predict(Xte, theta)
    assert set(np.unique(preds)).issubset({0, 1})
    assert preds.dtype.kind in ("i", "u")


def test_accuracy_reasonable(clf_data):
    Xtr, Xte, y_train, y_test = clf_data
    theta = logistic_regression_gd.logistic_regression_gd(
        Xtr, y_train, lr=0.1, epochs=4000
    )
    y_pred = logistic_regression_gd.predict(Xte, theta)
    # 合成数据简单可分，从零实现应达到基本准确率
    assert accuracy_score(y_test, y_pred) > 0.7


def test_threshold_argument(clf_data):
    Xtr, Xte, y_train, _ = clf_data
    theta = logistic_regression_gd.logistic_regression_gd(
        Xtr, y_train, lr=0.1, epochs=2000
    )
    # 阈值设极高 -> 全部判为 0（sigmoid 恒 < 0.999）；阈值设 0 -> 全部判为 1（sigmoid 恒 >= 0）
    assert np.all(logistic_regression_gd.predict(Xte, theta, threshold=0.999) == 0)
    assert np.all(logistic_regression_gd.predict(Xte, theta, threshold=0.0) == 1)

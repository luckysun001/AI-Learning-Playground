"""线性回归（从零梯度下降）基线测试。"""

import numpy as np
import pytest
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from linear_regression_gd import linear_regression_gd as linreg


@pytest.fixture
def regression_data():
    X, y = make_regression(
        n_samples=2000, n_features=5, noise=15.0, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    Xtr = np.c_[np.ones(X_train.shape[0]), scaler.fit_transform(X_train)]
    Xte = np.c_[np.ones(X_test.shape[0]), scaler.transform(X_test)]
    return Xtr, Xte, y_train, y_test


def test_theta_shape_and_zero_init(regression_data):
    Xtr, _, y_train, _ = regression_data
    theta, losses = linreg(Xtr, y_train, lr=0.1, epochs=10)
    assert theta.shape == (Xtr.shape[1],)
    assert len(losses) == 10


def test_losses_decrease(regression_data):
    Xtr, _, y_train, _ = regression_data
    _, losses = linreg(Xtr, y_train, lr=0.1, epochs=800)
    assert losses[-1] < losses[0]
    # 单调递减（允许浮点噪声）
    diffs = np.diff(losses)
    assert np.all(diffs < 1e-6) or losses[-1] < losses[0] * 0.5


def test_scratch_matches_sklearn(regression_data):
    Xtr, Xte, y_train, y_test = regression_data
    theta, _ = linreg(Xtr, y_train, lr=0.1, epochs=3000)
    y_pred_scratch = Xte @ theta
    r2_scratch = r2_score(y_test, y_pred_scratch)

    # sklearn 闭式解：用同样的缩放特征（不加偏置列，让它自己处理截距）
    Xtrain_scaled = Xtr[:, 1:]
    Xtest_scaled = Xte[:, 1:]
    lr = LinearRegression().fit(Xtrain_scaled, y_train)
    r2_sk = r2_score(y_test, lr.predict(Xtest_scaled))

    # 两者都应拟合良好，且 R² 接近
    assert r2_scratch > 0.8
    assert r2_sk > 0.8
    assert abs(r2_scratch - r2_sk) < 0.15


def test_deterministic(regression_data):
    Xtr, _, y_train, _ = regression_data
    t1, _ = linreg(Xtr, y_train, lr=0.1, epochs=300)
    t2, _ = linreg(Xtr, y_train, lr=0.1, epochs=300)
    assert np.allclose(t1, t2)

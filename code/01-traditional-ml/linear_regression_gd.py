"""
线性回归：从零实现（梯度下降）+ 与 sklearn 对比
------------------------------------------------
背景：预测连续数值（回归）。本脚本用梯度下降从零训一个线性回归，
      再与 sklearn 的闭式解 LinearRegression 对比 MSE / R²。

运行：python linear_regression_gd.py
依赖：numpy, scikit-learn, matplotlib（仅需前两者即可跑通核心逻辑）

预期输出：两行指标接近，说明从零实现正确。
"""
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def linear_regression_gd(X, y, lr=0.01, epochs=1000, verbose=False):
    """梯度下降法训练线性回归。

    X: 形状 (m, n)，已含偏置列（全 1）
    y: 形状 (m,)
    返回 (theta, losses)
    """
    m, n = X.shape
    theta = np.zeros(n)
    losses = []
    for epoch in range(epochs):
        y_pred = X @ theta
        error = y_pred - y
        grad = (X.T @ error) / m          # 与文档伪代码一致
        theta = theta - lr * grad
        losses.append(mean_squared_error(y, y_pred))
        if verbose and epoch % 200 == 0:
            print(f"  epoch {epoch:4d}  loss={losses[-1]:.4f}")
    return theta, losses


def main():
    # 合成回归数据（无需外部下载）
    X, y = make_regression(
        n_samples=2000, n_features=5, noise=15.0, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 特征缩放（梯度下降对量纲敏感，必须做）
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # 手动加偏置列
    Xtr = np.c_[np.ones(X_train_s.shape[0]), X_train_s]
    Xte = np.c_[np.ones(X_test_s.shape[0]), X_test_s]

    # 从零训练
    theta, _ = linear_regression_gd(Xtr, y_train, lr=0.1, epochs=3000)
    y_pred_scratch = Xte @ theta

    # sklearn 闭式解（注意：它内部自己处理截距，不需我们加偏置列）
    lr = LinearRegression().fit(X_train, y_train)
    y_pred_sk = lr.predict(X_test)

    print("【线性回归 · 梯度下降 vs sklearn 闭式解】")
    print("  从零实现  MSE=%.4f  R²=%.4f" % (
        mean_squared_error(y_test, y_pred_scratch),
        r2_score(y_test, y_pred_scratch)))
    print("  sklearn   MSE=%.4f  R²=%.4f" % (
        mean_squared_error(y_test, y_pred_sk),
        r2_score(y_test, y_pred_sk)))
    print("  参数一致度（与 sklearn.coef_ 接近）:",
          np.allclose(theta[1:], lr.coef_, atol=2.0))


if __name__ == "__main__":
    main()

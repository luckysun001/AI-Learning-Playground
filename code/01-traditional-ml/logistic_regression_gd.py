"""
逻辑回归：从零实现（梯度下降）+ 与 sklearn 对比
------------------------------------------------
背景：二分类。对线性回归输出套 Sigmoid 得到概率，用交叉熵作损失。

运行：python logistic_regression_gd.py
依赖：numpy, scikit-learn
"""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def sigmoid(z):
    # 数值稳定版
    return np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))


def logistic_regression_gd(X, y, lr=0.1, epochs=3000):
    m, n = X.shape
    theta = np.zeros(n)
    for _ in range(epochs):
        z = X @ theta
        y_pred = sigmoid(z)
        error = y_pred - y
        grad = (X.T @ error) / m           # 与线性回归同形
        theta = theta - lr * grad
    return theta


def predict(X, theta, threshold=0.5):
    return (sigmoid(X @ theta) >= threshold).astype(int)


def main():
    X, y = make_classification(
        n_samples=2000, n_features=10, n_informative=5,
        n_redundant=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    Xtr = np.c_[np.ones(X_train_s.shape[0]), X_train_s]
    Xte = np.c_[np.ones(X_test_s.shape[0]), X_test_s]

    theta = logistic_regression_gd(Xtr, y_train, lr=0.1, epochs=5000)
    y_pred_scratch = predict(Xte, theta)

    clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    y_pred_sk = clf.predict(X_test)

    print("【逻辑回归 · 梯度下降 vs sklearn】")
    print("  从零实现  Accuracy=%.4f" % accuracy_score(y_test, y_pred_scratch))
    print("  sklearn   Accuracy=%.4f" % accuracy_score(y_test, y_pred_sk))
    print("  概率头几个（从零实现）:", np.round(sigmoid(Xte @ theta)[:5], 3))


if __name__ == "__main__":
    main()

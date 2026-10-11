"""
案例1：房价回归对比（多种算法同台）
-----------------------------------
背景：回归任务，用合成房价数据对比 5 种算法，体会模型差异。
     对应文档：docs/traditional-ml/linear_regression.md 等。

运行：python case1_regression_comparison.py
依赖：numpy, scikit-learn
"""

import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def main():
    # 合成「房价」数据：10 个特征，含非线性噪声
    X, y = make_regression(
        n_samples=3000, n_features=10, n_informative=6, noise=20.0, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "线性回归": make_pipeline(StandardScaler(), LinearRegression()),
        "决策树": DecisionTreeRegressor(max_depth=8, random_state=42),
        "随机森林": RandomForestRegressor(n_estimators=200, random_state=42),
        "KNN": make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5)),
        "SVR(RBF)": make_pipeline(StandardScaler(), SVR(C=10.0, gamma=0.1)),
    }

    print("【案例1 · 房价回归 · 多模型对比】")
    print(f"{'模型':<12}{'MSE':>12}{'R²':>10}")
    print("-" * 34)
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"{name:<12}{mse:>12.2f}{r2:>10.4f}")

    print("\n观察：树模型/集成通常在这类含非线性数据上优于纯线性模型；")
    print("      SVR 对超参较敏感，需调 C 与 gamma。")


if __name__ == "__main__":
    main()

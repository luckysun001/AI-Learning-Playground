"""
案例2：客户流失预测（二分类 + 特征工程 + 模型调优）
--------------------------------------------------
背景：预测用户是否会流失。演示完整流程：缺失值处理 → 类别编码 →
      标准化 → Pipeline → 多模型对比 → 评估指标。
      对应文档：docs/traditional-ml/feature_engineering.md, model_evaluation.md。

运行：python case2_churn_prediction.py
依赖：numpy, pandas, scikit-learn
"""
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)


def make_churn_dataframe(n=2000, seed=42):
    """构造一个带缺失值、含数值与类别特征的流失数据集（纯合成）。"""
    X, y = make_classification(
        n_samples=n, n_features=6, n_informative=4,
        n_redundant=1, weights=[0.8], random_state=seed
    )
    df = pd.DataFrame(X, columns=[f"num{i}" for i in range(6)])
    # 注入类别特征
    df["plan"] = np.random.choice(["free", "basic", "pro"], n)
    df["region"] = np.random.choice(["north", "south", "east", "west"], n)
    df["churn"] = y
    # 注入缺失值
    mask = np.random.RandomState(seed).rand(*df[["num0", "num1"]].shape) < 0.1
    df.loc[mask[:, 0], "num0"] = np.nan
    df.loc[mask[:, 1], "num1"] = np.nan
    return df


def main():
    df = make_churn_dataframe()
    X = df.drop(columns=["churn"])
    y = df["churn"]

    num_cols = ["num0", "num1", "num2", "num3", "num4", "num5"]
    cat_cols = ["plan", "region"]

    pre = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), num_cols),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), cat_cols),
    ])

    models = {
        "逻辑回归": Pipeline([("pre", pre),
                              ("clf", LogisticRegression(max_iter=1000))]),
        "随机森林": Pipeline([("pre", pre),
                              ("clf", RandomForestClassifier(n_estimators=200,
                                                             random_state=42))]),
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("【案例2 · 客户流失预测】")
    print(f"{'模型':<10}{'Acc':>7}{'Prec':>7}{'Rec':>7}{'F1':>7}{'AUC':>8}")
    print("-" * 46)
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        print(f"{name:<10}"
              f"{accuracy_score(y_test, y_pred):>7.3f}"
              f"{precision_score(y_test, y_pred):>7.3f}"
              f"{recall_score(y_test, y_pred):>7.3f}"
              f"{f1_score(y_test, y_pred):>7.3f}"
              f"{roc_auc_score(y_test, y_prob):>8.3f}")
        # 5 折交叉验证（AUC）看稳定性
        cv = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
        print(f"   5-fold CV AUC: {cv.mean():.3f} (±{cv.std():.3f})")


if __name__ == "__main__":
    main()

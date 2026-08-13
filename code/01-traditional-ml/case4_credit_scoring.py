"""
案例4：信贷风控评分卡（逻辑回归 + WOE 编码思路）
------------------------------------------------
背景：信贷场景中，评分卡要求特征对「违约/不违约」有单调、可解释的关系。
      WOE（Weight of Evidence）把分箱后的类别映射为对好坏比的对数变换，
      再喂给逻辑回归得到可解释的线性打分。对应文档：feature_engineering.md。

运行：python case4_credit_scoring.py
依赖：numpy, pandas, scikit-learn
说明：本脚本用合成数据演示 WOE 计算与逻辑回归打分全流程。
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def compute_woe_iv(series, target, bins=5):
    """对一个数值特征做等频分箱，计算每箱的 WOE 与该特征 IV。"""
    bucket = pd.qcut(series, bins, duplicates="drop")
    df = pd.DataFrame({"x": bucket, "y": target})
    total_good = (target == 0).sum()
    total_bad = (target == 1).sum()
    woe_map = {}
    iv = 0.0
    for b in df["x"].cat.categories:
        sub = df[df["x"] == b]["y"]
        bad = (sub == 1).sum()
        good = (sub == 0).sum()
        bad_rate = (bad + 1e-6) / (total_bad + 1e-6)
        good_rate = (good + 1e-6) / (total_good + 1e-6)
        woe = np.log(good_rate / bad_rate)
        woe_map[b] = woe
        iv += (good_rate - bad_rate) * woe
    return woe_map, iv


def main():
    rng = np.random.default_rng(42)
    n = 3000
    # 合成：收入越高越不易违约；负债越高越易违约（uniform 便于 WOE 分箱）
    income = rng.uniform(10, 120, n)
    debt = rng.uniform(0, 100, n)
    # 线性 logit：收入正向、负债负向，叠加少量噪声
    logit = (income - 50) * 0.05 - (debt - 30) * 0.08 + rng.normal(0, 1.0, n)
    y = (logit > 0).astype(int)

    df = pd.DataFrame({"income": income, "debt": debt, "default": y})

    # 对每个特征做 WOE 变换
    woe_maps = {}
    ivs = {}
    for col in ["income", "debt"]:
        woe_map, iv = compute_woe_iv(df[col], df["default"], bins=5)
        woe_maps[col] = woe_map
        ivs[col] = iv
        df[col + "_woe"] = df[col].apply(
            lambda v: next((woe_maps[col][b] for b in woe_maps[col]
                            if v in b), 0.0))

    print("【案例4 · 信贷评分卡（WOE + 逻辑回归）】")
    for col in ["income", "debt"]:
        print(f"  特征 {col:<8} IV={ivs[col]:.3f}（>0.1 有区分力，>0.3 强）")

    X = df[["income_woe", "debt_woe"]].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf = LogisticRegression().fit(X_train, y_train)
    auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
    print(f"  逻辑回归 AUC={auc:.3f}")
    coefs = dict(zip(["income_woe", "debt_woe"], np.round(clf.coef_[0], 3)))
    print("  WOE 系数（正=降低违约概率）：", coefs)


if __name__ == "__main__":
    main()

"""案例脚本单元测试 + main() 端到端冒烟。

- case2：make_churn_dataframe（缺失值/类别特征/标签）
- case4：compute_woe_iv（WOE 符号、IV 量级）
- 各 case 的 main() 都能无异常跑通（案例3 的 matplotlib 由 conftest 桩接管）
"""

import case1_regression_comparison
import case2_churn_prediction
import case3_clustering_pca
import case4_credit_scoring
import numpy as np
import pandas as pd
import pytest

# ---------- case2：客户流失数据构造 ----------


def test_make_churn_dataframe_basic():
    df = case2_churn_prediction.make_churn_dataframe(n=500, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 500
    assert "churn" in df.columns
    assert {"plan", "region"}.issubset(df.columns)
    # 注入了缺失值
    assert df[["num0", "num1"]].isna().sum().sum() > 0
    # 标签为 0/1
    assert set(np.unique(df["churn"])).issubset({0, 1})


def test_make_churn_dataframe_deterministic():
    a = case2_churn_prediction.make_churn_dataframe(n=300, seed=99)
    b = case2_churn_prediction.make_churn_dataframe(n=300, seed=99)
    pd.testing.assert_frame_equal(a, b)


# ---------- case4：WOE / IV ----------


def test_compute_woe_iv_returns():
    rng = np.random.default_rng(42)
    n = 2000
    x = rng.uniform(10, 120, n)
    # 收入越高，违约概率越低
    logit = (x - 50) * 0.05 + rng.normal(0, 1, n)
    y = (logit > 0).astype(int)
    woe_map, iv = case4_credit_scoring.compute_woe_iv(
        pd.Series(x), pd.Series(y), bins=5
    )
    assert isinstance(woe_map, dict)
    assert len(woe_map) >= 1
    assert iv >= 0.0
    assert np.isfinite(iv)


def test_woe_monotonic_with_target():
    # 构造：特征 x 与 y 强正相关，低 x 多为坏样本 -> 低分箱 WOE 应为负
    rng = np.random.default_rng(1)
    n = 3000
    x = rng.uniform(0, 100, n)
    y = (x + rng.normal(0, 10, n) > 50).astype(int)
    woe_map, iv = case4_credit_scoring.compute_woe_iv(
        pd.Series(x), pd.Series(y), bins=5
    )
    # x 越高 -> y 越可能为 1（坏样本）；故低分箱好样本多 -> WOE 为正，
    # 高分箱坏样本多 -> WOE 为负。即最低分箱 WOE 应大于最高分箱 WOE（单调）
    keys = list(woe_map.keys())
    assert woe_map[keys[0]] > woe_map[keys[-1]]


# ---------- 各 case main() 端到端冒烟 ----------


def test_case1_main_runs(capsys):
    case1_regression_comparison.main()
    out = capsys.readouterr().out
    assert "案例1" in out


def test_case2_main_runs(capsys):
    case2_churn_prediction.main()
    out = capsys.readouterr().out
    assert "案例2" in out


def test_case3_main_runs(capsys):
    case3_clustering_pca.main()
    out = capsys.readouterr().out
    assert "案例3" in out


def test_case4_main_runs(capsys):
    case4_credit_scoring.main()
    out = capsys.readouterr().out
    assert "案例4" in out

"""pytest 公共配置：路径注入 + 缺失依赖桩。

背景：本仓库的 ML 教学脚本（kmeans_scratch.py、case3_clustering_pca.py 等）
在模块级「import matplotlib」并 `matplotlib.use("Agg")`。CI 环境装了真实
matplotlib，但本地轻量环境（如 rag_demo）可能没有。为了让测试套件在这些环境
都能跑，这里在 matplotlib 不可用时注入一个最小桩模块，使导入成功、绘图调用
成 no-op。算法逻辑（我们要测的部分）完全不依赖绘图。

真实 matplotlib 已安装时（CI），下面的 try/except 会跳过桩逻辑，使用真包。
"""

import sys
import types
from pathlib import Path

# 把业务代码目录加入 sys.path，使测试可 `import linear_regression_gd` 等
CODE_DIR = Path(__file__).resolve().parents[1] / "code" / "01-traditional-ml"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))


def _install_matplotlib_stub() -> None:
    """注入最小 matplotlib / matplotlib.pyplot 桩（仅当真实包不可用时）。"""

    class _NoOp:
        def __call__(self, *args, **kwargs):
            return _NoOp()

        def __getattr__(self, name):
            return _NoOp()

    mpl = types.ModuleType("matplotlib")
    mpl.use = lambda *a, **k: None
    mpl.rcParams = {}
    mpl.rc = types.ModuleType("matplotlib.rc")
    mpl.rcParams = {}
    sys.modules["matplotlib"] = mpl

    plt = types.ModuleType("matplotlib.pyplot")

    def _noop(*args, **kwargs):
        return None

    for name in [
        "figure", "scatter", "title", "legend", "tight_layout", "savefig", "show",
        "xlabel", "ylabel", "colorbar", "close", "axis", "grid", "hist", "plot",
        "imshow", "clf", "pause", "suptitle", "annotate", "bar", "text", "setp",
        "xticks", "yticks", "xlim", "ylim", "subplot", "subplot2grid", "style",
        "connect", "disconnect", "switch_backend",
    ]:
        setattr(plt, name, _noop)

    def _subplots(*args, **kwargs):
        return _NoOp(), _NoOp()

    plt.subplots = _subplots
    sys.modules["matplotlib.pyplot"] = plt


try:
    import matplotlib  # noqa: F401
except ImportError:
    _install_matplotlib_stub()

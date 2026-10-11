"""
决策树（CART 分类）：从零实现
-----------------------------
背景：通过递归二分构建树，用 Gini 不纯度选最优切分。可视化打印决策规则。

运行：python decision_tree_scratch.py
依赖：numpy, scikit-learn
说明：为演示清晰，训练集规模刻意取小；大数据请用 sklearn 的 DecisionTreeClassifier。
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature  # 内部节点：切分特征索引
        self.threshold = threshold  # 内部节点：切分阈值
        self.left = left
        self.right = right
        self.value = value  # 叶节点：类别


def gini(y):
    classes, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return 1.0 - np.sum(p**2)


def best_split(X, y):
    best_gain = -1.0
    best = None
    parent = gini(y)
    n_features = X.shape[1]
    for f in range(n_features):
        thresholds = np.unique(X[:, f])
        for t in thresholds:
            left_mask = X[:, f] <= t
            right_mask = ~left_mask
            if left_mask.sum() == 0 or right_mask.sum() == 0:
                continue
            w_l = left_mask.sum() / len(y)
            w_r = right_mask.sum() / len(y)
            gain = parent - w_l * gini(y[left_mask]) - w_r * gini(y[right_mask])
            if gain > best_gain:
                best_gain = gain
                best = (f, t)
    return best


def build_tree(X, y, depth=0, max_depth=6, min_samples_split=2):
    if len(y) < min_samples_split or depth >= max_depth or gini(y) == 0:
        classes, counts = np.unique(y, return_counts=True)
        return Node(value=classes[np.argmax(counts)])
    split = best_split(X, y)
    if split is None:
        classes, counts = np.unique(y, return_counts=True)
        return Node(value=classes[np.argmax(counts)])
    f, t = split
    left_mask = X[:, f] <= t
    right_mask = ~left_mask
    left = build_tree(
        X[left_mask], y[left_mask], depth + 1, max_depth, min_samples_split
    )
    right = build_tree(
        X[right_mask], y[right_mask], depth + 1, max_depth, min_samples_split
    )
    return Node(feature=f, threshold=t, left=left, right=right)


def _predict_one(node, x):
    if node.value is not None:
        return node.value
    if x[node.feature] <= node.threshold:
        return _predict_one(node.left, x)
    return _predict_one(node.right, x)


def predict(tree, X):
    return np.array([_predict_one(tree, x) for x in X])


def print_tree(node, feature_names, depth=0):
    indent = "  " * depth
    if node.value is not None:
        print(f"{indent}→ 叶节点: 类别={node.value}")
        return
    print(f"{indent}if {feature_names[node.feature]} <= {node.threshold:.3f}:")
    print_tree(node.left, feature_names, depth + 1)
    print(f"{indent}else:")
    print_tree(node.right, feature_names, depth + 1)


def main():
    X, y = make_classification(
        n_samples=300, n_features=4, n_informative=3, n_redundant=1, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    tree = build_tree(X_train, y_train, max_depth=5)
    y_pred = predict(tree, X_test)

    print("【决策树 CART · 从零实现】")
    print("  测试集 Accuracy=%.4f" % accuracy_score(y_test, y_pred))
    print("  决策规则（前几层）：")
    print_tree(tree, [f"x{i}" for i in range(X.shape[1])], depth=0)


if __name__ == "__main__":
    main()

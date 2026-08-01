"""
Matplotlib 基础 —— 6 个核心 API 示例

覆盖知识点：
  plt.plot()    — 折线图（训练损失曲线）
  plt.bar()     — 柱状图（模型对比）
  plt.scatter() — 散点图（数据分布）
  plt.pie()     — 饼图（占比展示）
  plt.subplots()— 子图布局（2×2）
  plt.savefig() — 保存高分辨率图像（dpi=300）
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 中文字体设置（SimHei 不可用时回退英文）
# ============================================================
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题


# ============================================================
# 1. plt.plot() — 折线图：模拟训练损失曲线
""""
总结：
先导入，设置字体，将横纵坐标放在plot里面，然后添加细节

"""
# ============================================================
def demo_line():
    """
    折线图：训练损失 vs 验证损失随 epoch 下降
    plt.plot(x, y, color, linewidth, marker, markersize, label)
    """
    epochs = np.arange(0, 21)
    # 模拟损失：训练损失平滑下降，验证损失有波动
    np.random.seed(42)
    train_loss = 2.1 * np.exp(-0.15 * epochs) + 0.05 * np.random.randn(len(epochs))
    val_loss = 2.3 * np.exp(-0.13 * epochs) + 0.12 * np.random.randn(len(epochs))

    #创建图表，设置大小
    plt.figure(figsize=(8, 5))

    # linewidth=2 细线；marker='o' 数据点标记；markersize=6
    plt.plot(epochs, train_loss, color="#1f77b4", linewidth=2,
             marker="o", markersize=6, label="训练损失")
    plt.plot(epochs, val_loss, color="#ff7f0e", linewidth=2,
             marker="s", markersize=6, label="验证损失")

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("训练过程中的损失曲线", fontsize=14)
    plt.legend(frameon=True, fancybox=True, fontsize=11)
    plt.grid(True, alpha=0.3)          # 浅灰网格，不抢眼
    plt.tight_layout()  #（自动优化排版）自动调整子图间距的函数，防止图表元素（标签、标题、刻度等）重叠或被裁剪。
    plt.show()


# ============================================================
# 2. plt.bar() — 柱状图：模型准确率对比
# ============================================================
def demo_bar():
    """
    柱状图：不同模型的测试准确率对比
    plt.bar(x, height, color, edgecolor, linewidth)
    plt.bar_label() — 柱顶直接标注数值
    """
    models = ["ResNet-50", "ViT-B", "EfficientNet", "MobileNet", "DenseNet"]
    accuracy = [76.2, 81.5, 78.9, 70.3, 79.8]

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(models, accuracy, color=colors, edgecolor="white", linewidth=1.2)

    # 柱顶标注数值（保留一位小数）
    for bar, val in zip(bars, accuracy):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"{val:.1f}%", ha="center", va="bottom", fontsize=11)

    plt.xlabel("模型")
    plt.ylabel("准确率 (%)")
    plt.title("各模型 ImageNet 测试准确率对比", fontsize=14)
    plt.ylim(65, 87)     #设置y轴范围                      # 留出标注空间
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# 3. plt.scatter() — 散点图：身高-体重分布
# ============================================================
def demo_scatter():
    """
    散点图：身高 vs 体重，点大小映射 BMI
    plt.scatter(x, y, s=size, c=color, alpha, cmap)
    """
    np.random.seed(42)
    n = 80
    height = np.random.normal(170, 10, n)        # 身高 cm
    weight = np.random.normal(65, 12, n)          # 体重 kg
    bmi = weight / (height / 100) ** 2            # BMI 用作颜色映射
    sizes = bmi * 8                               # 点大小正比于 BMI

    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(height, weight, s=sizes, c=bmi,
                          cmap="YlOrRd", alpha=0.75, edgecolors="white", linewidth=0.5)

    cbar = plt.colorbar(scatter)
    cbar.set_label("BMI", fontsize=11)

    plt.xlabel("身高 (cm)")
    plt.ylabel("体重 (kg)")
    plt.title("身高-体重分布（点大小 & 颜色 = BMI）", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# 4. plt.pie() — 饼图：市场份额占比
# ============================================================
def demo_pie():
    """
    饼图：市场份额占比展示
    plt.pie(values, labels, autopct, explode, colors, wedgeprops, startangle)
    """
    labels = ["华为", "苹果", "小米", "OPPO", "vivo", "其他"]
    shares = [28.5, 22.3, 18.7, 14.2, 10.8, 5.5]
    # 突出"华为"扇区（explode 为非 0 的扇区会偏移出来）
    explode = (0.08, 0, 0, 0, 0, 0)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    plt.figure(figsize=(7, 7))
    wedges, texts, autotexts = plt.pie(
        shares,
        labels=labels,
        autopct="%1.1f%%",
        explode=explode,
        colors=colors,
        wedgeprops={"edgecolor": "white", "linewidth": 2},   # 扇区之间 2px 白边
        startangle=140,           # 旋转起始角度，让视图更平衡
        pctdistance=0.75,         # 百分比标签距圆心距离
    )

    # 调整百分比文字样式
    for t in autotexts:
        t.set_fontsize(10)
        t.set_color("white")
        t.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(12)

    plt.title("2025 Q2 中国智能手机市场份额", fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()


# ============================================================
# 5. plt.subplots() — 子图：2×2 布局整合
# ============================================================
def demo_subplots():
    """
    子图：将折线图、柱状图、散点图、饼图整合到 2×2 画布
    fig, axes = plt.subplots(nrows, ncols, figsize)
    fig.tight_layout() — 防止子图重叠
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # ---- 子图1：折线图 ----
    epochs = np.arange(0, 21)
    np.random.seed(42)
    train_loss = 2.1 * np.exp(-0.15 * epochs) + 0.05 * np.random.randn(len(epochs))
    val_loss = 2.3 * np.exp(-0.13 * epochs) + 0.12 * np.random.randn(len(epochs))
    axes[0, 0].plot(epochs, train_loss, color="#1f77b4", linewidth=2, label="训练损失")
    axes[0, 0].plot(epochs, val_loss, color="#ff7f0e", linewidth=2, label="验证损失")
    axes[0, 0].set_title("损失曲线", fontsize=13)
    axes[0, 0].set_xlabel("Epoch")
    axes[0, 0].set_ylabel("Loss")
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(alpha=0.3)

    # ---- 子图2：柱状图 ----
    models = ["ResNet", "ViT", "EffNet", "Mobile", "Dense"]
    accuracy = [76.2, 81.5, 78.9, 70.3, 79.8]
    colors_bar = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    axes[0, 1].bar(models, accuracy, color=colors_bar, edgecolor="white", linewidth=1.2)
    axes[0, 1].set_title("模型准确率", fontsize=13)
    axes[0, 1].set_xlabel("模型")
    axes[0, 1].set_ylabel("准确率 (%)")
    axes[0, 1].set_ylim(65, 87)
    axes[0, 1].grid(axis="y", alpha=0.3)

    # ---- 子图3：散点图 ----
    np.random.seed(42)
    height = np.random.normal(170, 10, 60)
    weight = np.random.normal(65, 12, 60)
    bmi = weight / (height / 100) ** 2
    axes[1, 0].scatter(height, weight, s=bmi * 8, c=bmi, cmap="YlOrRd",
                       alpha=0.75, edgecolors="white", linewidth=0.5)
    axes[1, 0].set_title("身高-体重分布", fontsize=13)
    axes[1, 0].set_xlabel("身高 (cm)")
    axes[1, 0].set_ylabel("体重 (kg)")
    axes[1, 0].grid(alpha=0.3)

    # ---- 子图4：饼图 ----
    labels = ["华为", "苹果", "小米", "OPPO", "vivo", "其他"]
    shares = [28.5, 22.3, 18.7, 14.2, 10.8, 5.5]
    colors_pie = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    axes[1, 1].pie(shares, labels=labels, autopct="%1.1f%%", colors=colors_pie,
                   wedgeprops={"edgecolor": "white", "linewidth": 1.5}, startangle=140)
    axes[1, 1].set_title("手机市场份额", fontsize=13)

    # 总标题 + 防重叠
    fig.suptitle("Matplotlib 基础四图总览", fontsize=16, y=1.01)
    fig.tight_layout()
    plt.show()


# ============================================================
# 6. plt.savefig() — 保存高分辨率图像
# ============================================================
def demo_save():
    """
    保存图像：生成一张折线图并保存为 PNG
    plt.savefig("file.png", dpi=300, bbox_inches="tight")
    高分设置：dpi=300 保证打印/汇报清晰度
    """
    x = np.linspace(0, 4 * np.pi, 200)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y_sin, color="#1f77b4", linewidth=2, label="sin(x)")
    plt.plot(x, y_cos, color="#ff7f0e", linewidth=2, label="cos(x)")
    plt.axhline(0, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("sin(x) 与 cos(x)", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # dpi=300：高清输出，适合打印和 PPT 汇报
    # bbox_inches="tight"：自动裁剪白边
    save_path = "plot_demo.png"
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"图像已保存至: {save_path}")
    plt.show()


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. 折线图 demo_line()")
    print("=" * 50)
    demo_line()

    print("\n" + "=" * 50)
    print("2. 柱状图 demo_bar()")
    print("=" * 50)
    demo_bar()

    print("\n" + "=" * 50)
    print("3. 散点图 demo_scatter()")
    print("=" * 50)
    demo_scatter()

    print("\n" + "=" * 50)
    print("4. 饼图 demo_pie()")
    print("=" * 50)
    demo_pie()

    print("\n" + "=" * 50)
    print("5. 子图布局 demo_subplots()")
    print("=" * 50)
    demo_subplots()

    print("\n" + "=" * 50)
    print("6. 保存图像 demo_save()")
    print("=" * 50)
    demo_save()

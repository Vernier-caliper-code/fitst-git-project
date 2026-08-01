import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 1. sns.heatmap() — 热力图（相关性矩阵）
# ============================================================
np.random.seed(42)
data = pd.DataFrame({
    "学习时长(h)": np.random.normal(5, 2, 100),
    "考试成绩": np.random.normal(70, 15, 100),
    "睡眠时间(h)": np.random.normal(7, 1.5, 100),
    "焦虑指数": np.random.normal(50, 10, 100),
})
corr = data.corr()

plt.figure(figsize=(6, 5))
sns.heatmap(
    corr,
    annot=True,             # 格子内显示数值
    fmt=".2f",              # 保留两位小数
    cmap="coolwarm",         # 红正蓝负，白为0
    center=0,               # 0 对齐白色
    square=True,             # 正方形格子
    linewidths=0.5,         # 格子间边框
    cbar_kws={"shrink": 0.8},  # 缩小 colorbar
)
plt.title("特征相关性热力图", fontsize=14)
plt.tight_layout()
plt.savefig("seaborn_heatmap.png", dpi=150)
plt.close()
print("图1: heatmap 已保存")

# ============================================================
# 2. sns.boxplot() — 箱线图（异常值检测）
# ============================================================
# 构造餐饮消费数据（模拟 tips 数据集）
np.random.seed(1)
days = ["周四", "周五", "周六", "周日"]
times = ["午餐", "晚餐"]
rows = []
for day in days:
    for time in times:
        n = 30
        base = {"周六": 22, "周日": 24, "周五": 18, "周四": 16}[day]
        base += 3 if time == "晚餐" else 0
        bills = np.random.normal(base, 5, n).clip(5)  # clip 保证正值
        for b in bills:
            rows.append({"星期": day, "时段": time, "消费金额($)": round(b, 2)})
tips = pd.DataFrame(rows)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图：按星期分组
sns.boxplot(
    x="星期", y="消费金额($)", hue="星期",
    data=tips,
    palette="Set3",
    linewidth=1.2,
    legend=False,
    ax=axes[0],
)
axes[0].set_title("各天消费箱线图")

# 右图：hue 再加一层分组
sns.boxplot(
    x="星期", y="消费金额($)", hue="时段",
    data=tips,
    palette="pastel",
    ax=axes[1],
)
axes[1].set_title("午餐 vs 晚餐 消费箱线图")
axes[1].legend(title="时段", loc="upper right")

plt.tight_layout()
plt.savefig("seaborn_boxplot.png", dpi=150)
plt.close()
print("图2: boxplot 已保存")

# ============================================================
# 3. sns.pairplot() — 两两关系矩阵（EDA 利器）
# ============================================================
# 用 numpy 构造鸢尾花式数据（3类 × 50样本 × 4特征）
np.random.seed(0)
n = 50
# setosa: 小而窄
s = pd.DataFrame({"花萼长": np.random.normal(5.0, 0.3, n),
                   "花萼宽": np.random.normal(3.4, 0.3, n),
                   "花瓣长": np.random.normal(1.5, 0.2, n),
                   "花瓣宽": np.random.normal(0.2, 0.05, n),
                   "品种": "setosa"})
# versicolor: 中等
vc = pd.DataFrame({"花萼长": np.random.normal(5.9, 0.4, n),
                    "花萼宽": np.random.normal(2.7, 0.2, n),
                    "花瓣长": np.random.normal(4.3, 0.3, n),
                    "花瓣宽": np.random.normal(1.3, 0.1, n),
                    "品种": "versicolor"})
# virginica: 大而宽
vg = pd.DataFrame({"花萼长": np.random.normal(6.6, 0.5, n),
                    "花萼宽": np.random.normal(3.0, 0.2, n),
                    "花瓣长": np.random.normal(5.5, 0.4, n),
                    "花瓣宽": np.random.normal(2.0, 0.2, n),
                    "品种": "virginica"})
iris = pd.concat([s, vc, vg], ignore_index=True)

g = sns.pairplot(
    iris,
    hue="品种",
    diag_kind="kde",        # 对角放密度曲线（比直方图更平滑）
    palette="Set2",
    corner=False,           # True 则只显示左下三角
    height=2.2,
)
g.figure.suptitle("鸢尾花 Pairplot — 两两特征关系", y=1.02, fontsize=14)
g.savefig("seaborn_pairplot.png", dpi=150)
plt.close()
print("图3: pairplot 已保存")

print("\n全部图表已生成。")

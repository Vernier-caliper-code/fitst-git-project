"""
Day 3 练习：读取 CSV 文件，逐行处理，异常处理完善
知识要点：with 语句、文件读写、try/except、split 字符串处理
"""

def parse_row(line: str, row_num: int):
    """解析一行 CSV 数据，返回 (name, age, score) 或 None"""
    # 去掉首尾空白和换行符
    line = line.strip()
    """
     所以你后面写脚本的套路就是——读到东西先 .strip()
    再处理，省得被空白字符坑了查半天。
    # 1. 文件每行末尾自带换行符
     "张三,20,85\n"   # readlines() 返回的每行都带 \n
    
    """

    # 跳过空行
    if not line:
        return None

    parts = line.split(",")

    # 检查列数是否正确
    if len(parts) != 3:
        print(f"  [警告] 第 {row_num} 行列数不对，跳过: {line}")
        return None

    name, age_str, score_str = parts
    name = name.strip()

    # 校验 name 不为空
    if not name:
        print(f"  [警告] 第 {row_num} 行 name 为空，跳过")
        return None

    # 校验 age 和 score 是数字
    try:
        age = int(age_str.strip())
        score = float(score_str.strip())
    except ValueError as e:
        print(f"  [警告] 第 {row_num} 行数据类型错误 ({e})，跳过: {line}")
        return None

    return [name, age, score]


def main():
    csv_path = "data.csv"
    valid_rows = []

    # 用 with 语句打开文件（自动关闭，替代 try/finally）—— Day 3 核心知识点
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # Day 3 学的 readlines()
    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_path}'，请确认文件存在")
        return
    except PermissionError:
        print(f"错误：没有权限读取文件 '{csv_path}'")
        return

    print(f"共读取 {len(lines)} 行，开始逐行处理...\n")

    for i, line in enumerate(lines, start=1):
        if i == 1:
            print(f"  第 {i} 行（表头）: {line.strip()}")
            continue

        result = parse_row(line, i)
        if result:
            name, age, score = result
            valid_rows.append(result)
            print(f"  第 {i} 行 [OK]: name={name}, age={age}, score={score}")

    # 汇总输出
    print(f"\n{'='*40}")
    print(f"处理完毕：有效记录 {len(valid_rows)} 条")
    if valid_rows:
        ages = [r[1] for r in valid_rows]
        scores = [r[2] for r in valid_rows]
        print(f"平均年龄: {sum(ages)/len(ages):.1f}")
        print(f"平均分数: {sum(scores)/len(scores):.1f}")

        # 用 with 写入处理结果
        try:
            with open("output.csv", "w", encoding="utf-8") as f:
                f.write("name,age,score\n")
                for name, age, score in valid_rows:
                    f.write(f"{name},{age},{score}\n")
            print("结果已写入 output.csv")
        except IOError as e:
            print(f"写入文件失败: {e}")


if __name__ == "__main__":
    main()

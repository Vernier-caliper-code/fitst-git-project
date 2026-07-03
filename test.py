"""读取 CSV 文件，逐行处理成绩，异常处理完善"""

import csv
import sys

INPUT_FILE = "students.csv"
REQUIRED_HEADERS = ["姓名", "语文", "数学", "英语"]

def parse_row(row: dict) -> dict | None:
    """解析一行，返回格式化数据；失败返回 None"""
    name = row["姓名"].strip()
    scores = {}
    for subject in REQUIRED_HEADERS[1:]:  # 语文/数学/英语
        raw = row[subject].strip()
        if not raw:
            print(f"  ⚠ {name} — {subject} 成绩缺失，跳过")
            return None
        try:
            scores[subject] = int(raw)
        except ValueError:
            print(f"  ✗ {name} — '{raw}' 不是有效数字，跳过")
            return None
    total = sum(scores.values())
    avg = total / len(scores)
    return {"姓名": name, **scores, "总分": total, "平均分": avg}


def main() -> None:
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # 校验表头
            if reader.fieldnames != REQUIRED_HEADERS:
                actual = [h.strip() for h in reader.fieldnames]
                if actual != REQUIRED_HEADERS:
                    print(f"表头不匹配: 期望 {REQUIRED_HEADERS}, 实际 {actual}")
                    sys.exit(1)

            results = []
            for line_no, row in enumerate(reader, start=2):  # 第1行是表头
                result = parse_row(row)
                if result:
                    results.append(result)

        if not results:
            print("没有任何有效数据！")
            sys.exit(1)

        results.sort(key=lambda r: r["总分"], reverse=True)

        print(f"{'排名':<4}{'姓名':<6}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分':<6}")
        for i, r in enumerate(results, 1):
            print(f"{i:<4}{r['姓名']:<6}{r['语文']:<6}{r['数学']:<6}{r['英语']:<6}{r['总分']:<6}{r['平均分']:<6.1f}")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{INPUT_FILE}'")
        sys.exit(1)
    except PermissionError:
        print(f"错误：没有权限读取 '{INPUT_FILE}'")
        sys.exit(1)


if __name__ == "__main__":
    main()

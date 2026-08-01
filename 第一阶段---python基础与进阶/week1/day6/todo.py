import json
import os

"""
Day 6 项目：命令行 TODO 管理器
功能：添加、列出、标记完成、删除
存储：JSON 文件持久化
"""

'''
总结：做一个小项目的步骤
 1. 确定数据长什么样     →  每个任务: {"id", "title", "done"}
  2. 确定用什么容器装     →  列表装多个任务: [{...}, {...}, ...]
  3. 确定怎么持久化       →  JSON 文件，启动读，退出写
  4. 写正常逻辑           →  增删改查，先不管异常
  5. 崩一个修一个         →  空输入、不存在id、文件损坏...

'''


DATA_FILE = "todo_data.json"


# ====== Step 1：数据结构 ======
# 每个任务就是一个字典 {"id": 1, "title": "写作业", "done": False}
# 整个任务列表就是这些字典的列表


def load_tasks():
    """程序启动时从 JSON 文件读取任务列表"""
    if not os.path.exists(DATA_FILE):
        return []  # 第一次运行，文件不存在，返回空列表

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)  # json.load：文件 → Python 对象
    except (json.JSONDecodeError, IOError):
        return []  # 文件损坏或读不了，也别崩，给个空列表


def save_tasks(tasks):
    """修改任务后写回 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
        # json.dump：Python 对象 → 文件
        # ensure_ascii=False：中文正常显示
        # indent=2：格式化缩进，人可读


# ====== Step 2：CRUD 操作 ======

def generate_id(tasks):
    """生成新任务的 id：有任务就取最大 id + 1，没有就从 1 开始"""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(tasks, title):
    """添加任务"""
    task = {"id": generate_id(tasks), "title": title, "done": False}
    tasks.append(task)
    print(f"  已添加: [{task['id']}] {title}")


def list_tasks(tasks):
    """列出所有任务"""
    if not tasks:
        print("  暂无任务")
        return

    print(f"  共 {len(tasks)} 个任务:")
    for t in tasks:
        status = "[V]" if t["done"] else "[ ]"
        print(f"    {status}  [{t['id']}] {t['title']}")


def mark_done(tasks, task_id):
    """标记任务为完成"""
    for t in tasks:
        if t["id"] == task_id:
            if t["done"]:
                print(f"  任务 [{task_id}] 已经完成了")
            else:
                t["done"] = True
                print(f"  任务 [{task_id}] 已标记为完成")
            return
    print(f"  找不到 id 为 {task_id} 的任务")


def delete_task(tasks, task_id):
    """删除任务"""
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            print(f"  已删除任务 [{task_id}]")
            return
    print(f"  找不到 id 为 {task_id} 的任务")


# ====== Step 3 & 4：命令行交互循环 ======

def print_menu():
    print("\n  1. 添加任务")
    print("  2. 列出任务")
    print("  3. 标记完成")
    print("  4. 删除任务")
    print("  q. 退出")


def main():
    tasks = load_tasks()  # 程序启动，加载已有数据
    print("=== TODO 管理器 ===")

    while True:
        print_menu()
        choice = input("  请输入选项: ").strip()

        if choice == "1":
            title = input("  任务名称: ").strip()
            if title:
                add_task(tasks, title)
            else:
                print("  任务名不能为空")

        elif choice == "2":
            list_tasks(tasks)

        elif choice == "3":
            try:
                tid = int(input("  要完成的任务 id: "))
                mark_done(tasks, tid)
            except ValueError:
                print("  id 必须是一个数字")

        elif choice == "4":
            try:
                tid = int(input("  要删除的任务 id: "))
                delete_task(tasks, tid)
            except ValueError:
                print("  id 必须是一个数字")

        elif choice.lower() == "q":
            save_tasks(tasks)  # 退出前存盘
            print("  数据已保存，再见!")
            break

        else:
            print("  无效输入，请选 1/2/3/4/q")


if __name__ == "__main__":
    main()

"""
【问题】银行账户类
  实现一个 BankAccount 类，包含：
  - 属性：owner（姓名）、_balance（余额，私有属性）
  - 方法：deposit（存款）、withdraw（取款，余额不足时报错）
  - 打印账户信息时显示姓名和余额

  Python 知识点：class、__init__、self、__str__、@property
"""
# 感受 Python 类的写法差异：没有声明式私有属性，约定用一个下划线 _balance 表示"别碰"
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
        self._transactions: list[str] = []

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("存款金额必须为正数")
        self._balance += amount
        self._transactions.append(f"+{amount:.2f}")
        return f"存入 ${amount:.2f}，余额 ${self._balance:.2f}"

    def withdraw(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("取款金额必须为正数")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount
        self._transactions.append(f"-{amount:.2f}")
        return f"取出 ${amount:.2f}，余额 ${self._balance:.2f}"

    def __str__(self) -> str:
        return f"[{self.owner}] 余额: ${self._balance:.2f}"

if __name__ == "__main__":
    acc = BankAccount("张三", 100)
    print(acc.deposit(50))
    print(acc.withdraw(30))
    print(acc)
    try:
        acc.withdraw(200)
    except ValueError as e:
        print(f"错误: {e}")

"""
【问题】求素数列表
  输入一个整数上限 n，输出 2~n 之间的所有素数。
  用埃拉托色尼筛法实现。

  Python 知识点：列表推导式、enumerate()
"""
# 练习步骤：先读懂筛法逻辑（你 C++ 肯定写过），再看 Python 版最后一行推导式
def prime_sieve(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i, p in enumerate(is_prime) if p]

if __name__ == "__main__":
    n = int(input("输入上限: "))
    primes = prime_sieve(n)
    print(f"2~{n} 之间的素数共 {len(primes)} 个:")
    print(primes)

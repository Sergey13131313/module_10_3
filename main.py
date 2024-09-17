import threading
import random
import time
import logging


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(100):
            if self.balance >= 500:
                if self.lock.locked():
                    self.lock.release()
            else:
                add_accaunt = random.randint(50, 500)
                self.lock.acquire()
                self.balance += add_accaunt
                print(f'Пополнение: {add_accaunt}. Баланс: {self.balance}')
                self.lock.release()
            time.sleep(0.001)

    def take(self):
        for i in range(100):
            sub_account = random.randint(50, 500)
            print(f'Запрос на снятие {sub_account}')
            if self.balance < sub_account:
                if self.lock.locked():
                    self.lock.release()
                print('Запрос отклонён, недостаточно средств')
            else:
                if not self.lock.locked():
                    self.lock.acquire()
                    self.balance -= sub_account
                    self.lock.release()
                print(f'Снятие: {sub_account}. Баланс: {self.balance}')
            time.sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,), name='TH1')
th2 = threading.Thread(target=Bank.take, args=(bk,), name='TH2')

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
aa = 10

import os, textwrap

base = "bank_system_project"
dirs = [
    base,
    f"{base}/models",
    f"{base}/services",
    f"{base}/utils",
    f"{base}/logs"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

write(f"{base}/main.py", """
from services.bank_service import BankService
from utils.logger import get_logger

logger = get_logger()

def menu():
    print(\"\"\"\\n=== BANK SYSTEM ===
1. Create Customer
2. Create Account
3. Deposit
4. Withdraw
5. Show Accounts
6. Exit
\"\"\")

def main():
    bank = BankService()
    while True:
        try:
            menu()
            c = input("Choice: ")

            if c=="1":
                print(bank.create_customer(
                    input("First: "),
                    input("Last: "),
                    input("Address: ")
                ))

            elif c=="2":
                print(bank.create_account(
                    int(input("Customer ID: ")),
                    input("Type: ")
                ))

            elif c=="3":
                print(bank.deposit(
                    int(input("Account ID: ")),
                    float(input("Amount: "))
                ))

            elif c=="4":
                print(bank.withdraw(
                    int(input("Account ID: ")),
                    float(input("Amount: "))
                ))

            elif c=="5":
                print(bank.get_accounts(int(input("Customer ID: "))))

            elif c=="6":
                break

        except Exception as e:
            logger.exception("Error")
            print("Error:", e)

if __name__=="__main__":
    main()
""")

write(f"{base}/models/database.py", """
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "bank.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create()

    def create(self):
        c=self.conn.cursor()

        c.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            address TEXT)
        \"\"\")

        c.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            account_type TEXT,
            balance REAL DEFAULT 0)
        \"\"\")

        self.conn.commit()

    def execute(self,q,p=()):
        cur=self.conn.cursor()
        cur.execute(q,p)
        self.conn.commit()
        return cur
""")

write(f"{base}/models/account.py", """
class Account:
    def __init__(self,cid,atype,balance=0,aid=None):
        self.id=aid
        self.customer_id=cid
        self.account_type=atype
        self.balance=balance

    def deposit(self,a):
        if a<=0: raise ValueError("Invalid amount")
        self.balance+=a
        return self.balance

    def withdraw(self,a):
        if a>self.balance: raise ValueError("Insufficient funds")
        self.balance-=a
        return self.balance
""")

write(f"{base}/services/bank_service.py", """
from models.database import Database
from models.account import Account

class BankService:
    def __init__(self):
        self.db=Database()

    def create_customer(self,f,l,a):
        return self.db.execute(
            "INSERT INTO customers(first_name,last_name,address) VALUES(?,?,?)",
            (f,l,a)).lastrowid

    def create_account(self,cid,t):
        return self.db.execute(
            "INSERT INTO accounts(customer_id,account_type) VALUES(?,?)",
            (cid,t)).lastrowid

    def _acc(self,id):
        r=self.db.execute(
            "SELECT * FROM accounts WHERE id=?",(id,)
        ).fetchone()
        if not r: raise ValueError("Not found")
        return Account(r["customer_id"],r["account_type"],r["balance"],r["id"])

    def deposit(self,id,a):
        acc=self._acc(id)
        acc.deposit(a)
        self.db.execute("UPDATE accounts SET balance=? WHERE id=?",(acc.balance,id))
        return acc.balance

    def withdraw(self,id,a):
        acc=self._acc(id)
        acc.withdraw(a)
        self.db.execute("UPDATE accounts SET balance=? WHERE id=?",(acc.balance,id))
        return acc.balance

    def get_accounts(self,cid):
        return [dict(x) for x in self.db.execute(
            "SELECT * FROM accounts WHERE customer_id=?",(cid,)
        ).fetchall()]
""")

write(f"{base}/utils/logger.py", """
import logging, pathlib
path=pathlib.Path("logs")
path.mkdir(exist_ok=True)

def get_logger():
    log=logging.getLogger("bank")
    log.setLevel(logging.INFO)
    if not log.handlers:
        fh=logging.FileHandler(path/"errors.log")
        ch=logging.StreamHandler()
        fmt=logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fh.setFormatter(fmt); ch.setFormatter(fmt)
        log.addHandler(fh); log.addHandler(ch)
    return log
""")

write(f"{base}/README.md", """
# Banking System

CLI Banking System using Python + SQLite

Run:
python main.py
""")

print("Project created.")

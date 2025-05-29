import os
import sys
from datetime import datetime
from Cardroom import Cardroom

class Bankroll:
    
    def get_save_path(self, filename):
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            base_dir = os.path.join(os.getenv('APPDATA'), 'Bankroll Manager')
        else:
            # Running in script mode (Dev)
            base_dir = os.path.abspath(".")

        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, filename)

    def __init__(self, filename='bankroll.txt'):
        self.filename = self.get_save_path(filename)
        self.cardroom_balances = {}  # e.g. {"acr": 0.0, "888": 0.0}
        self.transactions = []  # Stores tuples of (timestamp, amount, description)
        self.cardrooms = ["888", "acr", "bodog", "wpt-global", "gg-poker", "kk"]
        self.net_profit_offset = 0.0

        self.load_data()

    # Ensure all expected cardrooms are present with at least zero balance
        for cardroom in self.cardrooms:
            if cardroom not in self.cardroom_balances:
                self.cardroom_balances[cardroom] = 0.0
                
    @property
    def balance(self):
        return sum(self.cardroom_balances.values())

    def add_funds(self, cardroom, amount, description='Deposit'):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.cardroom_balances[cardroom] = self.cardroom_balances.get(cardroom, 0.0) + amount
        self.transactions.append((cardroom, amount, description))
        self.save_data()

    def remove_funds(self, cardroom, amount, description='Withdrawal'):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        current_balance = self.cardroom_balances.get(cardroom, 0.0)
        
        if amount > current_balance:
            raise ValueError(f"Insufficient funds in {cardroom.upper()}.")
            
        self.cardroom_balances[cardroom] = current_balance - amount
        self.transactions.append((cardroom, -amount, description))
        self.save_data()
     
    def total_balance(self):
        return sum(self.cardroom_balances.values())
    
    def _record_transaction(self, amount, description):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transactions.append((timestamp, amount, description))
        self.save_data()

    def calculate_statistics(self):
        total_deposits = sum(a for _, a, _ in self.transactions if a > 0)
        total_withdrawals = sum(-a for _, a, _ in self.transactions if a < 0)
        net_profit = self.balance - self.net_profit_offset

        return {
            'Total Deposits': total_deposits,
            'Total Withdrawals': total_withdrawals,
            'Net Profit': net_profit
        }
    def reset_statistics(self):
        # Clear the transaction history
        self.transactions = []
        
        # Save the updated data
        self.save_data()
        
    def reset_net_profit(self):
        self.net_profit_offset = self.balance
        self.save_data()
  
    def save_data(self):
        with open(self.filename, 'w') as file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"timestamp:{timestamp}\n")
            file.write(f"net_profit_offset:{self.net_profit_offset}\n")
            file.write(f"{self.balance}\n")
            
            
            for cardroom, balance in self.cardroom_balances.items():
                file.write(f"timestamp:{timestamp}\n")
                file.write(f"{cardroom}:{balance}\n")
            for cardroom, amount, description in self.transactions:
                file.write(f"timestamp:{timestamp}\n")
                file.write(f"{cardroom}|{amount}|{description}\n")
                
    def load_data(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, 'r') as file:
            lines = file.readlines()
            self.cardroom_balances = {}
            self.transactions = []
            self.net_profit_offset = 0.0  # Initialize the offset

        for line in lines:
            line = line.strip()
            if line.startswith("net_profit_offset:"):
                try:
                    _, offset = line.split(":", 1)
                    self.net_profit_offset = float(offset)
                except ValueError:
                    print(f"Skipping invalid net profit offset line: {line}")
            elif ':' in line and '|' not in line:
                try:
                    cardroom, balance = line.split(':', 1)
                    self.cardroom_balances[cardroom] = float(balance)
                except ValueError:
                    print(f"Skipping invalid balance line: {line}")
            elif '|' in line:
                try:
                    cardroom, amount, description = line.split('|', 2)
                    self.transactions.append((cardroom, float(amount), description))
                except ValueError:
                    print(f"Skipping invalid transaction line: {line}")
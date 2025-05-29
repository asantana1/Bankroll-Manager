import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
from tkinter import messagebox
from Bankroll import Bankroll
from Cardroom import Cardroom
from tkinter import PhotoImage

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller) """
    try:
        base_path = sys._MEIPASS  # Temp folder created by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BankrollApp:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Bankroll Manager")
        self.master.minsize(750, 750)
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        # Bankroll logic
        self.bankroll = Bankroll()
        
        # Header
        header_label = tk.Label(
            self.master, 
            text="Bankroll Manager Version 0.1", 
            font=("Arial", 16, "bold"),
            anchor="center",
            justify="center"
        )
        header_label.grid(row=0, column=0, columnspan=4, pady=(10, 10), sticky="ew")

        # Load and display cardroom images
        self.cardrooms = ["888", "acr", "bodog", "wpt-global", "gg-poker", "kk"]
        self.max_size = (100, 100)
        self.cardroom_images = {}
        
        self.cardroom_entries = {}
        row = 2
        
        for name in self.cardrooms:
            image_path = resource_path(f"images/{name}.png")
            try:
                img = Image.open(image_path)
                img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                self.cardroom_images[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for {name}: {e}")
            
        for cardroom in self.bankroll.cardrooms:
            # Get image for this cardroom
            img = self.cardroom_images.get(cardroom)
            
            if img:
                img_label = tk.Label(master, image=img)
                img_label.grid(row=row, column=0, padx=10, pady=5)
            else:
                # fallback: if no image, show text or empty label
                img_label = tk.Label(master, text=cardroom.upper())
                img_label.grid(row=row, column=0, padx=10, pady=5)

            balance = self.bankroll.cardroom_balances.get(cardroom, 0.0)
            
            label = tk.Label(master, text=f"Balance: ${balance:.2f}", font=("Helvetica", 12, "bold"))
            label.grid(row=row, column=1, sticky="w", pady=2)

            amount_entry = tk.Entry(master)
            amount_entry.grid(row=row, column=2, sticky="w")
            
            btn_frame = tk.Frame(master)
            btn_frame.grid(row=row, column=3, sticky="w")

            deposit_btn = tk.Button(btn_frame, text="Deposit", command=lambda c=cardroom, e=amount_entry: self.cardroom_deposit(c, e))
            deposit_btn.pack(side="left", padx=(0, 5))

            withdraw_btn = tk.Button(btn_frame, text="Withdraw", command=lambda c=cardroom, e=amount_entry: self.cardroom_withdraw(c, e))
            withdraw_btn.pack(side="left")


            self.cardroom_entries[cardroom] = (label, amount_entry)
            row += 1
            
        self.balance_label = tk.Label(master, text=f"Total Balance: ${self.bankroll.balance:.2f}", font=("Helvetica", 20, "bold"), anchor="w", justify="left")
        self.balance_label.grid(row=row, column=0, columnspan=2, sticky="w", padx="20", pady=10)
        
        stats_button = tk.Button(master, text="Show Statistics", command=self.show_statistics)
        stats_button.grid(row=row + 1, column=0, columnspan=4, pady=10)
        
        reset_button = tk.Button(master, text="Reset Statistics", command=self.reset_statistics)
        reset_button.grid(row=row + 2, column=0, columnspan=4, pady=10)
        
        reset_button = tk.Button(master, text="Reset Net Profit", command=self.reset_net_profit)
        reset_button.grid(row= row + 3, column=0, columnspan=4, pady=10)


    def cardroom_deposit(self, cardroom, entry):
        try:
            amount = float(entry.get())
            self.bankroll.add_funds(cardroom, amount)
            self.update_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    def cardroom_withdraw(self, cardroom, entry):
        try:
            amount = float(entry.get())
            self.bankroll.remove_funds(cardroom, amount)
            self.update_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    def update_display(self):
        for cardroom, (label, _) in self.cardroom_entries.items():
            balance = self.bankroll.cardroom_balances.get(cardroom, 0.0)
            label.config(text=f"{cardroom.upper()} Balance: ${balance:.2f}")
        self.balance_label.config(text=f"Total Balance: ${self.bankroll.balance:.2f}", font=("Helvetica", 20, "bold"), anchor="w", justify="left")
        self.balance_label.grid(row=8, column=0, columnspan=2, sticky="w", padx="20", pady=10)
        
    def show_statistics(self):
        stats = self.bankroll.calculate_statistics()
        stats_message = (
            f"Total Deposits: ${stats['Total Deposits']:.2f}\n"
            f"Total Withdrawals: ${stats['Total Withdrawals']:.2f}\n"
            f"Net Profit: ${stats['Net Profit']:.2f}"
        )
        messagebox.showinfo("Statistics", stats_message)
        
    def save_data(self):
        with open(self.filename, 'w') as file:
            file.write(f"{self.balance}\n")
            for timestamp, amount, description in self.transactions:
                file.write(f"{timestamp}|{amount}|{description}\n")

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        
    def reset_statistics(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all statistics?")
        if confirm:
            self.bankroll.reset_statistics()
            self.update_display()
            messagebox.showinfo("Reset Complete", "Statistics have been reset.")
            
    def reset_net_profit(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset Net Profit?")
        if confirm:
            self.bankroll.reset_net_profit()
            messagebox.showinfo("Reset Complete", "Net Profit has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankrollApp(root)
    root.mainloop()
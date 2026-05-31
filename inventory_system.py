import tkinter as tk
from tkinter import ttk, messagebox


class InventoryApp:
    def __init__(self, master):
        self.master = master
        master.title("Inventory System")

        self.items = {}  # {name: {"qty": int, "price": float}}

        # --- Input fields ---
        tk.Label(master, text="Item Name").grid(row=0, column=0)
        self.name_var = tk.Entry(master)
        self.name_var.grid(row=0, column=1)

        tk.Label(master, text="Quantity").grid(row=1, column=0)
        self.qty_var = tk.Entry(master)
        self.qty_var.grid(row=1, column=1)

        tk.Label(master, text="Price ($)").grid(row=2, column=0)
        self.price_var = tk.Entry(master)
        self.price_var.grid(row=2, column=1)

        # --- Buttons ---
        tk.Button(master, text="Add/Update", command=self.add_item).grid(row=0, column=2)
        tk.Button(master, text="Remove", command=self.remove_item).grid(row=1, column=2)
        tk.Button(master, text="Total Value", command=self.total_value).grid(row=2, column=2)

        # --- Table ---
        self.table = ttk.Treeview(master, columns=("qty", "price"), show="headings")
        self.table.heading("qty", text="Quantity")
        self.table.heading("price", text="Price ($)")
        self.table.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)

        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def refresh_table(self):
        for i in self.table.get_children():
            self.table.delete(i)
        for name, info in self.items.items():
            self.table.insert("", "end", iid=name, values=(info["qty"], f"{info['price']:.2f}"), text=name)

    def add_item(self):
        name = self.name_var.get().strip()
        try:
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
        except ValueError:
            messagebox.showwarning("Invalid input", "Quantity must be integer, price numeric")
            return

        if name:
            if name in self.items:
                self.items[name]["qty"] += qty
                self.items[name]["price"] = price  # update price
            else:
                self.items[name] = {"qty": qty, "price": price}
            self.refresh_table()
            self.name_var.delete(0, tk.END); self.qty_var.delete(0, tk.END); self.price_var.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing name", "Enter an item name")

    def remove_item(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Select item", "Select an item to remove")
            return
        for name in selected:
            del self.items[name]
        self.refresh_table()

    def total_value(self):
        value = sum(i["qty"] * i["price"] for i in self.items.values())
        messagebox.showinfo("Inventory Value", f"Total value: ${value:.2f}")


# === Run it ===
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.geometry("400x300")
    root.mainloop()
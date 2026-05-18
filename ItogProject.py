import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x500")

        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        # Выбор валют
        tk.Label(root, text="Из:").grid(row=1, column=0, padx=10, pady=10)
        self.from_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY"])
        self.from_currency.set("USD")
        self.from_currency.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="В:").grid(row=2, column=0, padx=10, pady=10)
        self.to_currency = ttk.Combobox(root, values=["USD", "EUR", "RUB", "GBP", "JPY"])
        self.to_currency.set("EUR")
        self.to_currency.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка конвертации
        self.convert_btn = tk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Результат
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=("Сумма", "Из", "В", "Результат"), show="headings")
        self.history_tree.heading("Сумма", text="Сумма")
        self.history_tree.heading("Из", text="Из")
        self.history_tree.heading("В", text="В")
        self.history_tree.heading("Результат", text="Результат")
        self.history_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Загрузка истории
        self.load_history()
    def get_exchange_rate(self, from_curr, to_curr):
        api_key = "YOUR_API_KEY"  # Замените на ваш ключ
        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"

        try:
            response = requests.get(url)
            data = response.json()
            rate = data["rates"].get(to_curr)
            if rate is None:
                messagebox.showerror("Ошибка", "Валюта не найдена")
                return None
            return rate
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить курс: {e}")
            return None
    def save_history(self, amount, from_curr, to_curr, result):
        history = self.load_history_data()
        history.append({
            "amount": amount,
            "from": from_curr,
            "to": to_curr,
            "result": result
        })
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        self.refresh_history_table()

    def load_history_data(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_history(self):
        history = self.load_history_data()
        for item in history:
            self.history_tree.insert("", "end", values=(
                item["amount"], item["from"], item["to"], item["result"]
            ))

    def refresh_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        self.load_history()
    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число")
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate is not None:
            result = amount * rate
            self.result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
            self.save_history(amount, from_curr, to_curr, f"{result:.2f}")
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # Переменные
        self.length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)

        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля (8-64):").pack(pady=5)
        length_slider = ttk.Scale(
            self.root,
            from_=8,
            to=64,
            orient="horizontal",
            variable=self.length
        )
        length_slider.pack(fill="x", padx=20)

        length_label = ttk.Label(self.root, textvariable=self.length)
        length_label.pack()

        # Чекбоксы выбора символов
        ttk.Checkbutton(
            self.root,
            text="Цифры (0-9)",
            variable=self.use_digits
        ).pack(anchor="w", padx=20)
        ttk.Checkbutton(
            self.root,
            text="Буквы (A-Z, a-z)",
            variable=self.use_letters
        ).pack(anchor="w", padx=20)
        ttk.Checkbutton(
            self.root,
            text="Спецсимволы (!@#$% и т. д.)",
            variable=self.use_special
        ).pack(anchor="w", padx=20)

        # Кнопка генерации
        generate_btn = ttk.Button(
            self.root,
            text="Сгенерировать пароль",
            command=self.generate_password
        )
        generate_btn.pack(pady=20)

        # Поле вывода пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            self.root,
            textvariable=self.password_var,
            state="readonly",
            font=("Courier", 12)
        )
        password_entry.pack(fill="x", padx=20, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(anchor="w", padx=20)
        columns = ("ID", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_history_table()

    def generate_password(self):
        length = self.length.get()

        if length < 8 or length > 64:
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 8 до 64 символов!")
            return

        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)

        # Добавляем в историю
        char_types = []
        if self.use_digits.get(): char_types.append("Цифры")
        if self.use_letters.get(): char_types.append("Буквы")
        if self.use_special.get(): char_types.append("Спецсимволы")

        history_item = {
            "password": password,
            "length": length,
            "characters": ", ".join(char_types)
        }
        self.history.append(history_item)
        self.save_history()
        self.update_history_table()

    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, item in enumerate(self.history[-10:], 1):
            self.tree.insert("", "end", values=(
                i,
                item["password"],
                item["length"],
                item["characters"]
            ))

    def load_history(self):
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

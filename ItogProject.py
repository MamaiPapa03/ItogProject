import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0, sticky="w")
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Описание погоды:").grid(row=2, column=0, sticky="w")
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Осадки:").grid(row=3, column=0, sticky="w")
        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(root, variable=self.rain_var).grid(row=3, column=1, sticky="w")

        # Кнопка добавления
        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Rain"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Rain", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, sticky="w")
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по температуре (>):").grid(row=7, column=0, sticky="w")
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=10, column=0, pady=10)
        tk.Button(root, text="Загрузить из JSON", command=self.load_data).grid(row=10, column=1, pady=10)

      def add_entry(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()
        rain = self.rain_var.get()

        # Проверка корректности
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return

        # Добавление записи
        entry = {
            "date": date_str,
            "temperature": temp,
            "description": desc,
            "rain": rain
        }
        self.entries.append(entry)
        self.update_table()
        self.clear_inputs()
    def apply_filters(self):
        filtered = self.entries
        date_filter = self.filter_date_entry.get()
        temp_filter_str = self.filter_temp_entry.get()

        if date_filter:
            filtered = [e for e in filtered if e["date"] == date_filter]

        if temp_filter_str:
            try:
                temp_filter = float(temp_filter_str)
                filtered = [e for e in filtered if e["temperature"] > temp_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом")
                return

        self.update_table(filtered)

    def reset_filters(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()
    def save_data(self):
        with open("weather_diary.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в weather_diary.json")

    def load_data(self):
        try:
            with open("weather_diary.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Данные загружены из weather_diary.json")
        except FileNotFoundError:
            self.entries = []
    def update_table(self, entries=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        entries = entries or self.entries
        for entry in entries:
            rain_text = "Да" if entry["rain"] else "Нет"
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temperature']}°C",
                entry["description"],
                rain_text
            ))

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()


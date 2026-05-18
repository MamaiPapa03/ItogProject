import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник погоды")
        self.root.geometry("900x600")

        # Загрузка данных
        self.records = self.load_records()

        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Фрейм для добавления записей
        add_frame = ttk.LabelFrame(main_frame, text="Добавить запись", padding="10")
        add_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(add_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(add_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Температура (°C):").grid(row=1, column=0, sticky=tk.W)
        self.temp_entry = ttk.Entry(add_frame)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Описание погоды:").grid(row=2, column=0, sticky=tk.W)
        self.desc_entry = ttk.Entry(add_frame)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Осадки:").grid(row=3, column=0, sticky=tk.W)
        self.precip_var = tk.StringVar(value="Нет")
        ttk.Radiobutton(add_frame, text="Да", variable=self.precip_var, value="Да").grid(row=3, column=1, sticky=tk.W)
        ttk.Radiobutton(add_frame, text="Нет", variable=self.precip_var, value="Нет").grid(row=3, column=2, sticky=tk.W)

        ttk.Button(add_frame, text="Добавить запись",
                   command=self.add_record).grid(row=4, column=0, columnspan=3, pady=10)

        # Фрейм фильтров
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтры", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, sticky=tk.W)
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Температура > (°C):").grid(row=0, column=2, sticky=tk.W)
        self.filter_temp = ttk.Entry(filter_frame)
        self.filter_temp.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(filter_frame, text="Применить фильтры",
                   command=self.apply_filters).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить фильтры",
                   command=self.clear_filters).grid(row=0, column=5, padx=5)

        # Таблица записей
        records_frame = ttk.LabelFrame(main_frame, text="Записи о погоде", padding="10")
        records_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.records_tree = ttk.Treeview(records_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        self.records_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))


        records_frame.columnconfigure(0, weight=1)
        records_frame.rowconfigure(0, weight=1)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.update_records_display()

    def load_records(self):
        """Загрузка записей из JSON-файла"""
        try:
            if os.path.exists('weather_data.json'):
                with open('weather_data.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
            return []

    def save_records(self):
        """Сохранение записей в JSON-файл"""
        with open('weather_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)


    def validate_input(self, date_str, temp_str, description):
        """Валидация вводимых данных"""
        # Проверка даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return False

        # Проверка температуры
        try:
            float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return False

        # Проверка описания
        if not description.strip():
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым")
            return False

        return True

    def addrecord(self):
        """Добавление новой записи"""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = self.precip_var.get()

        if not self.validate_input(date, temp, description):
            return

        record = {
            "date": date,
            "temperature": float(temp),
            "description": description,
            "precipitation": precipitation
        }

        self.records.append(record)
        self.save_records()
        self.update_records_display()

        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set("Нет")

    def apply_filters(self):
        """Применение фильтров к записям"""
        self.update_records_display()

    def clear_filters(self):
        """Сброс фильтров"""
        self.filter_date.delete
            def clear_filters(self):
        """Сброс фильтров"""
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.update_records_display()

    def update_records_display(self):
        """Обновление отображения записей с учётом фильтров"""
        # Очистка таблицы
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        # Применение фильтров
        filtered_records = self.apply_record_filters()

        # Заполнение таблицы
        for record in filtered_records:
            self.records_tree.insert("", "end", values=(
                record["date"],
                f"{record['temperature']}°C",
                record["description"],
                record["precipitation"]
            ))

    def apply_record_filters(self):
        """Применение фильтров к записям"""
        date_filter = self.filter_date.get().strip()
        temp_filter = self.filter_temp.get().strip()

        filtered = []
        for record in self.records:
            # Проверка фильтра по дате
            if date_filter and date_filter != record["date"]:
                continue

            # Проверка фильтра по температуре
            if temp_filter:
                try:
                    min_temp = float(temp_filter)
                    if record["temperature"] <= min_temp:
                        continue
                except ValueError:
                    pass

            filtered.append(record)
        return filtered



if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()

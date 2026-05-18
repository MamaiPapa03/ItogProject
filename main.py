import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор цитат")
        self.root.geometry("800x600")

        # Загрузка данных
        self.quotes = self.load_quotes()
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Фрейм для генерации
        generate_frame = ttk.LabelFrame(main_frame, text="Генерация цитаты", padding="10")
        generate_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(generate_frame, text="Сгенерировать цитату",
                   command=self.generate_quote).grid(row=0, column=0, padx=5)

        # Фрейм фильтров
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтры", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky=tk.W)
        self.author_filter = ttk.Entry(filter_frame)
        self.author_filter.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky=tk.W)
        self.topic_filter = ttk.Entry(filter_frame)
        self.topic_filter.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(filter_frame, text="Применить фильтры",
                   command=self.apply_filters).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить фильтры",
                   command=self.clear_filters).grid(row=0, column=5, padx=5)

        # Отображение цитаты
        self.quote_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.quote_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # История цитат
        history_frame = ttk.LabelFrame(main_frame, text="История цитат", padding="10")
        history_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        columns = ("Автор", "Тема", "Цитата")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.update_history_display()

    def load_quotes(self):
        """Загрузка списка цитат из JSON-файла"""
        try:
            if os.path.exists('quotes.json'):
                with open('quotes.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Создаём базовый набор цитат, если файла нет
                default_quotes = [
                    {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Философия"},
                    {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Литература"},
                    {"text": "Мыслю, следовательно, существую", "author": "Рене Декарт", "topic": "Философия"}
                ]
                self.save_quotes(default_quotes)
                return default_quotes
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки цитат: {e}")
            return []

    def save_quotes(self, quotes):
        """Сохранение списка цитат в JSON-файл"""
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Загрузка истории из JSON-файла"""
        try:
            if os.path.exists('history.json'):
                with open('history.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки истории: {e}")
            return []

    def save_history(self):
        """Сохранение истории в JSON-файл"""
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def generate_quote(self):
        """Генерация случайной цитаты с валидацией"""
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Список цитат пуст!")
            return

        try:
            filtered_quotes = self.apply_current_filters(self.quotes)

            if not filtered_quotes:
                messagebox.showinfo("Информация", "По текущим фильтрам цитат не найдено")
                return

            quote = random.choice(filtered_quotes)
            self.history.append(quote)
            self.save_history()

            # Отображение цитаты
            self.quote_text.delete(1.0, tk.END)
            self.quote_text.insert(1.0, f"{quote['text']}\n\nАвтор: {quote['author']}\nТема: {quote['topic']}")

            self.update_history_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при генерации цитаты: {e}")

    def apply_current_filters(self, quotes_list):
        """Применение текущих фильтров к списку цитат"""
        author_filter = self.author_filter.get().strip().lower()
        topic_filter = self.topic_filter.get().strip().lower()

        filtered = quotes_list

        if author_filter:
            filtered = [q for q in filtered if author_filter in q['author'].lower()]

        if topic_filter:
            filtered = [q for q in filtered if topic_filter in q['topic'].lower()]

        return filtered

    def apply_filters(self):
        """Обновление отображения истории с фильтрами"""
        self.update_history_display()

    def clear_filters(self):
        """Очистка фильтров"""
        self.author_filter.delete(0, tk.END)
        self.topic_filter.delete(0, tk.END)
        self.update_history_display()
            def update_history_display(self):
        """Обновление отображения истории с фильтрами"""
        # Очищаем текущее содержимое
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Получаем отфильтрованную историю
        filtered_history = self.apply_current_filters(self.history)

        # Заполняем таблицу
        for quote in filtered_history:
            self.history_tree.insert("", "end", values=(
                quote['author'],
                quote['topic'],
                quote['text']
            ))

    def validate_input(self, text, author, topic):
        """Валидация вводимых данных"""
        if not text.strip():
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым")
            return False
        if not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым")
            return False
        if not topic.strip():
            messagebox.showerror("Ошибка", "Тема не может быть пустой")
            return False
        return True



# Точка входа в приложение
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()


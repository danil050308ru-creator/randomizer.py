import tkinter as tk
from tkinter import messagebox
import json
import os
import random

class RandomTaskGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Генератор задач")

        # Предопределённые категории и задачи
        self.task_types = {
            "Учёба": ["Прочитать статью", "Написать эссе", "Подготовиться к экзамену"],
            "Спорт": ["Сделать зарядку", "Пойти на пробежку", "Сыграть в футбол"],
            "Работа": ["Подготовить отчет", "Провести встречу", "Ответить на письма"]
        }
        self.tasks = []

        # Создаем интерфейс
        tk.Label(master, text="Нажмите кнопку, чтобы сгенерировать задачу:").pack(pady=10)

        self.task_display = tk.Text(master, height=5, width=40)
        self.task_display.pack(pady=10)

        self.filter_var = tk.StringVar(value="Все")
        options = ["Все"] + list(self.task_types.keys())
        self.filter_menu = tk.OptionMenu(master, self.filter_var, *options, command=self.on_history_filter_change)
        self.filter_menu.pack(pady=5)

        self.generate_button = tk.Button(master, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_button.pack(pady=5)

        self.add_frame = tk.Frame(master)
        self.add_frame.pack(pady=10)

        tk.Label(self.add_frame, text="Категория:").grid(row=0, column=0, padx=5)
        self.new_category_var = tk.StringVar(value=list(self.task_types.keys())[0])
        self.category_menu = tk.OptionMenu(self.add_frame, self.new_category_var, *self.task_types.keys())
        self.category_menu.grid(row=0, column=1, padx=5)

        tk.Label(self.add_frame, text="Задача:").grid(row=1, column=0, padx=5)
        self.new_task_entry = tk.Entry(self.add_frame, width=30)
        self.new_task_entry.grid(row=1, column=1, padx=5)

        self.add_task_button = tk.Button(self.add_frame, text="Добавить задачу", command=self.add_task)
        self.add_task_button.grid(row=2, column=0, columnspan=2, pady=5)

        # История задач
        self.history_label = tk.Label(master, text="История задач:")
        self.history_label.pack(pady=10)

        self.history_display = tk.Text(master, height=10, width=40)
        self.history_display.pack(pady=10)

        self.filter_history_var = tk.StringVar(value="Все")
        history_options = ["Все"] + list(self.task_types.keys())
        self.history_filter_menu = tk.OptionMenu(master, self.filter_history_var, *history_options, command=self.on_history_filter_change)
        self.history_filter_menu.pack(pady=5)

        self.save_button = tk.Button(master, text="Сохранить", command=self.save_task_history)
        self.save_button.pack(pady=5)

        # Загружаем историю задач
        self.load_task_history()

    def generate_task(self):
        selected_type = self.filter_var.get()
        if selected_type == "Все":
            all_tasks = [(task, cat) for cat, tasks in self.task_types.items() for task in tasks]
            if not all_tasks:
                self.display_task("Нет доступных задач.")
                return
            task, category = random.choice(all_tasks)
        else:
            task = random.choice(self.task_types.get(selected_type, []))
            category = selected_type
        self.display_task(task)
        self.tasks.append({"task": task, "category": category})
        self.update_history_display()

    def display_task(self, task):
        self.task_display.delete(1.0, tk.END)
        self.task_display.insert(tk.END, task)

    def update_history_display(self, filtered_tasks=None):
        self.history_display.delete(1.0, tk.END)
        tasks_to_show = filtered_tasks if filtered_tasks is not None else self.tasks
        for item in tasks_to_show:
            self.history_display.insert(tk.END, f"{item['task']} ({item['category']})\n")

    def save_task_history(self):
        try:
            with open("task_history.json", "w", encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Информация", "История задач сохранена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_task_history(self):
        if os.path.exists("task_history.json"):
            try:
                with open("task_history.json", "r", encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        self.update_history_display()

    def on_history_filter_change(self, selected_type):
        if selected_type == "Все":
            self.update_history_display()
        else:
            filtered_tasks = [t for t in self.tasks if t['category'] == selected_type]
            self.update_history_display(filtered_tasks)

    def add_task(self):
        category = self.new_category_var.get()
        task_text = self.new_task_entry.get().strip()
        if not task_text:
            messagebox.showerror("Ошибка", "Введите текст задачи.")
            return
        if category not in self.task_types:
            messagebox.showerror("Ошибка", "Выбрана неправильная категория.")
            return
        self.task_types[category].append(task_text)
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена в категорию '{category}'.")
        self.new_task_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()

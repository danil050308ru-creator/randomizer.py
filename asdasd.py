import tkinter as tk
from tkinter import messagebox
import json
import random
import os


class RandomTaskGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Task Generator")
        
        self.task_types = {
            "Учёба": ["Прочитать статью", "Написать эссе", "Подготовиться к экзамену"],
            "Спорт": ['Сделать зарядку", "Пойти на пробежку", "Сыграть в футбол'],
            "Работа": ["Подготовить отчет", "Провести встречу", "Ответить на письма"],
        }
        
        self.tasks = []
        self.load_task_history()

        self.label = tk.Label(master, text="Нажмите кнопку, чтобы сгенерировать задачу:")
        self.label.pack(pady=10)

        self.task_display = tk.Text(master, height=5, width=40)
        self.task_display.pack(pady=10)
        
        self.filter_var = tk.StringVar(value="Все")
        self.filter_menu = tk.OptionMenu(master, self.filter_var, "Все", *self.task_types.keys(), command=self.display_filtered_tasks)
        self.filter_menu.pack(pady=5)

        self.generate_button = tk.Button(master, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_button.pack(pady=5)

        self.history_label = tk.Label(master, text="История задач:")
        self.history_label.pack(pady=10)

        self.history_display = tk.Text(master, height=10, width=40)
        self.history_display.pack(pady=10)

        self.save_button = tk.Button(master, text="Сохранить", command=self.save_task_history)
        self.save_button.pack(pady=5)

    def generate_task(self):
        selected_type = self.filter_var.get()

        if selected_type == "Все":
            all_tasks = [task for tasks in self.task_types.values() for task in tasks]
            if not all_tasks:
                self.display_task("Нет доступных задач.")
                return
            task = random.choice(all_tasks)
        else:
            task = random.choice(self.task_types[selected_type])

        self.display_task(task)
        self.tasks.append(task)
        self.update_history_display()

    def display_task(self, task):
        self.task_display.delete(1.0, tk.END)  # Очистка предыдущего текста
        self.task_display.insert(tk.END, task)  # Отображение новой задачи

    def update_history_display(self):
        self.history_display.delete(1.0, tk.END)  # Очистка предыдущего текста
        for task in self.tasks:
            self.history_display.insert(tk.END, f"{task}\n")  # Отображение истории задач

    def save_task_history(self):
        with open("task_history.json", "w") as f:
            json.dump(self.tasks, f)
            messagebox.showinfo("Информация", "История задач сохранена.")

    def load_task_history(self):
        if os.path.exists("task_history.json"):
            with open("task_history.json", "r") as f:
                self.tasks = json.load(f)
                self.update_history_display()

    def display_filtered_tasks(self, selected_type):
        # Обновление отображения задач в зависимости от выбранного типа
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()

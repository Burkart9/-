import tkinter as tk
import csv
import xml.etree.ElementTree as ET

class TodoItem:
    def __init__(self, title):
        self.title = title
        self.completed = False

class TodoListApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("待办事项") # Title
        self.window.geometry("250x500+500+200") # Size, Position
        self.window.resizable(False, False) # Resizable
        self.window.iconbitmap("icon.ico") # 窗口图标

        self.translations = self.load_translations("translations.xml")  # Load Language file
        self.current_lang = "zh"  # 默认使用中文

        self.title_label = tk.Label(self.window, text=self.get_translation("title_label"))
        self.title_label.pack(fill=tk.X, padx=10, pady=10)

        self.todo_listbox = tk.Listbox(self.window)
        self.todo_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.add_frame = tk.Frame(self.window)
        self.add_frame.pack(fill=tk.X, padx=10, pady=10)

        self.add_entry = tk.Entry(self.add_frame)
        self.add_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.add_frame, text=self.get_translation("add_button"), command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = tk.Button(self.window, text=self.get_translation("complete_button"), command=self.mark_completed)
        self.complete_button.pack(fill=tk.X, padx=10, pady=5)

        self.delete_button = tk.Button(self.window, text=self.get_translation("delete_button"), command=self.delete_item, bitmap="error", compound="left")
        self.delete_button.pack(fill=tk.X, padx=10, pady=5)

        self.menu_bar = tk.Menu(self.window)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu.add_command(label="中文", command=lambda: self.change_language("zh"))
        self.language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.menu_bar.add_cascade(label="Languages", menu=self.language_menu)
        self.window.config(menu=self.menu_bar)

        self.load_items()

    def load_translations(self, filename):
        translations = {}
        tree = ET.parse(filename)
        root = tree.getroot()
        for translation in root.findall("translation"):
            lang = translation.get("lang")
            texts = {}
            for text in translation.findall("text"):
                text_id = text.get("id")
                text_value = text.text
                texts[text_id] = text_value
            translations[lang] = texts
        return translations

    def get_translation(self, text_id):
        if self.current_lang in self.translations:
            texts = self.translations[self.current_lang]
            if text_id in texts:
                return texts[text_id]
        return ""

    def load_items(self):
        self.todo_list = []
        self.todo_listbox.delete(0, tk.END)

        with open("todo_list.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                title = row[0]
                completed = row[1]
                item = TodoItem(title)
                item.completed = (completed == "True")
                self.todo_list.append(item)
                status = "✓" if item.completed else ""
                self.todo_listbox.insert(tk.END, f"{status} {item.title}")

    def save_items(self):
        with open("todo_list.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for item in self.todo_list:
                writer.writerow([item.title, str(item.completed)])

    def mark_completed(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            item = self.todo_list[index]
            item.completed = not item.completed
            self.save_items()
            self.load_items()

    def delete_item(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.todo_list[index]
            self.save_items()
            self.load_items()

    def add_item(self):
        title = self.add_entry.get()
        if title:
            item = TodoItem(title)
            self.todo_list.append(item)
            self.save_items()
            self.add_entry.delete(0, tk.END)
            self.load_items()

    def change_language(self, lang):
        self.current_lang = lang
        self.title_label.config(text=self.get_translation("title_label"))
        self.add_button.config(text=self.get_translation("add_button"))
        self.complete_button.config(text=self.get_translation("complete_button"))
        self.delete_button.config(text=self.get_translation("delete_button"))
        self.load_items()

    def run(self):
        self.window.mainloop()

todo_list_app = TodoListApp()
todo_list_app.run()

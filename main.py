from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import sqlite3

class NotesApp(App):
    def build(self):
        # Создание базы данных и таблицы при первом запуске
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                content TEXT
                              )""")
        self.conn.commit()

        # Создание главного макета
        main_layout = BoxLayout(orientation="vertical")

        # Создание поля ввода заголовка заметки
        self.title_input = TextInput(multiline=False)
        main_layout.add_widget(self.title_input)

        # Создание поля ввода содержимого заметки
        self.content_input = TextInput()
        main_layout.add_widget(self.content_input)

        # Создание кнопки сохранения заметки
        save_button = Button(text="Сохранить", on_press=self.save_note)
        main_layout.add_widget(save_button)

        # Создание метки для отображения списка заметок
        notes_label = Label(text="Заметки:")
        main_layout.add_widget(notes_label)

        # Создание макета для отображения списка заметок
        self.notes_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.notes_layout)

        # Загрузка списка заметок при запуске приложения
        self.load_notes()

        return main_layout

    def save_note(self, instance):
        # Сохранение заметки в базу данных
        title = self.title_input.text
        content = self.content_input.text
        self.cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        self.conn.commit()

        # Очистка полей ввода после сохранения заметки
        self.title_input.text = ""
        self.content_input.text = ""

        # Обновление списка заметок
        self.load_notes()

    def load_notes(self):
        # Загрузка списка заметок из базы данных
        self.notes_layout.clear_widgets()
        self.cursor.execute("SELECT * FROM notes")
        notes = self.cursor.fetchall()
        for note in notes:
            note_layout = BoxLayout(orientation="horizontal")
            note_title = Label(text=note[1])
            note_content = Label(text=note[2])
            delete_button = Button(text="Удалить", on_press=lambda instance, id=note[0]: self.delete_note(id))
            note_layout.add_widget(note_title)
            note_layout.add_widget(note_content)
            note_layout.add_widget(delete_button)
            self.notes_layout.add_widget(note_layout)

    def delete_note(self, id):
        # Удаление заметки из базы данных
        self.cursor.execute("DELETE FROM notes WHERE id=?", (id,))
        self.conn.commit()

        # Обновление списка заметок
        self.load_notes()

if __name__ == "__main__":
    NotesApp().run()

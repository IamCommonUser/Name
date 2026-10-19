from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
import flet as ft


class CustomMap:
    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):#проверка на наличие уже существующего элемента
        if key in self._keys:
            idx = self._keys.index(key)
            self._values[idx] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key, default=None):#
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return default



class AbstractEntity(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass


class Book(AbstractEntity):
    def __init__(self, title: str, author: str, year: int, is_read: bool = False, last_page: int = 0):
        self._title = title
        self._author = author
        self._year = year
        self._is_read = is_read
        self._last_page = last_page if not is_read else 0


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        self._year = value

    @property
    def is_read(self) -> bool:
        return self._is_read

    @is_read.setter
    def is_read(self, value: bool):
        self._is_read = value

    @property
    def last_page(self) -> int:
        return self._last_page

    @last_page.setter
    def last_page(self, value: int):
        self._last_page = value if value >= 0 else 0

    def get_info(self) -> str:
        status = "[Прочитано]" if self._is_read else f"[В процессе: стр. {self._last_page}]"
        return f"'{self._title}' — {self._author} ({self._year}) {status}"

    def __str__(self) -> str:
        return self.get_info()

    def __repr__(self) -> str:
        return f"Book(title='{self._title}', author='{self._author}', year={self._year}, is_read={self._is_read}, last_page={self._last_page})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False
        return self._title.lower() == other._title.lower() and self._author.lower() == other._author.lower()

    #сортировка по названию
    def __lt__(self, other) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self._title.lower() < other._title.lower()

#определение окна
class CustomAppTitle(ft.Text):
    def __init__(self, text):
        super().__init__(text, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT)

class CustomLabel(ft.Text):
    def __init__(self, text):
        super().__init__(text, size=14, color=ft.Colors.GREY_700, expand=True)

class CustomInputField(ft.TextField):
    def __init__(self, label_text, width_val=None):
        super().__init__(label=label_text, border_color=ft.Colors.BLUE_300, focused_border_color=ft.Colors.BLUE_700, expand=True if not width_val else False, width=width_val)

class CustomActionButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__(text, on_click=on_click, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))

class CustomDeleteButton(ft.IconButton):
    def __init__(self, on_click):
        super().__init__(icon=ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED_600, on_click=on_click)

class CustomListContainer(ft.ListView):
    def __init__(self):
        super().__init__(expand=True, spacing=10, padding=10)

class CustomRowLayout(ft.Row):
    def __init__(self, controls):
        super().__init__(controls=controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

class CustomCardContainer(ft.Container):
    def __init__(self, content):
        super().__init__(content=content, padding=12, border_radius=8, bgcolor=ft.Colors.GREY_100, border=ft.border.all(1, ft.Colors.GREY_300))

class CustomMainColumn(ft.Column):
    def __init__(self, controls):
        super().__init__(controls=controls, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, expand=True, spacing=15)

class CustomDropdownFilter(ft.Dropdown):
    def __init__(self, on_change, options):
        super().__init__(label="Сортировка", on_change=on_change, options=options, width=200, border_color=ft.Colors.BLUE_300)



class AppService:
    DATA_FILE = "books_data.json"

    @staticmethod #сохранение файлика
    def save_file(login: str, time_in: datetime, time_out: datetime):
        
        fmt = "%d.%m.%Y %H:%M:%S"
        t_in_str = time_in.strftime(fmt)
        t_out_str = time_out.strftime(fmt)
        
        with open("app_report.txt", "w", encoding="utf-8") as f:
            f.write("+------------------------------------+\n")
            f.write("|  login  |   time_in  |   time_out  |\n")
            f.write(f"|{login} | {t_in_str} | {t_out_str} |\n")
            f.write("+------------------------------------+\n")

    @staticmethod #загрузка списка книг если есть
    def load_books() -> list:
        if os.path.exists(AppService.DATA_FILE):
            try:
                with open(AppService.DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [Book(b["title"], b["author"], b["year"], b.get("is_read", False), b.get("last_page", 0)) for b in data]
            except Exception:
                pass
        
        
        initial_books = [
            Book("Book1", "Author1", 2001, False, 0),
            Book("Book2", "Author2", 2002, False, 0),
            Book("Book3", "Author3", 2003, False, 0),
            Book("Book4", "Author4", 2004, False, 0),
            Book("Book5", "Author5", 2005, False, 0),
            Book("Book6", "Author6", 2006, False, 0),
            Book("Book7", "Author7", 2007, False, 0),
            Book("Book8", "Author8", 2008, False, 0),
            Book("Book9", "Author9", 2009, False, 0),
            Book("Book10", "Author10", 2010, False, 0),
        ]
        AppService.save_books(initial_books)
        return initial_books

    @staticmethod
    def save_books(books_list: list):
        raw_data = [{
            "title": b.title, 
            "author": b.author, 
            "year": b.year,
            "is_read": b.is_read,
            "last_page": b.last_page
        } for b in books_list]
        with open(AppService.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)


def main(page: ft.Page):
    page.title = "Личный список и трекер книг"
    page.window.width = 700
    page.window.height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    
    user_login = "NameUser"
    time_in = datetime.now()

    books_collection = AppService.load_books()
    ui_mapping = CustomMap()

    title_view = CustomAppTitle("Моя личная библиотека")
    
    input_title = CustomInputField("Название книги")
    input_author = CustomInputField("Автор")
    input_year = CustomInputField("Год издания")
    
    list_view = CustomListContainer()

    def delete_book(book_obj, card_element):
        if book_obj in books_collection:
            books_collection.remove(book_obj)
            list_view.controls.remove(card_element)
            AppService.save_books(books_collection)
            page.update()

    def update_list_ui():
        list_view.controls.clear()
        for book in books_collection:
            def make_delete_handler(b):
                return lambda e: delete_book(b, ui_mapping.get(b))
            
            def make_status_handler(b, text_control, page_input):
                def handler(e):
                    b.is_read = e.control.value
                    page_input.visible = not b.is_read
                    if b.is_read:
                        page_input.value = "0"
                        b.last_page = 0
                    text_control.value = b.get_info()
                    AppService.save_books(books_collection)
                    page.update()
                return handler

            def make_page_handler(b, text_control):
                def handler(e):
                    val = e.control.value.strip()
                    b.last_page = int(val) if val.isdigit() else 0
                    text_control.value = b.get_info()
                    AppService.save_books(books_collection)
                    page.update()
                return handler

            lbl_info = CustomLabel(book.get_info())
            chk_read = ft.Checkbox(label="Прочитано", value=book.is_read, fill_color=ft.Colors.BLUE_600)
            
            tf_page = ft.TextField(
                label="Стр.", 
                value=str(book.last_page), 
                width=70, 
                height=40,
                text_size=13,
                content_padding=5,
                visible=not book.is_read,
                border_color=ft.Colors.BLUE_200
            )

            chk_read.on_change = make_status_handler(book, lbl_info, tf_page)
            tf_page.on_change = make_page_handler(book, lbl_info)
            btn_del = CustomDeleteButton(on_click=None)

            row_content = CustomRowLayout([
                lbl_info,
                ft.Row([tf_page, chk_read, btn_del], spacing=5, alignment=ft.MainAxisAlignment.END)
            ])
            card = CustomCardContainer(row_content)
            row_content.controls[-1].controls[-1].on_click = make_delete_handler(book)
            
            ui_mapping.put(book, card)
            list_view.controls.append(card)
        page.update()

    def add_book_clicked(e):
        if input_title.value.strip() and input_author.value.strip():
            try:
                year = int(input_year.value.strip()) if input_year.value.strip().isdigit() else datetime.now().year
                new_book = Book(input_title.value.strip(), input_author.value.strip(), year, is_read=False, last_page=0)
                
                if new_book not in books_collection:
                    books_collection.append(new_book)
                    AppService.save_books(books_collection)
                    update_list_ui()
                    
                    input_title.value = ""
                    input_author.value = ""
                    input_year.value = ""
                    page.update()
            except ValueError:
                pass

    def sort_changed(e):
        if dropdown_filter.value == "by_title":
            books_collection.sort()
        elif dropdown_filter.value == "by_year":
            books_collection.sort(key=lambda b: b.year)
        AppService.save_books(books_collection)
        update_list_ui()

    btn_add = CustomActionButton("Добавить книгу", on_click=add_book_clicked)
    
    dropdown_filter = CustomDropdownFilter(
        on_change=sort_changed,
        options=[
            ft.dropdown.Option("by_title", "По названию"),
            ft.dropdown.Option("by_year", "По году издания")
        ]
    )

    
    def handle_window_event(e):
        if e.data == "close":
            time_out = datetime.now()
            AppService.save_file(user_login, time_in, time_out)
            page.window.destroy()

    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    inputs_row = ft.Row([input_title, input_author, input_year], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    actions_row = ft.Row([btn_add, dropdown_filter], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    main_layout = CustomMainColumn([
        title_view,
        inputs_row,
        actions_row,
        ft.Divider(height=10, color=ft.Colors.GREY_400),
        list_view
    ])

    page.add(main_layout)
    update_list_ui()

if __name__ == "__main__":
    ft.app(target=main)

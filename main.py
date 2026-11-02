import customtkinter as ctk
import time
import webbrowser
import winsound

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("550x680")
app.title("MyApple Ultimate OS")
app.configure(fg_color="#0D0D11")

# --- ЗМІННА ДЛЯ ЗБЕРЕЖЕННЯ ІСТОРІЇ КАЛЬКУЛЯТОРА ---
calc_expression = ""


# --- ФУНКЦІЇ ДЛЯ DOCK (ЗАПУСК ПРОГРАМ) ---
def open_browser():
    webbrowser.open("https://google.com")


def save_notes_to_file(text_area):
    with open("notes.txt", "w", encoding="utf-8") as file:
        file.write(text_area.get("0.0", "end-1c"))


def open_notes():
    notes_window = ctk.CTkToplevel(app)
    notes_window.geometry("320x350")
    notes_window.title("Нотатки")
    notes_window.lift()
    notes_window.attributes("-topmost", True)

    text_area = ctk.CTkTextbox(master=notes_window, width=280, height=240, corner_radius=10)
    text_area.pack(pady=15, padx=15)

    try:
        with open("notes.txt", "r", encoding="utf-8") as file:
            text_area.insert("0.0", file.read())
    except FileNotFoundError:
        text_area.insert("0.0", "Тут можна щось написати...")

    save_btn = ctk.CTkButton(
        master=notes_window, text="Зберегти та закрити", fg_color="#FF9500", hover_color="#CC7A00", corner_radius=10,
        command=lambda: [save_notes_to_file(text_area), notes_window.destroy()]
    )
    save_btn.pack(pady=(0, 10))


# --- ВЛАСНИЙ КАЛЬКУЛЯТОР APPLE STYLE ---
def open_calculator():
    global calc_expression
    calc_expression = ""

    calc_window = ctk.CTkToplevel(app)
    calc_window.geometry("320x460")
    calc_window.title("Калькулятор")
    calc_window.configure(fg_color="#0D0D11")
    calc_window.lift()
    calc_window.attributes("-topmost", True)

    # Дисплей калькулятора
    display = ctk.CTkLabel(master=calc_window, text="0", font=("SF Pro Display", 40, "bold"), anchor="e",
                           text_color="#F2F2F7")
    display.pack(pady=20, padx=20, fill="x")

    def press_key(key):
        global calc_expression
        if key == "C":
            calc_expression = ""
            display.configure(text="0")
        elif key == "=":
            try:
                # Безпечне обчислення виразу
                result = str(eval(calc_expression.replace("×", "*").replace("÷", "/")))
                display.configure(text=result)
                calc_expression = result
            except:
                display.configure(text="Помилка")
                calc_expression = ""
        else:
            if calc_expression == "0" or display.cget("text") == "Помилка":
                calc_expression = ""
            calc_expression += str(key)
            display.configure(text=calc_expression)

    # Сітка кнопок
    buttons_frame = ctk.CTkFrame(master=calc_window, fg_color="transparent")
    buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

    keys = [
        ['C', '÷', '×', '-'],
        ['7', '8', '9', '+'],
        ['4', '5', '6', '='],
        ['1', '2', '3', '0']
    ]

    for row_idx, row in enumerate(keys):
        for col_idx, text in enumerate(row):
            # Підбір кольорів як у справжньому калькуляторі iOS
            if text in ['C', '÷', '×', '-', '+', '=']:
                bg = "transparent"
                border = "#FF9500"
                txt_col = "#FF9500"
            else:
                bg = "transparent"
                border = "#2C2C35"
                txt_col = "#F2F2F7"

            btn = ctk.CTkButton(
                master=buttons_frame, text=text, width=65, height=65, corner_radius=32,
                fg_color=bg, border_color=border, border_width=1.5, text_color=txt_col,
                font=("SF Pro Text", 20, "bold"), hover_color="#2C2C35",
                command=lambda t=text: press_key(t)
            )
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)


# --- ІНШІ ФУНКЦІЇ СИСТЕМИ ---
def update_time():
    current_time = time.strftime("%H:%M:%S")
    current_time_short = time.strftime("%H:%M")
    current_date = time.strftime("%A, %d %B")

    label_clock.configure(text=current_time)
    label_date.configure(text=current_date)
    statusbar_time.configure(text=current_time_short)

    app.after(1000, update_time)


def check_password():
    if password_entry.get() == "1234":
        label_error.configure(text="")
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

        # Ховаємо елементи екрана блокування
        glass_panel.pack_forget()
        password_label.pack_forget()
        password_entry.pack_forget()
        my_button.pack_forget()

        # Навігаційний статус-бар угорі
        statusbar_frame.pack(side="top", fill="x", padx=25, pady=5)

        # Панель Dock внизу
        dock_frame.pack(side="bottom", pady=20, padx=20, fill="x")
    else:
        label_error.configure(text="Невірний пароль! 🔒", text_color="#FF453A")


def toggle_theme():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        app.configure(fg_color="#F2F2F7")
        glass_panel.configure(fg_color="#E5E5EA", border_color="#C7C7CC")
        dock_frame.configure(fg_color="#E5E5EA", border_color="#C7C7CC")

        label_clock.configure(text_color="#1C1C1E")
        label_date.configure(text_color="#3A3A3C")
        statusbar_time.configure(text_color="#1C1C1E")
        theme_btn.configure(text="🔋 🌙 Тема", text_color="#1C1C1E", border_color="#1C1C1E")
    else:
        ctk.set_appearance_mode("Dark")
        app.configure(fg_color="#0D0D11")
        glass_panel.configure(fg_color="#16161F", border_color="#2C2C35")
        dock_frame.configure(fg_color="#16161F", border_color="#2C2C35")

        label_clock.configure(text_color="#F2F2F7")
        label_date.configure(text_color="#8E8E93")
        statusbar_time.configure(text_color="#F2F2F7")
        theme_btn.configure(text="🔋 ☀️ Тема", text_color="#FFFFFF", border_color="#8E8E93")


# --- СТРУКТУРА ІНТЕРФЕЙСУ ---

# НАВІГАЦІЙНА ПАНЕЛЬ УГОРІ (СТАТУС-БАР)
statusbar_frame = ctk.CTkFrame(master=app, fg_color="transparent", height=40)

statusbar_time = ctk.CTkLabel(master=statusbar_frame, text="00:00", font=("SF Pro Text", 16, "bold"),
                              text_color="#F2F2F7")
statusbar_time.pack(side="left", padx=5)

theme_btn = ctk.CTkButton(
    master=statusbar_frame, text="🔋 ☀️ Тема", width=100, height=30, fg_color="transparent",
    border_color="#8E8E93", border_width=1, corner_radius=8, text_color="#FFFFFF",
    font=("SF Pro Text", 12, "bold"), command=toggle_theme
)
theme_btn.pack(side="right", padx=5)

# ЕКРАН БЛОКУВАННЯ
glass_panel = ctk.CTkFrame(master=app, fg_color="#16161F", border_color="#2C2C35", border_width=1.5, corner_radius=24)
glass_panel.pack(pady=(50, 20), padx=30, fill="x")

label_date = ctk.CTkLabel(master=glass_panel, text="", font=("SF Pro Text", 15, "bold"), text_color="#8E8E93")
label_date.pack(pady=(20, 5))

label_clock = ctk.CTkLabel(master=glass_panel, text="", font=("SF Pro Display", 68, "bold"), text_color="#F2F2F7")
label_clock.pack(pady=(0, 20))

password_label = ctk.CTkLabel(master=app, text="Введіть PIN-код для розблокування:", font=("SF Pro Text", 14))
password_label.pack(pady=(30, 5))

password_entry = ctk.CTkEntry(master=app, width=180, height=45, placeholder_text="****", show="*", justify="center",
                              font=("SF Pro Text", 18, "bold"), corner_radius=12, fg_color="#16161F",
                              border_color="#2C2C35")
password_entry.pack(pady=5)

label_error = ctk.CTkLabel(master=app, text="", font=("SF Pro Text", 13))
label_error.pack(pady=5)

my_button = ctk.CTkButton(master=app, text="Розблокувати систему", fg_color="transparent", hover_color="#10253C",
                          border_color="#0A84FF", border_width=1.5, corner_radius=18, width=280, height=55,
                          font=("SF Pro Text", 16, "bold"), text_color="#0A84FF", command=check_password)
my_button.pack(pady=15)

# НИЖНЯ ПАНЕЛЬ DOCK
dock_frame = ctk.CTkFrame(master=app, fg_color="#16161F", border_color="#2C2C35", border_width=1.5, corner_radius=20)

btn_safari = ctk.CTkButton(master=dock_frame, text="🌐 Internet", width=100, height=45, fg_color="transparent",
                           border_color="#0A84FF", border_width=1, corner_radius=12, font=("SF Pro Text", 12, "bold"),
                           text_color="#0A84FF", command=open_browser)
btn_safari.pack(side="left", padx=15, pady=10)

btn_notes = ctk.CTkButton(master=dock_frame, text="📝 Notes", width=100, height=45, fg_color="transparent",
                          border_color="#FF9500", border_width=1, corner_radius=12, font=("SF Pro Text", 12, "bold"),
                          text_color="#FF9500", command=open_notes)
btn_notes.pack(side="left", padx=15, pady=10)

btn_calc = ctk.CTkButton(master=dock_frame, text="🧮 Calc", width=100, height=45, fg_color="transparent",
                         border_color="#30D158", border_width=1, corner_radius=12, font=("SF Pro Text", 12, "bold"),
                         text_color="#30D158", command=open_calculator)
btn_calc.pack(side="left", padx=15, pady=10)

update_time()
app.mainloop()

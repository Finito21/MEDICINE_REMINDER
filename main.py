import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import pyttsx3
import dateutil.parser
import os

MEDICATION_FILE = 'medication.csv'

# Funkcja mowy (opcjonalnie)
def speak_text(command):
    text = pyttsx3.init()
    text.say(command)
    text.runAndWait()

# Wczytaj dane leków
def load_medication_data():
    medication_data = []
    if not os.path.exists(MEDICATION_FILE):
        with open(MEDICATION_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nazwa leku", "Dawkowanie", "Częstotliwość", "Godzina przyjęcia"])
    with open(MEDICATION_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) == 4:
                medication_data.append(row)
    return medication_data

# Zapisz dane leków
def save_medication_data(data):
    with open(MEDICATION_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nazwa leku", "Dawkowanie", "Częstotliwość", "Godzina przyjęcia"])
        writer.writerows(data)

# Walidacja danych
def validate_medication(name, dosage, freq, time):
    if not name or not dosage or not freq or not time:
        return False, "Wszystkie pola są wymagane."
    try:
        datetime.datetime.strptime(time, "%H:%M")
    except ValueError:
        return False, "Godzina przyjęcia musi być w formacie HH:MM."
    return True, ""

# Dodawanie leku
def add_medication_schedule():
    name = entry_medication_name.get().strip()
    dosage = entry_dosage.get().strip()
    freq = entry_frequency.get().strip()
    time = entry_schedule_time.get().strip()
    valid, msg = validate_medication(name, dosage, freq, time)
    if not valid:
        messagebox.showerror("Błąd", msg)
        return
    data = load_medication_data()
    data.append([name, dosage, freq, time])
    save_medication_data(data)
    messagebox.showinfo("Sukces", "Lek został dodany.")
    add_window.destroy()
    refresh_table()

# Usuwanie leku
def delete_medication(index):
    data = load_medication_data()
    if index < len(data):
        if messagebox.askyesno("Potwierdź", f"Czy na pewno chcesz usunąć lek: {data[index][0]}?"):
            del data[index]
            save_medication_data(data)
            refresh_table()

# Okno dodawania leku
def open_add_window():
    global add_window, entry_medication_name, entry_dosage, entry_frequency, entry_schedule_time
    add_window = tk.Toplevel(window)
    add_window.title("Dodaj lek")
    add_window.geometry("350x320")
    add_window.config(bg='#333333')
    
    tk.Label(add_window, text="Nazwa leku:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_medication_name = tk.Entry(add_window, font=("Arial", 12))
    entry_medication_name.pack(pady=5)
    tk.Label(add_window, text="Dawkowanie:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_dosage = tk.Entry(add_window, font=("Arial", 12))
    entry_dosage.pack(pady=5)
    tk.Label(add_window, text="Częstotliwość:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_frequency = tk.Entry(add_window, font=("Arial", 12))
    entry_frequency.pack(pady=5)
    tk.Label(add_window, text="Godzina przyjęcia (HH:MM):", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_schedule_time = tk.Entry(add_window, font=("Arial", 12))
    entry_schedule_time.pack(pady=5)
    tk.Button(add_window, text="Dodaj lek", command=add_medication_schedule, font=("Arial", 12), fg="#000000", bg="#00D084").pack(pady=10)

# Tabela leków
def refresh_table():
    for row in table.get_children():
        table.delete(row)
    data = load_medication_data()
    for idx, row in enumerate(data):
        table.insert('', 'end', iid=idx, values=(row[0], row[1], row[2], row[3]))

def on_delete():
    selected = table.selection()
    if selected:
        idx = int(selected[0])
        delete_medication(idx)

def on_edit():
    selected = table.selection()
    if selected:
        idx = int(selected[0])
        data = load_medication_data()
        row = data[idx]
        open_edit_window(idx, row)

def open_edit_window(idx, row):
    global edit_window, entry_medication_name, entry_dosage, entry_frequency, entry_schedule_time
    edit_window = tk.Toplevel(window)
    edit_window.title("Edytuj lek")
    edit_window.geometry("350x320")
    edit_window.config(bg='#333333')
    
    tk.Label(edit_window, text="Nazwa leku:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_medication_name = tk.Entry(edit_window, font=("Arial", 12))
    entry_medication_name.insert(0, row[0])
    entry_medication_name.pack(pady=5)
    tk.Label(edit_window, text="Dawkowanie:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_dosage = tk.Entry(edit_window, font=("Arial", 12))
    entry_dosage.insert(0, row[1])
    entry_dosage.pack(pady=5)
    tk.Label(edit_window, text="Częstotliwość:", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_frequency = tk.Entry(edit_window, font=("Arial", 12))
    entry_frequency.insert(0, row[2])
    entry_frequency.pack(pady=5)
    tk.Label(edit_window, text="Godzina przyjęcia (HH:MM):", font=("Arial", 12), fg="#FFFFFF", bg="#333333").pack(pady=5)
    entry_schedule_time = tk.Entry(edit_window, font=("Arial", 12))
    entry_schedule_time.insert(0, row[3])
    entry_schedule_time.pack(pady=5)
    tk.Button(edit_window, text="Zapisz zmiany", command=lambda: save_edit(idx), font=("Arial", 12), fg="#000000", bg="#00D084").pack(pady=10)

def save_edit(idx):
    name = entry_medication_name.get().strip()
    dosage = entry_dosage.get().strip()
    freq = entry_frequency.get().strip()
    time = entry_schedule_time.get().strip()
    valid, msg = validate_medication(name, dosage, freq, time)
    if not valid:
        messagebox.showerror("Błąd", msg)
        return
    data = load_medication_data()
    data[idx] = [name, dosage, freq, time]
    save_medication_data(data)
    messagebox.showinfo("Sukces", "Lek został zaktualizowany.")
    edit_window.destroy()
    refresh_table()

# Automatyczne przypomnienia
def set_medication_reminders():
    data = load_medication_data()
    current_time = datetime.datetime.now().strftime("%H:%M")
    for row in data:
        try:
            schedule_time = dateutil.parser.parse(row[3]).strftime("%H:%M")
        except Exception:
            continue
        if current_time == schedule_time:
            messagebox.showinfo("Przypomnienie o leku", f"Czas przyjąć lek: {row[0]}.")
            # speak_text(f"Czas przyjąć lek: {row[0]}")  # odkomentuj, jeśli chcesz głosowe przypomnienie
    window.after(60000, set_medication_reminders)

# Główne okno
def close():
    window.destroy()

window = tk.Tk()
window.title("Aplikacja Leków")
window.geometry("1000x500")
window.config(bg='#23272F')

header = tk.Label(window, text="Aplikacja Przypomnień o Lekach", font=("Segoe UI", 22, "bold"), pady=18, bg='#23272F', fg='#00D084')
header.pack()

# Tabela
table_frame = tk.Frame(window, bg='#23272F')
table_frame.pack(pady=10)

columns = ("Nazwa leku", "Dawkowanie", "Częstotliwość", "Godzina przyjęcia")
table = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=130, anchor='center')
table.pack(side='left')

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# Przyciski
button_frame = tk.Frame(window, bg='#23272F')
button_frame.pack(pady=20)

button_style = {
    'font': ("Segoe UI", 13, "bold"),
    'bg': '#00D084',
    'fg': '#23272F',
    'activebackground': '#00B06B',
    'activeforeground': '#23272F',
    'relief': 'flat',
    'bd': 0,
    'highlightthickness': 0,
    'height': 2,
    'width': 18,
    'cursor': 'hand2',
    'padx': 8,
    'pady': 4
}

btn_add = tk.Button(button_frame, text="Dodaj lek", command=open_add_window, **button_style)
btn_add.grid(row=0, column=0, padx=10)
btn_edit = tk.Button(button_frame, text="Edytuj lek", command=on_edit, **button_style)
btn_edit.grid(row=0, column=1, padx=10)
btn_delete = tk.Button(button_frame, text="Usuń lek", command=on_delete, **button_style)
btn_delete.grid(row=0, column=2, padx=10)
btn_exit = tk.Button(button_frame, text="Wyjście", command=close, **button_style)
btn_exit.grid(row=0, column=3, padx=10)

refresh_table()
set_medication_reminders()
window.mainloop()
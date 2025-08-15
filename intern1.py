import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Setup database
conn = sqlite3.connect("bmi_users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT,
        date TEXT
    )
""")
conn.commit()

# BMI categorization
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Calculate BMI and store
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not name or age <= 0 or weight <= 0 or height <= 0:
            raise ValueError

        bmi = round(weight / (height ** 2), 2)
        category = get_bmi_category(bmi)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store in DB
        cursor.execute("INSERT INTO bmi_data (name, age, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, age, weight, height, bmi, category, date))
        conn.commit()

        result_label.config(text=f"BMI: {bmi} ({category})", fg="blue")
        print(f"[INFO] Stored data: {name}, BMI: {bmi}, Category: {category}")

        # Clear input fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        weight_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs!")

# View history
def view_history():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Needed", "Enter your name to view history.")
        return

    cursor.execute("SELECT date, bmi FROM bmi_data WHERE name = ? ORDER BY date", (name,))
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No history found for this user.")
        return

    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
    bmis = [row[1] for row in data]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, bmis, marker='o', color='green')
    plt.title(f"BMI History for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x420")
root.resizable(False, False)

font_style = ("Arial", 12)

tk.Label(root, text="Name", font=font_style).pack()
name_entry = tk.Entry(root, font=font_style)
name_entry.pack()

tk.Label(root, text="Age", font=font_style).pack()
age_entry = tk.Entry(root, font=font_style)
age_entry.pack()

tk.Label(root, text="Weight (kg)", font=font_style).pack()
weight_entry = tk.Entry(root, font=font_style)
weight_entry.pack()

tk.Label(root, text="Height (m)", font=font_style).pack()
height_entry = tk.Entry(root, font=font_style)
height_entry.pack()

tk.Button(root, text="Calculate BMI", font=font_style, command=calculate_bmi).pack(pady=10)
tk.Button(root, text="View BMI History", font=font_style, command=view_history).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
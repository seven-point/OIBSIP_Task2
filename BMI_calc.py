import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Global list to store BMI history
bmi_history = []

# Create a SQLite database connection
conn = sqlite3.connect("bmi_history.db")
cursor = conn.cursor()

# Create a table for BMI history if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bmi_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bmi REAL
    )
''')
conn.commit()

def calculate_bmi():
    height = float(height_entry.get()) / 100
    weight = float(weight_entry.get())
    
    bmi = weight / (height ** 2)
    
    result_label.config(text=f"Your BMI: {bmi}")
    bmi_history.append(bmi)
    cursor.execute("INSERT INTO bmi_history (bmi) VALUES (?)", (bmi,))
    conn.commit()
    
    update_meter(bmi)

def update_meter(bmi):
    angle = bmi*6  # Adjust the range as needed
    canvas.delete("meter")
    draw_meter(bmi,angle)

def draw_meter(bmi,angle):
    canvas.create_arc(10, 10, 190, 190, start=0, extent=180, style=tk.ARC, outline=None, width=10, tags="meter")
    if bmi<18.5:
        canvas.create_arc(10, 10, 190, 190, start=180, extent=-angle, style=tk.ARC, outline="green", width=10, tags="meter")
        canvas.delete("output_label")
        canvas.create_text(100, 100, text="Underweight", font=("Helvetica", 12), tags="output_label")
    elif bmi<25.0:
        canvas.create_arc(10, 10, 190, 190, start=180, extent=-angle, style=tk.ARC, outline="orange", width=10, tags="meter")
        canvas.delete("output_label")
        canvas.create_text(100, 100, text="Normal Weight", font=("Helvetica", 12), tags="output_label")
    else:
        canvas.create_arc(10, 10, 190, 190, start=180, extent=-angle, style=tk.ARC, outline="red", width=10, tags="meter")
        canvas.delete("output_label")
        canvas.create_text(100, 100, text="Overweight", font=("Helvetica", 12), tags="output_label")
    

def show_history():
    cursor.execute("SELECT bmi FROM bmi_history")
    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo("BMI History", "No BMI data available.")
        return
    
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")

    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)

    x_values = list(range(1, len(rows) + 1))
    y_values = [row[0] for row in rows]

    plot.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plot.set_title('BMI Trend Over Time')
    plot.set_xlabel('Measurement Number')
    plot.set_ylabel('BMI')

    canvas = FigureCanvasTkAgg(fig, master=history_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Create the main window
window = tk.Tk()
window.title("BMI Calculator")

# Create and place widgets
height_label = tk.Label(window, text="Height (cm):")
height_label.grid(row=0, column=0, padx=10, pady=10)

height_entry = tk.Entry(window)
height_entry.grid(row=0, column=1, padx=10, pady=10)

weight_label = tk.Label(window, text="Weight (kg):")
weight_label.grid(row=1, column=0, padx=10, pady=10)

weight_entry = tk.Entry(window)
weight_entry.grid(row=1, column=1, padx=10, pady=10)

calculate_button = tk.Button(window, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, padx=5, pady=10)

result_label = tk.Label(window, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Create a canvas for the meter
canvas = tk.Canvas(window, width=200, height=200)
canvas.grid(row=4, column=0, columnspan=2)

history_button = tk.Button(window, text="History", command=show_history)
history_button.grid(row=2, column=1, padx=5, pady=10)

# Start the main loop
window.mainloop()


import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import ast

# Create root window
root = tk.Tk()
root.title("Regression Line Analyzer by Anatolie Jentimir")
root.geometry("2500x1750")

# Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(7, 5))
canvas = None

def parse_input_data(data_str):
    try:
        return ast.literal_eval(data_str)
    except Exception as e:
        messagebox.showerror("Data Error", f"Invalid data format:\n{e}")
        return []

def compute_and_plot(data):
    global canvas

    try:
        ax.clear()

        x_vals = [point[0] for point in data]
        y_vals = [point[1] for point in data]
        x_squared = [x**2 for x in x_vals]
        y_squared = [y**2 for y in y_vals]
        xy_products = [x*y for x, y in zip(x_vals, y_vals)]

        n = len(data)
        sum_x = sum(x_vals)
        sum_y = sum(y_vals)
        sum_x2 = sum(x_squared)
        sum_y2 = sum(y_squared)
        sum_xy = sum(xy_products)

        # Calculate correlation coefficient (r)
        numerator = n * sum_xy - sum_x * sum_y
        denominator = np.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
        r = numerator / denominator if denominator != 0 else 0

        # Linear regression using least squares
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        y_fit = [slope * x + intercept for x in x_vals]
        ax.plot(x_vals, y_fit, color='red', label=f"Best Fit Line: y = {slope:.3f}x + {intercept:.3f}")

        # Scatter plot
        ax.scatter(x_vals, y_vals, color='blue', s=100, label='Data Points')

        # Annotate r-value
        ax.annotate(f'r = {r:.4f}', xy=(0.05, 0.95), xycoords='axes fraction',
                    fontsize=14, backgroundcolor='white')

        ax.set_title("Linear Regression: y = mx + b", fontsize=22)
        ax.set_xlabel("x", fontsize=18)
        ax.set_ylabel("y", fontsize=18)
        ax.grid(True)
        ax.legend()

        canvas.draw()

        # Table display
        table_text = "x\t y\t x²\t y²\t xy\n"
        for x, y, x2, y2, xy in zip(x_vals, y_vals, x_squared, y_squared, xy_products):
            table_text += f"{x}\t {y}\t {x2}\t {y2}\t {xy}\n"
        table_label.config(text=table_text)

        summary_text = f"""
Σx = {sum_x}
Σy = {sum_y}
Σx² = {sum_x2}
Σy² = {sum_y2}
Σxy = {sum_xy}
n = {n}

Numerator = n * Σxy - Σx * Σy 
Denominator = √[(n * Σx² - (Σx)²) * (n * Σy² - (Σy)²)] 
Numerator = {numerator}

Denominator = {denominator:.4f}

r = {r:.4f}
"""
        summary_label.config(text=summary_text)

        # Interpretation
        if r >= 0.9:
            desc = "Very strong positive correlation"
        elif r >= 0.7:
            desc = "Strong positive correlation"
        elif r >= 0.5:
            desc = "Moderate positive correlation"
        elif r >= 0.3:
            desc = "Weak positive correlation"
        elif r > 0:
            desc = "Very weak positive correlation"
        elif r == 0:
            desc = "No correlation"
        elif r > -0.3:
            desc = "Very weak negative correlation"
        elif r > -0.5:
            desc = "Weak negative correlation"
        elif r > -0.7:
            desc = "Moderate negative correlation"
        elif r > -0.9:
            desc = "Strong negative correlation"
        else:
            desc = "Very strong negative correlation"

        interpretation_text = (
            "Correlation Coefficient Analysis:\n"
            f"r = {r:.4f}\n"
            f"Interpretation: → {desc}\n\n"
            "Understanding r:\n"
            "r = 1: Perfect positive linear correlation\n"
            "r = -1: Perfect negative linear correlation\n"
            "r = 0: No linear correlation\n\n"
            "Anatolie Jentimir, 2025"
        )
        interpretation_label.config(text=interpretation_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_data_and_plot():
    data_str = input_box.get("1.0", tk.END).strip()
    data = parse_input_data(data_str)
    if data:
        compute_and_plot(data)

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Saved", f"Plot saved to:\n{file_path}")

def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(table_label.cget("text"))
            f.write("\n")
            f.write(summary_label.cget("text"))
            f.write("\n")
            f.write(interpretation_label.cget("text"))
        messagebox.showinfo("Saved", f"Data saved to:\n{file_path}")

def exit_app():
    root.destroy()

# Layout
top_frame = tk.Frame(root, bg="#e6f0ff", padx=10, pady=5)
top_frame.pack(fill=tk.X)
tk.Label(top_frame, text="📈 Regression Line Analyzer", bg="#e6f0ff", font=("Arial", 28, "bold")).pack(side=tk.LEFT)

control_frame = tk.Frame(root, pady=10)
control_frame.pack(fill=tk.X)

tk.Label(control_frame, text="Enter (x, y) pairs as Python list of tuples:", font=("Arial", 20)).pack(anchor="w", padx=10)

input_box = tk.Text(control_frame, height=4, font=("Courier", 18), wrap=tk.NONE)
input_box.insert(tk.END, "[(2, 7), (4, 11), (5, 13), (6, 20)]")
input_box.pack(fill=tk.X, padx=10)

btn_frame = tk.Frame(control_frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🔍 Analyze", command=load_data_and_plot, font=("Arial", 20), bg="#007acc", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="💾 Save Plot", command=save_plot, font=("Arial", 20), bg="#28a745", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="📝 Save Data", command=save_data, font=("Arial", 20), bg="#ffc107", fg="black").pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="❌ Exit", command=exit_app, font=("Arial", 20), bg="#cc0000", fg="white").pack(side=tk.LEFT, padx=10)

# Main Panels
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = FigureCanvasTkAgg(fig, master=left_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

right_panel = tk.Frame(main_frame, bg="#f0f6ff", width=820, padx=30)
right_panel.pack(side=tk.RIGHT, fill=tk.Y)
right_panel.pack_propagate(0)

tk.Label(right_panel, text="📊 Data Table & Summary", font=("Helvetica", 28, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(5, 2))
table_label = tk.Label(right_panel, text="", bg="#f0f6ff", justify="left", font=("Courier", 20))
table_label.pack(pady=(0, 10), padx=5, anchor="w")

summary_label = tk.Label(right_panel, text="", bg="#f0f6ff", justify="left", font=("Courier", 20))
summary_label.pack(pady=(0, 10), padx=5, anchor="w")

tk.Label(right_panel, text="📐 Regression Formula", font=("Helvetica", 26, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(5, 2))
tk.Label(
    right_panel,
    text=(
        "r = [nΣxy - (Σx)(Σy)] / \n"
        "   √{[nΣx² - (Σx)²][nΣy² - (Σy)²]}\n\n"
        "Where:\n"
        "Σxy = sum of x*y products\n"
        "Σx² = sum of x squared\n"
        "Σy² = sum of y squared\n"
        "n = number of data pairs"
    ),
    bg="#f0f6ff", justify="left", font=("Courier", 20), fg="#2c3e50"
).pack(pady=(0, 8), padx=5, anchor="w")

interpretation_label = tk.Label(right_panel, text="", bg="#f0f6ff", justify="left", font=("Courier", 20), wraplength=750)
interpretation_label.pack(pady=(5, 10), padx=5, anchor="w")

root.mainloop()

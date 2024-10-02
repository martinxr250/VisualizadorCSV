import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from ttkthemes import ThemedTk

# Toast Notification
def show_toast(message, duration=2000):
    toast = tk.Toplevel()
    toast.overrideredirect(1)
    toast.configure(bg="#333333")
    toast.geometry(f"300x50+{root.winfo_screenwidth()//2-150}+{root.winfo_screenheight()//2-25}")
    tk.Label(toast, text=message, bg="#333333", fg="white", font=("Arial", 12)).pack(pady=10)
    toast.after(duration, toast.destroy)

# Load CSV
def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            show_toast("CSV file loaded successfully!")
            display_data(df)
        except Exception as e:
            show_toast(f"Failed to load CSV: {e}", duration=3000)

# Filter Data
def filter_data():
    if df is None:
        show_toast("No CSV file loaded", duration=3000)
        return
    
    filter_column = filter_column_entry.get()
    filter_value = filter_value_entry.get()
    
    if filter_column not in df.columns:
        show_toast(f"Column '{filter_column}' not found", duration=3000)
        return
    
    try:
        filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, na=False)]
        display_data(filtered_df)
        show_toast(f"Data filtered by '{filter_value}'", duration=3000)
    except Exception as e:
        show_toast(f"Failed to filter data: {e}", duration=3000)

# Display Data in Treeview
def display_data(dataframe):
    for widget in frame_results.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame_results, style="Custom.Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    for column in tree["columns"]:
        tree.heading(column, text=column)
        tree.column(column, anchor=tk.CENTER)

    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

# Generate Pie Chart for Gender/Género
def generate_pie_chart():
    if df is None:
        show_toast("No CSV file loaded", duration=3000)
        return
    
    gender_columns = [col for col in df.columns if col.lower() in ['gender', 'genero']]
    
    if not gender_columns:
        show_toast("No 'Gender' or 'Género' column found in the data", duration=3000)
        return
    
    gender_column = gender_columns[0]
    gender_counts = df[gender_column].value_counts()
    
    # Generate Pie Chart
    plt.figure(figsize=(5, 5))
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    plt.title(f'Distribution of {gender_column}')
    plt.show()

# Main Application
def main():
    global df, filter_column_entry, filter_value_entry, frame_results, root

    df = None
    root = ThemedTk(theme="arc")
    root.title("Visualizador de csv")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")

    # Style configuration
    style = ttk.Style()
    style.configure("Custom.Treeview", foreground="black", font=("Arial", 10))
    style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure('TButton', font=('Arial', 12), padding=10)
    
    # Frame for Load button
    frame_top = tk.Frame(root, bg="#f0f0f0")
    frame_top.pack(pady=10)

    load_button = ttk.Button(frame_top, text="📂 Load CSV File", command=load_csv)
    load_button.pack(side=tk.LEFT, padx=10)

    # Frame for Filter inputs
    frame_filter = tk.Frame(root, bg="#f0f0f0", bd=2, relief=tk.SUNKEN)
    frame_filter.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(frame_filter, text="🔍 Filter Column:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
    filter_column_entry = ttk.Entry(frame_filter, width=30, font=("Arial", 12))
    filter_column_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_filter, text="🔍 Filter Value:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    filter_value_entry = ttk.Entry(frame_filter, width=30, font=("Arial", 12))
    filter_value_entry.grid(row=1, column=1, padx=10, pady=5)

    filter_button = ttk.Button(frame_filter, text="Apply Filter", command=filter_data)
    filter_button.grid(row=2, columnspan=2, pady=10)

    # Button for Pie Chart
    pie_chart_button = ttk.Button(frame_filter, text="Generate Gender Pie Chart", command=generate_pie_chart)
    pie_chart_button.grid(row=3, columnspan=2, pady=10)

    # Frame for displaying results
    frame_results = tk.Frame(root, bg="#f0f0f0", bd=2, relief=tk.SUNKEN)
    frame_results.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()

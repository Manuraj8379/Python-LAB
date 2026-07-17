import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Blue Shades")
root.geometry("700x500")
root.configure(bg="white")

# 7 Shades of Blue
blue_shades = [
    "#E3F2FD",
    "#BBDEFB",
    "#90CAF9",
    "#64B5F6",
    "#42A5F5",
    "#1E88E5",
    "#0D47A1"
]

# Create color strips
for color in blue_shades:
    frame = tk.Frame(
        root,
        bg=color,
        height=60,
        bd=0,
        highlightthickness=0
    )
    frame.pack(fill="x", padx=10, pady=4)

# Prevent frames from shrinking
for widget in root.winfo_children():
    widget.pack_propagate(False)

# Run the application
root.mainloop()
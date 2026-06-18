import tkinter as tk


def press_key(char):
    """Appends characters to the display."""
    current = display_var.get()
    if current == "0" and char not in ".":
        display_var.set(char)
    else:
        display_var.set(current + str(char))


def clear_display():
    """Resets the calculator display."""
    display_var.set("0")


def calculate():
    """Evaluates the mathematical equation safely."""
    try:
        # Replace the visual '×' and '÷' with Python valid operators '*' and '/'
        equation = display_var.get().replace("×", "*").replace("÷", "/")
        result = eval(equation)

        # Format float numbers neatly if they end in .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        display_var.set(str(result))
    except Exception:
        display_var.set("Error")


# --- UI Configuration Constants ---
BG_COLOR = "#1C1C1E"  # Rich dark background
DISPLAY_BG = "#1C1C1E"
TEXT_COLOR = "#FFFFFF"

# Button Palette
COLOR_NUM = "#3A3A3C"  # Dark gray for numbers
COLOR_OP = "#FF9F0A"  # Vibrant Orange for operators
COLOR_FUNC = "#AEAEB2"  # Light gray for functions

# Initialize main window
root = tk.Tk()
root.title("Calculator")
root.geometry("360x540")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# String Variable to hold display text
display_var = tk.StringVar(value="0")

# --- Display Screen ---
display_frame = tk.Frame(root, bg=DISPLAY_BG)
display_frame.pack(expand=True, fill="both", padx=20, pady=(20, 10))

display_label = tk.Label(
    display_frame,
    textvariable=display_var,
    font=("Helvetica", 44),
    anchor="e",
    bg=DISPLAY_BG,
    fg=TEXT_COLOR,
    padx=10,
)
display_label.pack(expand=True, fill="both")

# --- Button Grid ---
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(fill="both", padx=15, pady=(0, 20))

# Layout blueprint: (Text, Row, Column, Span, Color, Command)
# FIXED: All numerical arguments in lambda: press_key() are now strings
buttons = [
    ("C", 0, 0, 1, COLOR_FUNC, clear_display),
    ("(", 0, 1, 1, COLOR_FUNC, lambda: press_key("(")),
    (")", 0, 2, 1, COLOR_FUNC, lambda: press_key(")")),
    ("÷", 0, 3, 1, COLOR_OP, lambda: press_key("÷")),
    ("7", 1, 0, 1, COLOR_NUM, lambda: press_key("7")),
    ("8", 1, 1, 1, COLOR_NUM, lambda: press_key("8")),
    ("9", 1, 2, 1, COLOR_NUM, lambda: press_key("9")),
    ("×", 1, 3, 1, COLOR_OP, lambda: press_key("×")),
    ("4", 2, 0, 1, COLOR_NUM, lambda: press_key("4")),
    ("5", 2, 1, 1, COLOR_NUM, lambda: press_key("5")),
    ("6", 2, 2, 1, COLOR_NUM, lambda: press_key("6")),
    ("-", 2, 3, 1, COLOR_OP, lambda: press_key("-")),
    ("1", 3, 0, 1, COLOR_NUM, lambda: press_key("1")),
    ("2", 3, 1, 1, COLOR_NUM, lambda: press_key("2")),
    ("3", 3, 2, 1, COLOR_NUM, lambda: press_key("3")),
    ("+", 3, 3, 1, COLOR_OP, lambda: press_key("+")),
    ("0", 4, 0, 2, COLOR_NUM, lambda: press_key("0")),
    (".", 4, 2, 1, COLOR_NUM, lambda: press_key(".")),
    ("=", 4, 3, 1, COLOR_OP, calculate),
]

# Configure grid row/column weights dynamically for responsive look
for i in range(5):
    btn_frame.rowconfigure(i, weight=1, minsize=75)
for i in range(4):
    btn_frame.columnconfigure(i, weight=1, minsize=75)

# Render buttons onto grid with layout adjustments
for text, row, col, span, bg, cmd in buttons:
    fg_color = "#000000" if bg == COLOR_FUNC else "#FFFFFF"

    btn = tk.Button(
        btn_frame,
        text=text,
        font=("Helvetica", 20, "bold" if bg == COLOR_OP else "normal"),
        bg=bg,
        fg=fg_color,
        activebackground=bg,
        activeforeground=fg_color,
        bd=0,
        relief="flat",
        command=cmd,
    )
    btn.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=6, pady=6)

root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# ---------- Password Logic ----------

def generate_password():
    length = length_var.get()
    use_letters = letters_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    exclude_similar = exclude_similar_var.get()
    must_include = must_include_var.get()

    if not (use_letters or use_digits or use_symbols):
        messagebox.showwarning("Selection Error", "Select at least one character type!")
        return

    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    similar_chars = "O0l1I"

    pool = ""
    if use_letters:
        pool += letters
    if use_digits:
        pool += digits
    if use_symbols:
        pool += symbols

    if exclude_similar:
        pool = ''.join(ch for ch in pool if ch not in similar_chars)

    password = []

    if must_include:
        if use_letters:
            password.append(random.choice(letters))
        if use_digits:
            password.append(random.choice(digits))
        if use_symbols:
            password.append(random.choice(symbols))

    remaining_length = length - len(password)
    password += random.choices(pool, k=remaining_length)

    random.shuffle(password)
    final_password = ''.join(password)

    password_var.set(final_password)
    update_strength(final_password)


def update_strength(pwd):
    score = 0
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in string.punctuation for c in pwd): score += 1
    if len(pwd) >= 12: score += 1

    strength = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    strength_var.set(f"Strength: {strength[score-1]}")


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")


def update_length_label(event=None):
    length_label_var.set(f"Length: {length_var.get()}")

# ---------- UI Setup ----------

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x600")
root.resizable(False, False)

# Title
title = ttk.Label(root, text="🔐 Password Generator", font=("Helvetica", 20, "bold"))
title.pack(pady=10)

# Instructions
instructions = tk.Label(
    root,
    text="Select the password options below and adjust the length.\n"
         "Click 'Generate Password' to create a secure password.\n"
         "Click 'Copy Password' to copy it to clipboard.",
    font=("Helvetica", 10),
    justify="center"
)
instructions.pack(pady=10)

# Password Display
password_var = tk.StringVar()
password_entry = ttk.Entry(root, textvariable=password_var, font=("Helvetica", 14), width=40)
password_entry.pack(pady=10)

copy_btn = ttk.Button(root, text="Copy Password", command=copy_to_clipboard)
copy_btn.pack(pady=5)

# Length Slider
length_var = tk.IntVar(value=12)
length_label_var = tk.StringVar(value=f"Length: {length_var.get()}")
length_label = ttk.Label(root, textvariable=length_label_var)
length_label.pack()

length_slider = ttk.Scale(root, from_=6, to=40, variable=length_var, orient="horizontal", command=update_length_label)
length_slider.pack(pady=5)

# Options
letters_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_similar_var = tk.BooleanVar()
must_include_var = tk.BooleanVar(value=True)

ttk.Checkbutton(root, text="Include Letters", variable=letters_var).pack(anchor='w', padx=50)
ttk.Checkbutton(root, text="Include Digits", variable=digits_var).pack(anchor='w', padx=50)
ttk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack(anchor='w', padx=50)
ttk.Checkbutton(root, text="Exclude Similar Characters (O,0,l,1,I)", variable=exclude_similar_var).pack(anchor='w', padx=50)
ttk.Checkbutton(root, text="Must include selected character types", variable=must_include_var).pack(anchor='w', padx=50)

# Strength Indicator
strength_var = tk.StringVar(value="Strength: ")
strength_label = ttk.Label(root, textvariable=strength_var, font=("Helvetica", 12, "bold"))
strength_label.pack(pady=10)

# Generate Button
generate_btn = ttk.Button(root, text="Generate Password", command=generate_password)
generate_btn.pack(pady=20)

root.mainloop()
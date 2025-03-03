import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import re
import csv

# Translation dictionary / Prekladový slovník
translations = {
    "English": {
        "title": "TextAlign UI",
        "file1_label": "File 1:",
        "file2_label": "File 2:",
        "browse_button": "Browse",
        "text1_label": "Enter text 1:",
        "text2_label": "Enter text 2:",
        "align_button": "Align Text",
        "result_label": "Result:",
        "save_button": "Save",
        "back_button": "Back",
        "error_no_text": "Enter text or load files.",
        "error_no_data": "No data to save.",
        "success_save": "Results saved successfully!",
        "language_button": "SK/EN",
        "default_text_button": "Use Default Text"
    },
    "Slovak": {
        "title": "TextAlign UI",
        "file1_label": "Súbor 1:",
        "file2_label": "Súbor 2:",
        "browse_button": "Prehľadávať",
        "text1_label": "Zadajte text 1:",
        "text2_label": "Zadajte text 2:",
        "align_button": "Zarovnať text",
        "result_label": "Výsledok:",
        "save_button": "Uložiť",
        "back_button": "Späť",
        "error_no_text": "Zadajte text alebo načítajte súbory.",
        "error_no_data": "Nie sú žiadne dáta na uloženie.",
        "success_save": "Výsledky boli úspešne uložené!",
        "language_button": "SK/EN",
        "default_text_button": "Použiť predvolený text"
    }
}

# Current language / Aktuálny jazyk
current_language = "English"

def update_ui_language():
    # Updating the interface text to the selected language / Aktualizácia textu rozhrania na vybraný jazyk
    lang = translations[current_language]
    window.title(lang["title"])
    file1_label.config(text=lang["file1_label"])
    file2_label.config(text=lang["file2_label"])
    browse_button1.config(text=lang["browse_button"])
    browse_button2.config(text=lang["browse_button"])
    text1_label.config(text=lang["text1_label"])
    text2_label.config(text=lang["text2_label"])
    align_button.config(text=lang["align_button"])
    result_label.config(text=lang["result_label"])
    save_button.config(text=lang["save_button"])
    back_button.config(text=lang["back_button"])
    language_button.config(text=lang["language_button"])
    default_text_button.config(text=lang["default_text_button"])  # Update button text

def toggle_language():
    # Switching between English and Slovak languages / Prepnúť medzi anglickým a slovenským jazykom
    global current_language
    current_language = "Slovak" if current_language == "English" else "English"
    update_ui_language()

def reopen_main_window():
    window.destroy()

def load_file(entry, text_widget):
    # Load text from a file into the entry and text widget / Načítanie textu zo súboru do poľa pre vstup a textového widgetu
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

        if file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                text = "\n".join(row[0] for row in reader if row)
        else:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text)

def split_into_sentences(text):
    # Split text into sentences / Rozdelenie textu na vety
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def align_texts():
    # Align the entered or loaded text / Zarovnanie zadaného alebo načítaného textu
    file1 = entry_file1.get()
    file2 = entry_file2.get()

    text1 = text_input1.get("1.0", tk.END).strip()
    text2 = text_input2.get("1.0", tk.END).strip()

    if file1:
        with open(file1, "r", encoding="utf-8") as f:
            text1 = f.read().strip()

    if file2:
        with open(file2, "r", encoding="utf-8") as f:
            text2 = f.read().strip()

    if not text1 or not text2:
        messagebox.showerror(translations[current_language]["error_no_text"], translations[current_language]["error_no_text"])
        return

    aligned_text = fastalign_mock(text1, text2)

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, aligned_text)

def fastalign_mock(text1, text2):
    # Improved text alignment / Vylepšené zarovnanie textu
    sentences1 = split_into_sentences(text1)
    sentences2 = split_into_sentences(text2)

    # Simple alignment by the number of sentences / Jednoduché zarovnanie podľa počtu viet
    aligned_lines = []
    for i in range(max(len(sentences1), len(sentences2))):
        s1 = sentences1[i] if i < len(sentences1) else ""
        s2 = sentences2[i] if i < len(sentences2) else ""
        aligned_lines.append(f"{s1} | {s2}")

    return "Aligned text:\n" + "\n".join(aligned_lines)

def save_results():
    # Save the alignment results / Uložiť výsledky zarovnania
    output_text = text_output.get("1.0", tk.END).strip()
    if not output_text:
        messagebox.showerror(translations[current_language]["error_no_data"],
                             translations[current_language]["error_no_data"])
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])

    if file_path:
        if file_path.endswith(".csv"):
            with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file, delimiter=";")  # Используем ";" вместо "|"
                rows = [line.split(" | ") for line in output_text.split("\n")[1:]]
                writer.writerows(rows)
        else:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(output_text)

        messagebox.showinfo(translations[current_language]["success_save"],
                            translations[current_language]["success_save"])

# Default texts for alignment / Predvolené texty na zarovnanie
DEFAULT_TEXT_1 = "The quick brown fox jumps over the lazy dog. This sentence contains all the letters of the English alphabet. It is often used for typing practice."
DEFAULT_TEXT_2 = "Rýchly hnedý líška preskočí cez lenivého psa. Táto veta obsahuje všetky písmená anglickej abecedy. Často sa používa na nácvik písania."

def insert_default_text():
    text_input1.delete("1.0", tk.END)
    text_input1.insert(tk.END, DEFAULT_TEXT_1)

    text_input2.delete("1.0", tk.END)
    text_input2.insert(tk.END, DEFAULT_TEXT_2)

# === UI Settings / Nastavenia používateľského rozhrania ===
window = tk.Tk()
window.title("TextAlign UI")
window.geometry("700x785")
window.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#0078D7", font=("Arial", 10))
style.configure("TLabel", background="#f0f0f0", font=("Arial", 11))
style.configure("TEntry", font=("Arial", 10))
style.configure("TFrame", background="#f0f0f0")

# === Main Frame / Hlavný rámec ===
main_frame = ttk.Frame(window, padding=10)
main_frame.pack(fill="both", expand=True)

# === Language switch button / Tlačidlo na prepnutie jazyka ===
language_button = ttk.Button(main_frame, text="Switch to Slovak", command=toggle_language)
language_button.pack(pady=5)

# === File Selection and Text Input / Výber súboru a vstup textu ===
file_frame = ttk.Frame(main_frame)
file_frame.pack(pady=5, fill="x")

# File / Súbor 1
file1_label = ttk.Label(file_frame, text="File 1:")
file1_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_file1 = ttk.Entry(file_frame, width=50)
entry_file1.grid(row=0, column=1, padx=5, pady=5)
browse_button1 = ttk.Button(file_frame, text="Browse", command=lambda: load_file(entry_file1, text_input1))
browse_button1.grid(row=0, column=2, padx=5, pady=5)

# File / Súbor 2
file2_label = ttk.Label(file_frame, text="File 2:")
file2_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_file2 = ttk.Entry(file_frame, width=50)
entry_file2.grid(row=1, column=1, padx=5, pady=5)
browse_button2 = ttk.Button(file_frame, text="Browse", command=lambda: load_file(entry_file2, text_input2))
browse_button2.grid(row=1, column=2, padx=5, pady=5)

# === Button to insert default text (Moved here) / Tlačidlo na vloženie predvoleného textu ===
default_text_button = ttk.Button(main_frame, text="Use Default Text", command=insert_default_text)
default_text_button.pack(pady=5)

# === Manual Text Input / Ručný vstup textu ===
text_frame = ttk.Frame(main_frame)
text_frame.pack(pady=5, fill="both", expand=True)

text1_label = ttk.Label(text_frame, text="Enter text 1:")
text1_label.pack(anchor="w", padx=5, pady=2)
text_input1 = tk.Text(text_frame, height=5, width=70, font=("Arial", 10))
text_input1.pack(fill="both", expand=True, padx=5, pady=5)

text2_label = ttk.Label(text_frame, text="Enter text 2:")
text2_label.pack(anchor="w", padx=5, pady=2)
text_input2 = tk.Text(text_frame, height=5, width=70, font=("Arial", 10))
text_input2.pack(fill="both", expand=True, padx=5, pady=5)

# === "Align" Button / Tlačidlo "Zarovnať ===
align_button = ttk.Button(main_frame, text="Align Text", command=align_texts)
align_button.pack(pady=10)

# === Output Window / Okno výstupu ===
output_frame = ttk.Frame(main_frame)
output_frame.pack(pady=5, fill="both", expand=True)

result_label = ttk.Label(output_frame, text="Result:")
result_label.pack(anchor="w", padx=5, pady=2)
text_output = tk.Text(output_frame, height=10, width=70, font=("Arial", 10))
text_output.pack(fill="both", expand=True, padx=5, pady=5)

# === "Save" and "Back" Buttons / Tlačidlá "Uložiť" a "Späť ===
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10, fill="x")

save_button = ttk.Button(button_frame, text="Save", command=save_results)
save_button.pack(side="left", padx=5)

back_button = ttk.Button(button_frame, text="Back", command=reopen_main_window)
back_button.pack(side="right", padx=5)

# Interface initialization / Inicializácia rozhrania
update_ui_language()

# Run the window / Spustiť okno
window.mainloop()

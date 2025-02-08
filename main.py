import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
import spacy
import subprocess

# Loading necessary NLTK data / Načítanie potrebných údajov NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Loading the spaCy model / Načítanie modelu spaCy
nlp = spacy.load("en_core_web_sm")

# Initialization of text processing tools / Inicializácia nástrojov na spracovanie textu
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# --- Variables for switching language / Premenné na prepínanie jazyka ---
# Dictionaries for texts in different languages / Slovníky pre texty v rôznych jazykoch
translations = {
    "English": {
        "exit": "❌",
        "toggle_language": "Switch to Slovak",
        "instructions": "Instructions: Enter text below or upload a file to begin processing.",
        "output": "Output:",
        "settings": "Settings",
        "remove_urls": "Remove URLs",
        "remove_stopwords": "Remove Stop Words",
        "tokenize": "🌀 Tokenize",
        "segment": "✂ Segment",
        "pos_tags": "📚 POS Tags",
        "normalize": "🌟 Normalize",
        "save": "💾 Save Result",
        "upload": "📂 Upload File",
        "default": "✨ Use Default Text",
        "clear_text": "🗑 Clear Text",
        "file_error": "The file could not be uploaded",
        "column_selection": "Available columns: {columns}\nEnter the name of the column to process:",
        "invalid_column": "Invalid column name.",
        "no_output_to_save": "There is no output to save.",
        "save_success": "The results are saved in {file_path}",
        "save_error": "The file could not be saved",
        "align_text": "📏 Align Text"
    },
    "Slovak": {
        "exit": "❌",
        "toggle_language": "Prepnúť na angličtinu",
        "instructions": "Pokyny: Zadajte text nižšie alebo nahrajte súbor na spracovanie.",
        "output": "Výstup:",
        "settings": "Nastavenia",
        "remove_urls": "Odstrániť URL",
        "remove_stopwords": "Odstrániť stop slová",
        "tokenize": "🌀 Tokenizácia",
        "segment": "✂ Segmentácia",
        "pos_tags": "📚 POS Tagy",
        "normalize": "🌟 Normalizácia",
        "save": "💾 Uložiť výsledok",
        "upload": "📂 Nahrať súbor",
        "default": "✨ Použiť predvolený text",
        "clear_text": "🗑 Vymazať text",
        "file_error": "Súbor sa nepodarilo nahrať",
        "column_selection": "Dostupné stĺpce: {columns}\nZadajte názov stĺpca na spracovanie:",
        "invalid_column": "Neplatný názov stĺpca.",
        "no_output_to_save": "Nie je čo uložiť.",
        "save_success": "Výsledky sú uložené v {file_path}",
        "save_error": "Súbor sa nepodarilo uložiť",
        "align_text": "📏 Zarovnať text"
    }
}

# Current language / Aktuálny jazyk
current_language = "English"

def update_ui_language():
    # Updating the interface text to the selected language / Aktualizácia textu rozhrania na vybraný jazyk
    lang = translations[current_language]
    btn_exit.config(text=lang["exit"])
    btn_toggle_language.config(text=lang["toggle_language"])
    instructions_label.config(text=lang["instructions"])
    text_output_label.config(text=lang["output"])
    settings_frame.config(text=lang["settings"])
    remove_urls_checkbox.config(text=lang["remove_urls"])
    remove_stopwords_checkbox.config(text=lang["remove_stopwords"])
    btn_tokenize.config(text=lang["tokenize"])
    btn_segment.config(text=lang["segment"])
    btn_pos_tags.config(text=lang["pos_tags"])
    btn_normalize.config(text=lang["normalize"])
    btn_save.config(text=lang["save"])
    btn_upload.config(text=lang["upload"])
    btn_default.config(text=lang["default"])
    btn_clear_text.config(text=lang["clear_text"])
    btn_align_text.config(text=lang["align_text"])
    if text_input.get("1.0", tk.END).strip() == translations["English"]["instructions"]:
        text_input.delete("1.0", tk.END)
        text_input.insert("1.0", translations[current_language]["instructions"])

def toggle_language():
    # Switching between English and Slovak languages / Prepnúť medzi anglickým a slovenským jazykom
    global current_language
    current_language = "Slovak" if current_language == "English" else "English"
    update_ui_language()

def open_align_window():
    subprocess.Popen(["python", "align_text_window.py"])

# --- Button to exit the application / Tlačidlo na výstup z aplikácie ---
def exit_application():
    window.quit()

# --- Text processing functions / Funkcie spracovania textu ---
def clean_text(text, remove_urls=False):
    if remove_urls:
        text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def tokenize_text():
    input_text = text_input.get("1.0", tk.END)
    input_text = clean_text(input_text, var_remove_urls.get())
    tokens = word_tokenize(input_text)

    if var_remove_stopwords.get():
        tokens = [token for token in tokens if token not in stop_words]

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Tokens:\n" + ", ".join(tokens))

def segment_text():
    input_text = text_input.get("1.0", tk.END)
    input_text = clean_text(input_text, var_remove_urls.get())
    sentences = sent_tokenize(input_text)

    if var_remove_stopwords.get():
        sentences = [" ".join([word for word in word_tokenize(sentence) if word not in stop_words]) for sentence in sentences]

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Sentences:\n" + "\n".join(sentences))

def pos_tags():
    input_text = text_input.get("1.0", tk.END)
    input_text = clean_text(input_text, var_remove_urls.get())
    doc = nlp(input_text)
    result = [f"{token.text}: {token.pos_}" for token in doc if token.text.strip()]
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "POS Tags:\n" + "\n".join(result))

def normalize_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        return

    input_text = clean_text(input_text)

    tokens = word_tokenize(input_text)

    tokens = [token for token in tokens if token.lower() not in stop_words]

    pos_tags = pos_tag(tokens)

    normalized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Normalized Text:\n" + " ".join(normalized_tokens))

def lemmatize_or_stem_text():
    input_text = text_input.get("1.0", tk.END)
    input_text = clean_text(input_text, var_remove_urls.get())
    technique = technique_choice.get()
    processed_tokens = []

    tokens = word_tokenize(input_text)

    if var_remove_stopwords.get():
        tokens = [token for token in tokens if token not in stop_words]

    if technique == "Lemmatization":
        doc = nlp(" ".join(tokens))
        for token in doc:
            if token.text.lower().endswith(("er", "or")):
                lemma_as_verb = token.lemma_ if token.pos_ == "VERB" else token.text.lower()
                processed_tokens.append(lemma_as_verb if lemma_as_verb != token.text.lower() else token.lemma_)
            else:
                processed_tokens.append(token.lemma_)

    elif technique == "Stemming":
        for token in tokens:
            stem = stemmer.stem(token.lower())
            if token.lower().endswith("er"):
                stem = stemmer.stem(token[:-2])
            processed_tokens.append(stem)

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, f"{technique} Result:\n" + ", ".join(processed_tokens))


def get_wordnet_pos(treebank_tag):
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    return tag_dict.get(treebank_tag[0].upper(), wordnet.NOUN)

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
            column = simpledialog.askstring(
                "Column Selection",
                translations[current_language]["column_selection"].format(columns=", ".join(data.columns))
            )
            if column not in data.columns:
                messagebox.showerror("Error", translations[current_language]["invalid_column"])
                return
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, " ".join(data[column].astype(str)))
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, file.read())
        else:
            messagebox.showerror("Error", translations[current_language]["file_error"])
    except Exception as e:
        messagebox.showerror("Error", f"{translations[current_language]['file_error']}: {e}")

def save_results():
    output_text = text_output.get("1.0", tk.END)
    if not output_text.strip():
        messagebox.showerror("Error", translations[current_language]["no_output_to_save"])
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
        ("Text files", "*.txt"),
        ("CSV files", "*.csv")
    ])
    if not file_path:
        return
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output_text)
        messagebox.showinfo("Success", translations[current_language]["save_success"].format(file_path=file_path))
    except Exception as e:
        messagebox.showerror("Error", f"{translations[current_language]['save_error']}: {e}")

def use_default_text():
    default_text = "Natural Language Processing enables machines to understand and  respond to text just like humans."
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, default_text)

# --- Button to switch language in the settings section / Tlačidlo na prepnutie jazyka v sekcii nastavení ---
def toggle_language_settings():
    toggle_language()

# Adding a button to clear the text input field / Pridanie tlačidla na vyčistenie textového poľa pre vstup
def clear_text_input():
    text_input.delete("1.0", tk.END)

# --- Creating the interface / Vytváranie rozhrania ---
window = tk.Tk()
window.title("Text Processing Application")
window.geometry("700x680")
window.configure(bg="#f0f8ff")

# Application logo / Logo aplikácie
logo_label = tk.Label(window, text="📘 Text Processor", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#4682b4")
logo_label.pack(pady=5, anchor="center")

btn_exit = tk.Button(window, text="", command=exit_application, bg="#ff6961", font=("Arial", 10))
btn_exit.place(relx=1, rely=0, anchor="ne", x=-10, y=10)

# Instructions / Inštrukcie
instructions_label = tk.Label(window, text="", bg="#f0f8ff", font=("Arial", 12))
instructions_label.pack(pady=5)

# Text input area / Oblasť pre vstup textu
text_input = tk.Text(window, height=8, width=70, wrap="word", font=("Arial", 10))
text_input.pack(pady=5)

# Buttons for loading and default text / Tlačidlá na načítanie a predvolený text
file_buttons_frame = tk.Frame(window, bg="#f0f8ff")
file_buttons_frame.pack(pady=5)

btn_upload = tk.Button(file_buttons_frame, text="", command=upload_file, bg="#add8e6", font=("Arial", 10))
btn_upload.grid(row=0, column=0, padx=5)

btn_default = tk.Button(file_buttons_frame, text="", command=use_default_text, bg="#add8e6", font=("Arial", 10))
btn_default.grid(row=0, column=1, padx=5)

btn_clear_text = tk.Button(file_buttons_frame, text="🗑 Clear Text", command=clear_text_input, bg="#ff6666", font=("Arial", 10))
btn_clear_text.grid(row=0, column=2, padx=5)

# Settings section / Sekcia nastavení
settings_frame = tk.LabelFrame(window, text="", bg="#e0ffff", font=("Arial", 12, "bold"), fg="#4682b4")
settings_frame.pack(pady=8, fill="x")

var_remove_urls = tk.BooleanVar()
remove_urls_checkbox = tk.Checkbutton(settings_frame, text="", variable=var_remove_urls, bg="#e0ffff")
remove_urls_checkbox.pack(side=tk.LEFT, padx=10)

var_remove_stopwords = tk.BooleanVar()
remove_stopwords_checkbox = tk.Checkbutton(settings_frame, text="", variable=var_remove_stopwords, bg="#e0ffff")
remove_stopwords_checkbox.pack(side=tk.LEFT, padx=10)

# Dropdown menu for selecting text processing technique / Rozbaľovacie menu na výber techniky spracovania textu
technique_choice = tk.StringVar()
technique_choice.set("None")
technique_menu = tk.OptionMenu(settings_frame, technique_choice, "None", "Lemmatization", "Stemming")
technique_menu.config(bg="#add8e6", font=("Arial", 10))
technique_menu.pack(side=tk.LEFT, padx=5)

# Raised button for switching the language / Vyvýšené tlačidlo na prepínanie jazyka
btn_toggle_language = tk.Button(settings_frame, text="", command=toggle_language_settings, bg="#add8e6", font=("Arial", 10))
btn_toggle_language.pack(side=tk.LEFT, padx=10, pady=5)

# Main buttons for processing / Hlavné tlačidlá na spracovanie
buttons_frame = tk.Frame(window, bg="#f0f8ff")
buttons_frame.pack(pady=5)

btn_tokenize = tk.Button(buttons_frame, text="", command=tokenize_text, bg="#90ee90", font=("Arial", 10))
btn_tokenize.grid(row=0, column=0, padx=5, pady=5)

btn_segment = tk.Button(buttons_frame, text="", command=segment_text, bg="#90ee90", font=("Arial", 10))
btn_segment.grid(row=0, column=1, padx=5, pady=5)

btn_pos_tags = tk.Button(buttons_frame, text="", command=pos_tags, bg="#90ee90", font=("Arial", 10))
btn_pos_tags.grid(row=0, column=2, padx=5, pady=5)

btn_process = tk.Button(buttons_frame, text="🛠 Lemmatize/Stem", command=lemmatize_or_stem_text, bg="#90ee90", font=("Arial", 10))
btn_process.grid(row=1, column=1, padx=5, pady=5)

btn_normalize = tk.Button(buttons_frame, text="", command=normalize_text, bg="#90ee90", font=("Arial", 10))
btn_normalize.grid(row=1, column=0, padx=5, pady=5)

btn_align_text = tk.Button(buttons_frame, text="📏 Align Text", command=open_align_window, bg="#90ee90", font=("Arial", 10))
btn_align_text.grid(row=1, column=2, padx=5, pady=5)

btn_save = tk.Button(buttons_frame, text="", command=save_results, bg="#add8e6", font=("Arial", 10))
btn_save.grid(row=2, column=1, padx=5, pady=10)

# Text output area / Oblasť pre výstup textu
text_output_label = tk.Label(window, text="", font=("Arial", 12, "bold"), bg="#f0f8ff")
text_output_label.pack(pady=5)

text_output = tk.Text(window, height=10, width=70, wrap="word", font=("Arial", 10), state="normal")
text_output.pack(pady=5)

# Launching the application / Spustenie aplikácie
update_ui_language()
window.mainloop()
import os
import sys
from tkinter import Tk, Button, filedialog, Label, messagebox, ttk, Entry
from tkinter import font as tkFont
from PIL import Image, ImageTk

# Функция для получения правильного пути к файлу
def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает для dev и для PyInstaller."""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Функция для обработки текстур _d
def process_d_texture(img, base_name, output_dir, postfixes):
    r, g, b, a = img.split()
    
    # Create Albedo map
    albedo_postfix = postfixes["albedo"]
    albedo = Image.merge('RGB', (r, g, b))
    albedo_path = os.path.join(output_dir, base_name.replace('_d', albedo_postfix) + '.png')
    albedo.save(albedo_path)
    
    # Create AO map from alpha channel
    ao_postfix = postfixes["ao"]
    ao = Image.merge('RGB', (a, a, a))
    ao_path = os.path.join(output_dir, base_name.replace('_d', ao_postfix) + '.png')
    ao.save(ao_path)

# Функция для обработки текстур _n
def process_n_texture(img, base_name, output_dir, postfixes):
    r, g, b, a = img.split()
    white = Image.new('L', img.size, 255)
    
    # Normal map: R=Alpha, G=G, B=255
    normal_postfix = postfixes["normal"]
    normal = Image.merge('RGB', (a, g, white))
    normal_path = os.path.join(output_dir, base_name.replace('_n', normal_postfix) + '.png')
    normal.save(normal_path)
    
    # Roughness map from Red channel
    roughness_postfix = postfixes["roughness"]
    roughness = Image.merge('RGB', (r, r, r))
    roughness_path = os.path.join(output_dir, base_name.replace('_n', roughness_postfix) + '.png')
    roughness.save(roughness_path)
    
    # Metal map from Blue channel
    metal_postfix = postfixes["metal"]
    metal = Image.merge('RGB', (b, b, b))
    metal_path = os.path.join(output_dir, base_name.replace('_n', metal_postfix) + '.png')
    metal.save(metal_path)

# Обработка текстур
def process_textures(input_dir, output_dir, progress_bar, status_label, postfixes):
    os.makedirs(output_dir, exist_ok=True)
    
    dds_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.dds')]
    total_files = len(dds_files)
    
    if total_files == 0:
        messagebox.showwarning("Warning", "No .dds files found in the selected folder.")
        return
    
    progress_bar['maximum'] = total_files
    progress_bar['value'] = 0
    status_label.config(text="Processing textures...")
    
    for i, filename in enumerate(dds_files):
        base_name = os.path.splitext(filename)[0]
        input_path = os.path.join(input_dir, filename)
        
        try:
            img = Image.open(input_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {filename}: {str(e)}")
            continue
        
        if base_name.endswith('_d'):
            process_d_texture(img, base_name, output_dir, postfixes)
        elif base_name.endswith('_n'):
            process_n_texture(img, base_name, output_dir, postfixes)
        
        progress_bar['value'] = i + 1
        progress_bar.update()
        status_label.config(text=f"Processed {i + 1}/{total_files} textures...")
    
    status_label.config(text="Conversion completed!")
    messagebox.showinfo("Success", f"Textures converted and saved to:\n{output_dir}")

# GUI setup
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        # Получаем выбранные постфиксы из полей ввода
        postfixes = {
            "albedo": albedo_entry.get(),
            "ao": ao_entry.get(),
            "normal": normal_entry.get(),
            "roughness": roughness_entry.get(),
            "metal": metal_entry.get()
        }
        
        output_folder = os.path.join(folder, 'converted_textures')
        
        progress_window = Tk()
        progress_window.title("Conversion Progress")
        progress_window.geometry("400x150")
        progress_window.configure(bg="#1e1e1e")  # фон окна
        
        status_label = Label(progress_window, text="Starting conversion...", 
                             font=("Arial", 12), bg="#1e1e1e", fg="#cccccc")
        status_label.pack(pady=10)
        
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("Custom.Horizontal.TProgressbar", background="#007acc", troughcolor="#1e1e1e")
        
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate",
                                       style="Custom.Horizontal.TProgressbar")
        progress_bar.pack(pady=10)
        
        process_textures(folder, output_folder, progress_bar, status_label, postfixes)
        progress_window.destroy()

# Главное окно
root = Tk()
root.title("Dagor Engine Textures Converter")
root.geometry("600x530")
root.configure(bg="#1e1e1e")  # фон

# Загрузка пользовательского шрифта
try:
    custom_font_path = os.path.join(os.path.dirname(__file__), "MyFont.ttf")
    custom_font = tkFont.Font(family="RodchenkoCTT", size=12)
    custom_font2 = tkFont.Font(family="RodchenkoCTT", size=24)
except Exception as e:
    print(f"Failed to load custom font: {e}")
    custom_font = ("Arial", 12)  # Запасной шрифт
    custom_font2 = ("Arial", 24)

# Load logo
try:
    logo_path = resource_path("ui/logo.ico")
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((64, 64))
    logo_photo = ImageTk.PhotoImage(logo_image)
except Exception as e:
    print(f"Failed to load logo: {e}")
    logo_photo = None 

icon_photo = ImageTk.PhotoImage(logo_image)
root.iconphoto(False, icon_photo)

# Add logo label
logo_label = Label(root, image=logo_photo, bg="#1e1e1e")
logo_label.image = logo_photo
logo_label.pack(pady=10)

# Title label
title_label = Label(root, text="Dagor Engine Textures Converter", font=custom_font2, bg="#1e1e1e", fg="#cccccc")
title_label.pack(pady=10)

# Description label
desc_label = Label(root, text="Select a folder with .dds textures to convert them.\n"
                              "Output textures will use the specified postfixes below.", 
                   font=("Arial", 12), bg="#1e1e1e", fg="#cccccc", justify="left")
desc_label.pack(pady=5)

# Постфиксы по умолчанию
default_postfixes = {
    "albedo": "_Albedo",
    "ao": "_AO",
    "normal": "_Normal",
    "roughness": "_Roughness",
    "metal": "_Metal"
}

# Настройка полей ввода для постфиксов
Label(root, text="Albedo Postfix:", font=("Arial", 12), bg="#1e1e1e", fg="#cccccc").pack()
albedo_entry = Entry(root, font=("Arial", 12), width=20)
albedo_entry.insert(0, default_postfixes["albedo"])
albedo_entry.pack()

Label(root, text="AO Postfix:", font=("Arial", 12), bg="#1e1e1e", fg="#cccccc").pack()
ao_entry = Entry(root, font=("Arial", 12), width=20)
ao_entry.insert(0, default_postfixes["ao"])
ao_entry.pack()

Label(root, text="Normal Postfix:", font=("Arial", 12), bg="#1e1e1e", fg="#cccccc").pack()
normal_entry = Entry(root, font=("Arial", 12), width=20)
normal_entry.insert(0, default_postfixes["normal"])
normal_entry.pack()

Label(root, text="Roughness Postfix:", font=("Arial", 12), bg="#1e1e1e", fg="#cccccc").pack()
roughness_entry = Entry(root, font=("Arial", 12), width=20)
roughness_entry.insert(0, default_postfixes["roughness"])
roughness_entry.pack()

Label(root, text="Metal Postfix:", font=("Arial", 12), bg="#1e1e1e", fg="#cccccc").pack()
metal_entry = Entry(root, font=("Arial", 12), width=20)
metal_entry.insert(0, default_postfixes["metal"])
metal_entry.pack()

# Select folder button
btn_select = Button(root, text="Select Folder", command=select_folder, 
                    font=custom_font, bg="#007acc", fg="white", padx=10, pady=5, relief="flat")
btn_select.pack(pady=20)

# Signature label
#signature_label = Label(root, text="Created by Shemich 2025", 
#                         font=("Arial", 10, "italic"), bg="#1e1e1e", fg="#888888")
#signature_label.pack(side="bottom", pady=10)

root.mainloop()
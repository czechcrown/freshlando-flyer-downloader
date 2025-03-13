import subprocess
import sys
import tkinter as tk
import tkinter.simpledialog
from PIL import Image
from fpdf import FPDF
import os
import requests

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
    import PIL
    import fpdf
except ImportError:
    install('requests')
    install('Pillow')
    install('fpdf')

def download_flyer(kod_zeme, cislo_combined, pocet_stranek, nazev_pdf):
    cislo_data, cislo = cislo_combined.split('/')
    base_url = f"https://eu.freshlandocdns.com/{kod_zeme}/data/{cislo_data}/{cislo}/"
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i in range(pocet_stranek):
        image_url = f"{base_url}{i}.webp"
        response = requests.get(image_url)
        if response.status_code == 200:
            image_path = f"temp_{i}.webp"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            image = Image.open(image_path)
            jpeg_path = f"temp_{i}.jpg"
            image = image.convert('RGB')
            image.save(jpeg_path, 'JPEG')

            # Resize image to fit PDF page
            pdf.add_page()
            pdf_w, pdf_h = pdf.w - 20, pdf.h - 20
            img_w, img_h = image.size
            ratio = min(pdf_w/img_w, pdf_h/img_h)
            new_width, new_height = int(img_w * ratio), int(img_h * ratio)
            pdf.image(jpeg_path, x=10, y=10, w=new_width, h=new_height)

            # Remove temporary files
            os.remove(image_path)
            os.remove(jpeg_path)
        else:
            print(f"Image {image_url} not found.")

    # Save PDF file with user-defined name
    pdf.output(f"{nazev_pdf}.pdf")
    print(f"PDF file '{nazev_pdf}.pdf' created.")

def get_user_input(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = tk.simpledialog.askstring("Input", prompt)
    root.destroy()
    return user_input

# Example usage
if __name__ == "__main__":
    kod_zeme = get_user_input("Enter ISO 3166-1 alpha-2 code:")
    cislo_combined = get_user_input("Enter code of flyer:")
    pocet_stranek = int(get_user_input("Enter number of pages:"))
    nazev_pdf = get_user_input("Enter pdf name:")

    download_flyer(kod_zeme, cislo_combined, pocet_stranek, nazev_pdf)

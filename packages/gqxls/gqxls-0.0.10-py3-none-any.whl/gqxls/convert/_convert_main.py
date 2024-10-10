import fitz, os
from PIL import Image
from PyPDF2 import PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import shutil
class convert_main:
    def signal_pdf_to_image(self,pdf_path: str,image_path:str,image_page:int,image_name:str,dpi:int):
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(image_page)
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image_file = os.path.join(image_path, f"{image_name}.png")
        pil_image.save(image_file, dpi=(dpi, dpi))

    def convert_image_to_pdf(self,image_path:str, output_pdf_path:str,title:str):
        img = Image.open(image_path)
        img_width, img_height = img.size
        a4_width, a4_height = A4
        if img_width > img_height:
            width, height = a4_height, a4_width
        else:
            width, height = a4_width, a4_height
        c = canvas.Canvas(os.path.join(output_pdf_path,title), pagesize=(width, height))
        scale = min(width / img_width, height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        x = (width - new_width) / 2
        y = (height - new_height) / 2
        c.drawImage(image_path, x, y, new_width, new_height, preserveAspectRatio=True)
        c.save()

    def merge_pdf(self,tem_path:str, convert_path:str, title:str):
        name = os.listdir(tem_path)
        name.sort(key=lambda x: (int(x.split('.')[0])), reverse=False)
        for i in range(len(name)):
            name[i] = os.path.join(tem_path, name[i])
        merger = PdfMerger()
        for file in name:
            reader = PdfReader(file)
            merger.append(reader)
        merger.write(os.path.join(convert_path, title))
        merger.close()
        shutil.rmtree('tem_path')
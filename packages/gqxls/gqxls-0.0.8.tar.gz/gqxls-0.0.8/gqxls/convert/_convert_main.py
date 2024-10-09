import fitz, os
from PIL import Image
class convert_main:
    def signal_pdf_to_image(self,pdf_path: str,image_path:str,image_page:int,image_name:str,dpi:int):
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(image_page)
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image_file = os.path.join(image_path, f"{image_name}.png")
        pil_image.save(image_file, dpi=(dpi, dpi))
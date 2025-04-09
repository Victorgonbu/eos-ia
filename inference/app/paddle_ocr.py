from paddleocr import PaddleOCR
import base64
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes
import numpy as np

class PaddleOcr:
    def __init__(self, use_gpu=True):
        # You can add other params like det=False, use_angle_cls=False if not needed
        self.ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=use_gpu)

    def run_ocr(self, image_base64=None, pdf_base64=None):
        images = []

        if image_base64:
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data)).convert("RGB")
            images.append(np.array(image))

        elif pdf_base64:
            pdf_data = base64.b64decode(pdf_base64)
            pil_images = convert_from_bytes(pdf_data)
            images = [np.array(img.convert("RGB")) for img in pil_images]

        else:
            raise ValueError("Either image_base64 or pdf_base64 must be provided")

        # Run OCR on each image
        all_text = []
        for img in images:
            results = self.ocr.ocr(img)
            for line in results[0]:
                all_text.append(line[1][0])  # Extract text only

        return " ".join(all_text)

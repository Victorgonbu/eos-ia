import base64
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes
import numpy as np
from docling.document_converter import DocumentConverter
import tempfile
import os
import docling

class PaddleOcr:
    def __init__(self, use_gpu=True):
        # Initialize the DocumentConverter
        docling.utils.model_downloader.download_models()
        self.converter = DocumentConverter()

    def run_ocr(self, image_base64=None, pdf_base64=None):
        temp_image_paths = []

        try:
            if image_base64:
                # Decode and save the image as a temporary file
                image_data = base64.b64decode(image_base64)
                image = Image.open(BytesIO(image_data)).convert("RGB")
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                image.save(temp_file.name)
                temp_image_paths.append(temp_file.name)

            elif pdf_base64:
                # Decode and save each page of the PDF as a temporary file
                pdf_data = base64.b64decode(pdf_base64)
                pil_images = convert_from_bytes(pdf_data)
                for img in pil_images:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                    img.save(temp_file.name)
                    temp_image_paths.append(temp_file.name)

            else:
                raise ValueError("Either image_base64 or pdf_base64 must be provided")

            # Run OCR on each temporary image file
            all_text = []
            print(temp_image_paths)
            for image_path in temp_image_paths:
                results = self.converter.convert(image_path)
                all_text.append(results.document.export_to_markdown())

            return " ".join(all_text)

        finally:
            # Clean up temporary files
            for temp_path in temp_image_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
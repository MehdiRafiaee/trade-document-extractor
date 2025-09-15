
from paddleocr import PaddleOCR
import cv2
import numpy as np
from PIL import Image
import pdf2image
import os

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='fa')
    
    def extract_text_from_image(self, image_path):
        """
        استخراج متن از تصویر
        """
        try:
            result = self.ocr.ocr(image_path, cls=True)
            full_text = ""
            
            for line in result:
                if line and line[0]:
                    for word_info in line:
                        text = word_info[1][0]
                        confidence = word_info[1][1]
                        if confidence > 0.5: # فقط کلمات با اطمینان بالا
                            full_text += text + " "
            
            return full_text.strip()
        except Exception as e:
            print(f"خطا در پردازش OCR: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path):
        """
        استخراج متن از PDF
        """
        try:
            # تبدیل PDF به تصویر
            images = pdf2image.convert_from_path(pdf_path)
            all_text = ""
            
            for i, image in enumerate(images):
                image_path = f"temp_page_{i}.jpg"
                image.save(image_path, "JPEG")
                page_text = self.extract_text_from_image(image_path)
                all_text += page_text + "\n\n"
                os.remove(image_path) # حذف فایل موقت
            
            return all_text
        except Exception as e:
            print(f"خطا در پردازش PDF: {e}")
            return ""
    
    def process_document(self, file_path):
        """
        پردازش سند بر اساس نوع فایل
        """
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self.extract_text_from_image(file_path)
        elif file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        else:
            raise ValueError("فرمت فایل پشتیبانی نمی‌شود")

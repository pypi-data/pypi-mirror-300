from datetime import datetime
import time
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import docx
import json
import boto3
from typing import Union
from io import BytesIO
import httpx

# import pytesseract
from PIL import Image


# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\augusto.lorencatto\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def check_file_type(file_bytes: bytes) -> str:
    # Verifica se é um PDF
    if file_bytes.startswith(b'%PDF-'):
        return "pdf"
    
    # Verifica se é um DOCX (arquivos DOCX são ZIP)
    if file_bytes.startswith(b'PK\x03\x04'):
        return "docx"
    
    return "Unknown file type"

def extract_pdf_to_text(doc_bytes : bytes) -> Union[str,str]:

    pdf_stream = BytesIO(doc_bytes)
    reader = PdfReader(pdf_stream)

    conversion_process = "raw_pdf"
    
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

    # TODO : Só falta tratar .pdf de imagem
    if len(text) < 100:
        raise Exception("Can't extract info from .pdf")
    
    return text,conversion_process

    # with open(file_path, 'rb') as file:
    #     reader = PdfReader(file)

    #     file_name : str = file_path.split("/")[-1]

    #     conversion_process = "raw_pdf"
    #     text = ''
    #     for page_num in range(len(reader.pages)):
    #         page = reader.pages[page_num]
    #         text += page.extract_text()

    #     if len(text) < 100:
    #         raise Exception("Can't extract text from .pdf with only images")

    #         # TODO : Implement
    #         # print("Converting all pages to images...")
    #         # conversion_process = "pdf_to_image"

    #         # #
    #         # poppler_path=r"T:\libs\poppler\Library\bin"

    #         # #
    #         # images = convert_from_path(file_path,poppler_path=poppler_path)

    #         # for i in range(len(images)):

    #         #     text_extracted = pytesseract.image_to_string(images[i])
    #         #     text += text_extracted

    # return text,conversion_process

def extract_docx_to_text(doc_bytes : bytes) -> str:
    stream = BytesIO(doc_bytes)

    doc = docx.Document(stream)

    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def doc_url_to_bytes(url) -> bytes:
    try:

        response = httpx.get(url,verify=False)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# TODO
def extract_text_from_image_using_textract(image : bytes) -> str:
    textract_client = boto3.client('textract')

    response = textract_client.detect_document_text(
        Document={'Bytes': image}
    )

    extracted_text = ''.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])

    return extracted_text
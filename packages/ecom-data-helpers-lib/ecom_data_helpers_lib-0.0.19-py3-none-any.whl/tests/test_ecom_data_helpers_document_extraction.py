import pytest
import unittest
import os
from moto import mock_aws

from ecom_data_helpers.document_extraction import (
    extract_docx_to_text,
    extract_pdf_to_text,
    check_file_type,
    extract_text_from_image_using_textract
)


class TestEcomDataHelpersDocumentExtraction(unittest.TestCase):

    def setUp(self):

        self.ROOT_DIR =  os.path.dirname(os.path.abspath(__file__))

    def test_extract_docx_to_text_with_sucess(self):

        filepath : str = self.ROOT_DIR + "/data/exemplo.docx"
        with open(filepath, 'rb') as file: 
            text : str = extract_docx_to_text(doc_bytes=file.read())

            assert len(text) > 100

    def test_extract_pdf_to_text_with_sucess(self):
        
        filepath : str = self.ROOT_DIR + "/data/exemplo.pdf"

        with open(filepath, 'rb') as file: 
            text,conversion_process = extract_pdf_to_text(doc_bytes=file.read())

            assert len(text) > 100
            assert conversion_process == 'raw_pdf'

    def test_extract_pdf_to_text_with_error(self):

        filepath : str = self.ROOT_DIR + "/data/exemplo_pdf_imagem.pdf"

        with open(filepath, 'rb') as file: 

            with pytest.raises(Exception, match="Can't extract info from .pdf"):
                extract_pdf_to_text(doc_bytes=file.read())

    def test_check_file_type_pdf_with_sucess(self):

        # Arrange
        filepath : str = self.ROOT_DIR + "/data/exemplo.pdf"

        # Act
        with open(filepath, 'rb') as file: 
            file_type : str = check_file_type(file_bytes=file.read())

            # Assert
            assert file_type == 'pdf'

    def test_check_file_type_docx_with_sucess(self):

        # Arrange
        filepath : str = self.ROOT_DIR + "/data/exemplo.docx"

        # Act
        with open(filepath, 'rb') as file: 
            file_type : str = check_file_type(file_bytes=file.read())

            # Assert
            assert file_type == 'docx'

    # TODO : Faze sentido testar um serviço externo?
    # @mock_aws
    # def test_extract_text_from_image_using_textract_with_sucess(self):

    #     # Arrange
    #     filepath : str = self.ROOT_DIR + "/data/exemplo-imagem.jpg"

    #     # Act
    #     with open(filepath, 'rb') as file: 
            
    #         file_bytes : bytes = file.read()

    #         extracted_text : str = extract_text_from_image_using_textract(
    #             image=file_bytes
    #         )

    #         # print(extracted_text)

    #         # Assert
    #         assert type(file_bytes) == bytes
    #         assert type(extracted_text) == str


        




if __name__ == "__main__":
    unittest.main()
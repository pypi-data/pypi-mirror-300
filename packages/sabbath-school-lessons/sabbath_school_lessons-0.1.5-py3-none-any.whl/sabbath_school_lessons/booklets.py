import PyPDF2
from PyPDF2 import Transformation
import os
import tempfile

class booklets:
    def __init__(self):
        pass 

    def add_padding_pages(self, input_pdf_path, pages_per_leaf):
        # Open the existing PDF file
        with open(input_pdf_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            num_pages = len(reader.pages)

            # Calculate how many blank pages to add
            pages_per_sheet = pages_per_leaf * 2
            pages_to_add = (pages_per_sheet - (num_pages % pages_per_sheet)) % pages_per_sheet

            # Create a PdfWriter object to write the new PDF
            writer = PyPDF2.PdfWriter()

            # Add existing pages
            for page in reader.pages:
                writer.add_page(page)

            # Add blank pages if necessary
            for _ in range(pages_to_add):
                writer.add_blank_page()

            # Create a temporary file for the padded PDF
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file_path = temp_file.name

            # Write the new PDF to the temporary file
            with open(temp_file_path, 'wb') as output_file:
                writer.write(output_file)

            return temp_file_path 

    
    def A5_on_A4(self, input_pdf_path):
        temp_pdf_path = self.add_padding_pages(input_pdf_path, pages_per_leaf=2)
        base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
        directory = os.path.dirname(input_pdf_path)
        
        # Set new name with path
        output_pdf_path = os.path.join(directory, f"{base_name}_A5_on_A4_booklet.pdf")
        # Open the existing PDF file
        with open(temp_pdf_path, 'rb') as input_file: # open the temporary file
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            writer_tmp = PyPDF2.PdfWriter()
            num_pages = len(reader.pages)

            order = []
            for i in range((num_pages + 1) // 2):
                if i % 2 == 0:
                    order.append((num_pages - i, i + 1))  # (last, first)
                else:
                    order.append((i + 1, num_pages - i))  # (first, last)

            a4_width = 842  # A4 width in points # landscape
            a4_height = 595  # A4 height in points

            for left_page_index, right_page_index in order:
                combined_page = writer_tmp.add_blank_page(width=a4_width, height=a4_height)  # A4 landscape dimensions

                # Merge left page (right column)
                if left_page_index <= num_pages:
                    page_left = reader.pages[left_page_index - 1]  # -1 for 0-indexing
                    combined_page.merge_page(page_left)

                # Merge right page (left column)
                if right_page_index <= num_pages:
                    page_right = reader.pages[right_page_index - 1]  # -1 for 0-indexing
                    right_page = writer_tmp.add_blank_page(width=a4_width, height=a4_height)
                    right_page.merge_page(page_right)
                    transformation = Transformation().translate(a4_width/2, 0)  # Move the second page to the right
                    right_page.add_transformation(transformation)
                    combined_page.merge_page(right_page)
                
                
                writer.add_page(combined_page)

            # Write the combined pages to a new PDF file
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
        os.remove(temp_pdf_path)
import re
from io import BytesIO
import copy
import tempfile
import os
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import letter, A5
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus import ListFlowable, ListItem, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, LineStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
import markdown as markdown_
from reportlab.platypus import Flowable
from PyPDF2 import PdfReader
from PIL import Image as PILImage

# Register fonts
module_dir = os.path.dirname(__file__)
font_path = os.path.join(module_dir, 'fonts', 'Arial-Bold.ttf')
pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
from . import translations
from .flowables import *

class CustomTemplate1(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        self.allowSplitting = 0
        self.toc = TableOfContents()
        self.toc.levelStyles = [
            ParagraphStyle(name='TOCEntry1',
                            fontSize=10,
                            fontName='Arial',
                            leftIndent=20,
                            firstLineIndent=-20,
                            spaceBefore=3,
                            leading=16)
        ]
        self.toc_page_count = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, LessonHeader):
            text = flowable.title
            lesson_num = flowable.lesson_num
            bible_text = flowable.bible_text
            date_range = flowable.date_range
            key = f'lesson-{lesson_num}'
            self.canv.bookmarkPage(key)
            spaces = ".\t" if int(lesson_num) >= 10 else '.\t'
            entry = f"{lesson_num}{spaces}{translations.custom_title_case(text)} — {date_range} ({bible_text})"
            self.notify('TOCEntry', (0, entry, self.page, key))


# some quarters have more than 1 lesson_number
class markdown_to_pdf:
    def __init__(self, input_file, lesson_number=1, lesson_header_color=colors.red, lang="en", start_date=None, lesson_title="Provide a title", copyrightowner="Gospel Sounders", quarter="Quarter 4, 2024", lesson_book=None):
        self.lesson_title = lesson_title
        directory = os.path.dirname(input_file)
        output_file_name = self.generate_file_name(quarter, lesson_number)
        output_file = os.path.join(directory, f"{output_file_name}.pdf")
        self.input_file = input_file
        self.output_file = output_file
        self.lesson_header_color = lesson_header_color
        self.lang = lang
        self.start_date = start_date
        if start_date:
            self.start_date = datetime.strptime(start_date, "%B %d, %Y")
        self.copyrightowner = copyrightowner
        self.quarter = quarter
        
        self.lesson_book = lesson_book
        
        self.page_size = A5
        self.rightMargin = 40
        self.leftMargin = 40
        self.topMargin = 20
        self.bottomMargin = 20
        self.page_numbers = {}

        self.month_translations = translations.months

    def get_lesson_month(self, quarter):
        
        # Map quarters to the start month
        quarter_months = {
            "Quarter 1": 1,   # January
            "Quarter 2": 4,   # April
            "Quarter 3": 7,   # July
            "Quarter 4": 10    # October
        }
        return quarter_months.get(quarter, None)
    

    def generate_file_name(self, quarter, lesson_number):
        def get_year_from_quarter(quarter_str):
            match = re.search(r',\s*(\d{4})', quarter_str)
            if match:
                return int(match.group(1))
            raise ValueError("Year not found in the provided quarter string.")
        # Get the lesson month from the quarter
        lesson_month = self.get_lesson_month(quarter.split(",")[0])
        if lesson_month is None:
            raise ValueError("Invalid quarter provided.")
        year = get_year_from_quarter(quarter)

        # Extract numeric quarter value
        match = re.search(r'Quarter\s*(\d)', quarter)
        if match:
            quarter_number = int(match.group(1))
        else:
            raise ValueError("Quarter number not found.")

        # Format the file name
        return f"SSL{year}{lesson_month:02d}{lesson_number:02d}-{quarter_number:02d}-{self.lesson_title.upper().replace(' ', '_')}"
        # self.process()
    def pre_process(self):
        self.process(True)
        return self
    def process(self, is_buffer=False):
        if is_buffer:
            self.read_markdown()
            self.parse_content()
            self.parse_sections()
        self.generate_pdf(is_buffer=is_buffer)
        return self

    def read_markdown(self):
        with open(self.input_file, 'r', encoding='utf-8') as file:
            self.markdown_text = file.read()
        self.html = markdown_.markdown(self.markdown_text)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def create_first_page_content(self):
        title = self.lesson_title
        subtitle = self.quarter
        lesson_book = self.lesson_book
        current_year = datetime.now().year
        copyright_info = f"© {current_year} {self.copyrightowner}. All rights reserved."
        width = self.doc.width*0.9  # Width of the canvas area
        height = self.doc.height*0.9  # Height of the canvas area
        
        # self.intro_content.insert(0,PageBreak())
        # self.intro_content.insert(0,FirstPageRender(title, subtitle, copyright_info, width, height, title_color=colors.red, copyright_color=colors.gray))

        self.intro_content = [
            
            FirstPageRender(title, subtitle, copyright_info, width, height, title_color=colors.red, copyright_color=colors.gray,lesson_book=lesson_book, lang=self.lang),
            PageBreak()
        ] + self.intro_content

    def parse_content(self):
        self.styles = getSampleStyleSheet()
        self.stylesheet = getSampleStyleSheet()
        self.setup_styles()
        
        self.story = []
        self.intro_content = []
        self.main_content = []
        self.first_dated_section_found = False

    def setup_styles(self):
        self.subparagraph_style = self.stylesheet['BodyText']
        self.subparagraph_style.fontSize = 10
        self.subparagraph_style.leading = 12
        self.subparagraph_style1 = self.stylesheet['BodyText']
        self.subparagraph_style1.fontSize = 10
        self.subparagraph_style1.leading = 12
        self.subparagraph_style1.alignment = TA_JUSTIFY
        self.subparagraph_style11 = self.stylesheet['BodyText']
        self.subparagraph_style11.fontSize = 11
        self.subparagraph_style11.leading = 12
        self.subparagraph_style11.alignment = TA_JUSTIFY
        self.subparagraph_style11.spaceAfter = 5
        self.subparagraph_style11.spaceBefore = 1
        self.styles.add(ParagraphStyle(name='TOC_Entry', 
                                fontSize=12, 
                                fontName='Arial',
                                leftIndent=0,
                                firstLineIndent=-20,
                                alignment=TA_JUSTIFY,
                                spaceAfter=2))
        self.styles.add(ParagraphStyle(name='JustifiedBody',
                                fontSize=11,
                                fontName='Arial',
                                alignment=TA_JUSTIFY,
                                spaceAfter=10,
                                spaceBefore=0))
        self.styles.add(ParagraphStyle(name='JustifiedBodySmallSpacing',
                                fontSize=11,
                                fontName='Arial',
                                alignment=TA_JUSTIFY,
                                spaceAfter=1,
                                spaceBefore=0))
        self.styles.add(LineStyle(name='Bold', fontName='Helvetica-Bold', fontSize=12))
        self.styles.add(ParagraphStyle(name='CenteredHeading3', fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceBefore=10, spaceAfter=10))
        self.styles.add(ParagraphStyle(name='CenteredHeading4', fontName='Helvetica-Bold', fontSize=11, alignment=1, spaceAfter=10))
        self.styles.add(ParagraphStyle(name='CenteredHeading5', fontName='Helvetica-Bold', fontSize=10, alignment=1, spaceAfter=10))

    def parse_sections(self):
        sections = self.soup.find_all('h2')
        for section in sections:
            lesson_title = translations.translations["lesson_title"][self.lang]
            match = re.match(rf'{lesson_title} (\d+)[^A-Za-z]+(.*)', section.text, flags=re.IGNORECASE)
            if match:
                self.parse_lesson_section(section, match)
                pass
            else:
                self.parse_non_lesson_section(section)

    def parse_lesson_section(self, section, match):
        lesson_num, title = match.groups()
        title_in_document = title
        title = title.rstrip(".,!?;:'\"").title()

        date, bible_text = self.extract_date_and_bible_text(section, lesson_num)
        
        if self.first_dated_section_found:
            self.add_lesson_content(lesson_num, date, bible_text, title_in_document, section)
        else:
            self.add_intro_content(title, section)

    def extract_date_and_bible_text(self, section, lesson_num):
        date = None
        bible_text = None
        next_element = section.find_next_sibling()
        while next_element:
            if next_element.name == 'h2':
                break
            if next_element.name == 'p':
                if self.lang == "en":
                    date_match = re.search(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b', next_element.text)
                elif self.lang == "swa":
                    date_match = re.search(r'\b(?:Januari|Februari|Machi|Aprili|Mei|Juni|Julai|Agosti|Septemba|Octoba|Novemba|Desemba)\s+\d{1,2},\s+\d{4}\b', next_element.text)
                if date_match:
                    date = date_match.group()
                    if self.start_date:
                        lesson_date = self.start_date + timedelta(days=(int(lesson_num) - 1) * 7)
                        formatted_date = lesson_date.strftime("%B %d, %Y")
                    else:
                        formatted_date = date
                    
                    if self.lang in self.month_translations:
                        month_name = formatted_date.split()[0]
                        translated_month = self.month_translations[self.lang].get(month_name, month_name)
                        formatted_date = formatted_date.replace(month_name, translated_month)

                    self.first_dated_section_found = True
                    bible_text = next_element.text.replace(date, '').strip()
                    bible_text = bible_text.replace('(', '').replace(')', '').rstrip('.!?;:,')
                    if not bible_text.strip():
                        bible_text = None
                    next_element.decompose()
                    break
            next_element = next_element.find_next_sibling()
        return formatted_date if date else None, bible_text

    def add_lesson_content(self, lesson_num, date, bible_text, title_in_document, section):
        if date:
            width_extra = 0 if int(lesson_num) < 10 else 0.1
            self.main_content.append(LessonHeader(lesson_num, date, bible_text, title_in_document, 7*inch, 20, self.lesson_header_color, width_extra=width_extra, lang=self.lang))
            self.main_content.append(Spacer(1, 0.2*inch))
        else:
            lesson_text = translations.get_lesson_text(self.lang, case="upper")
            self.main_content.append(Paragraph(f"{lesson_text} {lesson_num}. — {title_in_document}", self.styles['Heading2']))
            self.main_content.append(Paragraph(f"{date}", self.styles['Normal']))
            self.main_content.append(Paragraph(f"{bible_text}", self.styles['Normal']))

        self.parse_lesson_content(section)
        self.main_content.append(PageBreak())

    def parse_lesson_content(self, section):
        next_element = section.find_next_sibling()
        while next_element and next_element.name != 'h2':
            if next_element.name == 'ol':
                self.parse_ordered_list(next_element)
            elif next_element.name in ["h3", "h4", "h5"]:
                self.main_content.append(Paragraph(next_element.text, self.styles[f'CenteredHeading{next_element.name[-1]}']))
            elif next_element.name in ['p', 'li']:
                self.parse_paragraph(next_element)
            next_element = next_element.find_next_sibling()

    def parse_ordered_list(self, element):
        list_index = 1
        for li in element.find_all('li'):
            self.main_content.append(Paragraph(f"{list_index}. {li.text}", self.subparagraph_style11))
            list_index += 1

    def parse_paragraph(self, element):
        image_paths = self.extract_images_from_children(element)
        for img_path in image_paths:
            # self.doc.handle_nextPageTemplate('imagepage') 
            image_flowable = ImageRenderer(img_path, width=self.page_size[0], height=self.page_size[1])
            self.main_content.append(image_flowable)
            # self.doc.handle_nextPageTemplate('textpage') 
        if len(image_paths) == 0:
            self.main_content.append(Paragraph(element.text, self.styles['JustifiedBody']))

    def extract_images_from_children(self, element):
        return [img['src'] for img in element.find_all('img', src=True)]

    def add_intro_content(self, title, section):
        self.intro_content.append(Paragraph(f"{title}", self.styles['Heading2']))
        next_element = section.find_next_sibling()
        while next_element and next_element.name != 'h2':
            if next_element.name in ['p', 'li']:
                self.intro_content.append(Paragraph(next_element.text, self.styles['JustifiedBody']))
            next_element = next_element.find_next_sibling()
        self.intro_content.append(PageBreak())

    def parse_non_lesson_section(self, section):
        next_element = section.find_next_sibling()
        while next_element:
            if next_element.name == 'h2':
                break
            if next_element.name in ["h3", "h4", "h5"]:
                self.intro_content.append(Paragraph(next_element.text, self.styles[f'CenteredHeading{next_element.name[-1]}']))
            elif next_element.name in ['p', 'li']:
                text = next_element.decode_contents()
                self.intro_content.append(Paragraph(text, self.subparagraph_style1))
            next_element = next_element.find_next_sibling()

    def generate_pdf(self, is_buffer = False):
        buffer = None
        if is_buffer:
            buffer = "BytesIO().pdf"
        self.create_document(buffer)
        
        if buffer:
            self.create_first_page_content()
            self.build_intro_content()
        if buffer:
            self.build_toc()        
    
            self.build_main_content()
        
        self.finalize_document(buffer)

    def create_document(self, buffer=None):
        target = self.output_file if not buffer else buffer
        self.doc = CustomTemplate1(target,
                            pagesize=self.page_size,
                            rightMargin=40, leftMargin=40,
                            topMargin=20, bottomMargin=20)
        self.doc1 = CustomTemplate1(target,
                            pagesize=self.page_size,
                            rightMargin=0, leftMargin=0,
                            topMargin=0, bottomMargin=0)
        
        frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='normal')
        frame1 = Frame(self.doc1.leftMargin, self.doc1.bottomMargin, self.doc1.width, self.doc1.height, id='normal')

        template = PageTemplate(id='textpage', frames=frame, onPage=lambda canvas, doc: self.add_page_number(canvas, doc))
        template1 = PageTemplate(id='imagepage', frames=frame1, onPage=lambda canvas, doc: self.add_page_number(canvas, doc))
        
        self.doc.addPageTemplates([template])
        self.doc.addPageTemplates([template1])

    # def build_intro_content(self):
    #     intro_content_copy = copy.deepcopy(self.intro_content)
    #     intro_page_count = self.build_intro_and_get_page_count(copy.deepcopy(intro_content_copy), "intro")
    #     self.intro_content, intro_page_count

    def build_intro_content(self):
        intro_content_copy = copy.deepcopy(self.intro_content)
        intro_page_count = self.build_intro_and_get_page_count(copy.deepcopy(intro_content_copy), "intro")
        intro_content, intro_page_count = self.addBlankPage(copy.deepcopy(self.intro_content), intro_page_count, "even", section_start_page=1, count_start_page=0, start_numbering_on_page=2, stop=None, num_type="i")
        self.intro_page_count = intro_page_count
        self.intro_content_ = intro_content
    def build_toc(self):
        toc_title = Paragraph("Contents", self.styles['Heading1'])
        toc = [toc_title, self.doc.toc]
        toc_page_count = self.build_intro_and_get_page_count(toc.copy(), "toc")
        toc, toc_page_count = self.addBlankPage(toc, toc_page_count, "even", section_start_page=self.intro_page_count+1, count_start_page=self.intro_page_count, stop=None, num_type="i")
        # toc = [toc_title, toc]
        self.toc_page_count = toc_page_count
        self.story.extend(copy.deepcopy(self.intro_content_))
        self.story.extend(toc)
        self.toc_elems = toc
        # self.story.append(PageBreak())

    def build_main_content(self):
        pages_so_far = self.toc_page_count + self.intro_page_count + 1
        main_content_page_count = self.build_intro_and_get_page_count(copy.deepcopy(self.main_content), None)
        self.addBlankPage(copy.deepcopy(self.main_content), main_content_page_count, None, section_start_page=pages_so_far, count_start_page=1, stop=None, num_type="1")
        self.story.extend(copy.deepcopy(self.main_content))

    def finalize_document(self, is_buffer=True):
        if is_buffer:
            self.doc.multiBuild(self.story)
            self.toc = self.doc.toc
        else:
            self.update_toc()
            self.build_final_document()

    def update_toc(self):
        toc_ = copy.deepcopy(self.toc_elems[1])
        toc_entries = toc_._entries
        modified_toc = [(entry[0], entry[1], self.get_page_number(entry[2], False), entry[3]) for entry in toc_entries]
        toc_._entries = modified_toc
        self.toc_ = toc_
        return toc_

    def build_final_document(self):
        final_story = []
        if self.intro_page_count > 0:
            final_story.extend(self.intro_content_)

        toc_content = self.create_toc_content()
        final_story.extend(toc_content)
        # final_story.append(PageBreak()) # start main contents on new page
        final_story.extend(copy.deepcopy(self.main_content))

        self.doc.build(final_story)

    def create_toc_content(self):
        toc_entries = self.toc_._entries
        toc_content = [Paragraph("Contents", self.styles['Heading1'])]
        toc_table_nolinks = self.create_toc(toc_entries, self.styles, True)
        toc_content.append(toc_table_nolinks)

        toc_page_count_first = self.build_intro_and_get_page_count(toc_content, "toc")
        toc_content, toc_page_count_second = self.addBlankPage(toc_content, toc_page_count_first, "even", section_start_page=self.intro_page_count+1, count_start_page=self.intro_page_count, stop=None, num_type="i")

        toc_content = [Paragraph("Contents", self.styles['Heading1'])]
        toc_table = self.create_toc(toc_entries, self.styles)
        toc_content.append(toc_table)
        toc_content.append(PageBreak())
        if toc_page_count_first != toc_page_count_second:
            toc_content.append(PageBreak())

        return toc_content

    def create_toc(self, entries, styles, nolinks=False):
        toc_style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('RIGHTPADDING', (0, 0), (0, -1), 20),
            ('LEFTPADDING', (1, 0), (1, -1), 6),
        ])
        
        toc_data = []
        for _, text, page, link in entries:
            if not nolinks:
                p = Paragraph(f'<a href="#{link}" color="blue">{text}</a>', styles['TOC_Entry'])
            else:
                p = Paragraph(f'{text}', styles['TOC_Entry'])
            toc_data.append([p, str(page)])
        
        table = Table(toc_data, colWidths=['95%', '5%'], style=toc_style)
        return table

    def build_intro_and_get_page_count(self, content, section=None):
        buffer = BytesIO()
        intro_doc = CustomTemplate1(buffer,
                             pagesize=self.page_size,
                             rightMargin=40, leftMargin=40,
                             topMargin=20, bottomMargin=20)

        frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='normal')
        template = PageTemplate(id='textpage', frames=frame)
        intro_doc.addPageTemplates([template])
        intro_doc.build(content)
        buffer.seek(0)

        pdf_reader = PdfReader(buffer)
        return len(pdf_reader.pages)

    def addBlankPage(self, section, page_count, page_count_type, section_start_page=0, count_start_page=0, start_numbering_on_page=1, stop=None, num_type=None):
        section_copy = copy.deepcopy(section)
        page_count_old = page_count
        for i in range(page_count_old): # starts counting from zero
            if num_type is not None:
                tab = i + section_start_page
                if tab >= start_numbering_on_page:
                    self.page_numbers[tab] = {
                        "type": num_type,
                        "number": count_start_page + i
                    }
        section_copy = section_copy + [PageBreak()] # start next section in new page
        if page_count_type in ["odd", "even"]:
            if (page_count_type == "odd" and page_count % 2 == 0) or \
               (page_count_type == "even" and page_count % 2 != 0):
                page_count += 1
                section_copy = section_copy + [PageBreak()] # blank page
        return section_copy, page_count

    def get_page_number(self, page_num, format=True):
        page_num_elem = self.page_numbers.get(page_num)
        if page_num_elem:
            num_type = page_num_elem["type"]
            page_num = page_num_elem["number"]
            if num_type == "i":
                text = f"{self.roman(page_num).lower()}"
            elif num_type == "1":
                text = f"{page_num}"
            else:
                return
            if format:
                text = f"—{text}—"
            return text
        return False

    @staticmethod
    def roman(num):
        roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        return roman_numerals[num - 1] if num <= 10 else str(num)

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        page_num = canvas.getPageNumber()
        text = self.get_page_number(page_num)
        if not text:
            return
        canvas.setFont("Arial", 10)
        x_center = self.page_size[0] / 2
        canvas.drawCentredString(x_center, doc.bottomMargin - 5, text)
        canvas.restoreState()


    
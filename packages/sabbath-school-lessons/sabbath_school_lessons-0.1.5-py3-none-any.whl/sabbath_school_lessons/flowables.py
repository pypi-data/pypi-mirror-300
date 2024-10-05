from reportlab.platypus import Flowable
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage
import tempfile, os
from . import translations
class LessonHeader(Flowable):
    def __init__(self, lesson_num, date_range, bible_text, title, width, height1, background_color, width_extra=0, lang="en"):
        Flowable.__init__(self)
        self.lesson_num = lesson_num
        self.bible_text = bible_text
        self.date_range = date_range
        self.title = title
        self.width = width
        self.height1 = height1
        self.height = height1 + 50
        self.background_color = background_color
        self.width_extra = width_extra
        self.lang = lang

    def draw(self):
        self.canv.setFillColor(self.background_color)
        self.canv.rect(0, 0, (1.25+self.width_extra)*inch, self.height, fill=1, stroke=0)
        
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Arial-Bold", 12)

        lesson_text = translations.get_lesson_text(self.lang, case="title")
        self.canv.drawString(0.25*inch, 10, lesson_text)
        self.canv.setFont("Arial-Bold", 24)
        self.canv.drawString(0.88*inch, 20, self.lesson_num)

        self.canv.setFillColor(colors.black)
        self.canv.setFont("Arial", 10)
        self.canv.drawString((1.30+self.width_extra)*inch, self.height-10, self.date_range)
        self.canv.setFont("Arial-Bold", 14)
        
        words = self.title.split()
        current_line = ""
        title_lines = []

        for word in words:
            if len(current_line) + len(word) + 1 <= 26:
                current_line += (word + " ")
            else:
                title_lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            title_lines.append(current_line.strip())

        center_xes = [i*14 for i in range(len(title_lines))]
        max_value = max(center_xes)
        min_value = min(center_xes)
        range_value = max_value - min_value
        midpoint_of_range = range_value / 2
        center_xes.reverse()
        center_xes[:] = [(tab - midpoint_of_range+self.height/2 -10) for tab in center_xes]
        
        for i, center_x in enumerate(center_xes):
            self.canv.drawString((1.30+self.width_extra)*inch, center_x, title_lines[i])
        
        if self.bible_text:
            self.canv.setFont("Arial", 10)
            self.canv.drawString((1.30+self.width_extra)*inch, 0, self.bible_text)

class ImageRenderer(Flowable):
    def __init__(self, image_path, width, height,topMargin=20, background_color=None):
        Flowable.__init__(self)
        self.image_path = image_path
        self.width = width
        self.height = height - topMargin*2.7
        self.total_width = width
        self.total_height = height
        self.background_color = background_color

    def draw(self):
        with PILImage.open(self.image_path) as img:
            img_width, img_height = img.size

            if img_width > img_height:
                img = img.rotate(-90, expand=True)
                img_width, img_height = img.size

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                img.save(temp_file.name, format='PNG')
                temp_image_path = temp_file.name

        with PILImage.open(temp_image_path) as img:
            img_width, img_height = img.size
            
            scale_x = self.total_width / img_width
            scale_y = self.total_height / img_height
            scale_factor = min(scale_x, scale_y)
            scale_factor *= 0.9

            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            x_pos = ((self.total_width - new_width)) / 2 - 45
            y_pos = (self.total_height - new_height) / 2

            self.canv.drawImage(temp_image_path, x_pos, y_pos, width=new_width, height=new_height, mask='auto')

        os.remove(temp_image_path)

class FirstPageRender(Flowable):
    def __init__(self, title, subtitle, copyright_info, width, height, title_color=colors.black, copyright_color=colors.gray,lesson_book=None,lang="en"):
        Flowable.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.lesson_book = lesson_book
        self.copyright_info = copyright_info
        self.width = width
        self.height = height
        self.title_color = title_color
        self.copyright_color = copyright_color
        self.lang = lang

    def draw(self):
        canvas = self.canv  # Reference to the canvas

        # Draw the title at the top center
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(colors.gray)
        canvas.drawCentredString(self.width / 2.0, self.height - 1 * inch, translations.translations["Sabbath School Lesson"][self.lang])

        canvas.setFont("Helvetica-Bold", 24)
        canvas.setFillColor(self.title_color)
        canvas.drawCentredString(self.width / 2.0, self.height - 1.5 * inch, self.title)

        if self.lesson_book:
            lesson_book = translations.translate_word(self.lesson_book, self.lang)
            canvas.setFont("Helvetica-Bold", 16)
            canvas.setFillColor(colors.gray)
            canvas.drawCentredString(self.width / 2.0, self.height - 2.0 * inch, lesson_book) # chapters
        
        canvas.setFont("Helvetica-Bold", 18)
        canvas.setFillColor(colors.black)
        subtitle = translations.translate_word(self.subtitle, self.lang)
        canvas.drawCentredString(self.width / 2.0, self.height - 3.5 * inch, subtitle)

        # Draw the copyright info at the bottom center
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(self.copyright_color)
        copyright_info = translations.translate_word(self.copyright_info, self.lang)
        canvas.drawCentredString(self.width / 2.0, 0.5 * inch, copyright_info)

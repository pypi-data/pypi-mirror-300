from . import booklets
from . import markdown_to_pdf
import json

def batch(config_file):
    # Load configurations from JSON file
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Initialize the booklet object
    booklet = booklets()

    # Iterate through each lesson in the config
    for lesson in config["lessons"]:
        # Create markdown_to_pdf instance
        markdown2pdf = markdown_to_pdf(
            lesson["markdown_file"],
            quarter=lesson["quarter"],
            lesson_title=lesson["lesson_title"],
            start_date=lesson["start_date"],
            lesson_book=lesson["lesson_book"],
            lang=lesson.get("lang")  # Optional language parameter
        )

        # Process markdown to PDF
        markdown2pdf.pre_process().process()

        # Convert to booklet format
        booklet.A5_on_A4(markdown2pdf.output_file)
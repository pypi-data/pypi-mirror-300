# Sabbath School Lessons

This module is part of a project to improve upon the work done by [Adventist Archives](https://www.adventistarchives.org/) in digitizing old Sabbath School Lessons. Its purpose is to produce output documents in multiple formats for use on the web, on phone applications, and for printing, which are free from the OCR errors that exist in the documents scanned and *OCRed* by Adventist Archives. Furthermore, it enables the reproduction of an old lesson for a new quarter at the click of a button.

## Contents
1. [The Process](#the-process)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Usage](#usage)
   - [Numbering](#numbering)
   - [Generating PDFs](#generating-pdfs)
5. [Contributing](#contributing)

## The Process

Text documents extracted from the PDFs available from Adventist Archives are available at [ssl-pdfs](https://sslpdfs.gospelsounders.org). These documents should be proofread to remove OCR errors and add a little formatting:

```markdown
##

Original Title

### SABBATH SCHOOL LESSONS ON THE ACTS OF THE APOSTLES

#### For Senior Classes

#### SECOND QUARTER, 1898

....
## LESSON 1. — JOURNEYING TO JERUSALEM.
(Acts 21:1-17.)
April 2, 1898

<start_numbering>
question 1
question 2
...
<stop_numbering>

### Notes
<start_numbering>
note 1
note 2
...
<stop_numbering>
```

Formatting Guidelines:
1. Start the document with `##` followed by a blank line
2. For sections which appear before the first lesson, for titles or for centering `big text` use heading 3 (```###``` followed by space before the title). For smaller centered text use heading 4 `####`. Try all possible headings (excluding heading1 and heading2) to see what fits your need.
3. Use heading 2 on all lesson sections
4. After the lesson title line, add both the `lesson texts` and date. For now, only a single date in the format `April 2, 1898` is supported. The order of the date and texts does not matter as long as they are in adjacent lines.
5. Use heading 3 for all notes sections
6. In case extra material such as images are added, these will appear each on its own page.
7. (Optionally) use the `<start_numbering>` and `<stop_numbering>` tags between sections which you would like to turn into an ordered list and have numbers added, if the lines are not numbered already.

## Features

- Converts markdown to PDF
- Generates a table of contents
- Adds page numbers
- Supports multiple languages (currently English and Swahili)
- Handles images and creates full-page image spreads
- Creates a cover page
- Supports custom styling and formatting

## Requirements

- Python 3.x
- Required Python libraries: reportlab, BeautifulSoup, markdown, PyPDF2, Pillow

## Usage

1. Prepare your markdown file according to the specified format (see [the process](#the-process)).
2. Install the package:

```bash
pip install sabbath-school-lessons
```

### Numbering
This section is only needed if you need to fix lists in your markdown files:

```python
from sabbath_school_lessons import markdown
markdown.number_lines_in_md("input.md", "output.md")  # the output file can be set to be the same as the input
```

### Generating PDFs

```python
from sabbath_school_lessons import markdown_to_pdf
markdown2pdf = markdown_to_pdf("english.md", quarter="Quarter 4, 2024", lesson_title="Acts of the Apostles", start_date="October 5, 2024", lesson_book="Chapters 21:1 - 28:31")

# lesson_book is optional. It is only used for lessons which are based on a book
```

example of output file name: `SSL20241001-04-ACTS_OF_THE_APOSTLES.pdf` will match the format `SSSYYYYMMNN-QQ-LESSON_TITLE.pdf` Where `N` is the number of lesson in the quarter. Most quarters will only have one lesson. `Q` is the quarter.

### CMS
#### Initial setup
The lessons are designed to be hosted using `gh-pages`, divided per decade, each decade closing on the `0th` year. Therefore there is a repo for each decade. Creating these repos is a one time affair. One you have a personal access token, put it in your environment variables `export GHPAT=token`. Then run this script:

```python
from sabbath_school_lessons import cms
CMS = cms()
CMS.create_repos_for_all_decades()
```

#### Adding the original content
Next we add the original content (pdfs and extracted text from [Adventist Archives](https://www.adventistarchives.org/)). 

```python
from sabbath_school_lessons import cms
CMS = cms()
CMS.original_content()
```

## Contributing

Contributions to improve the module are welcome. Please submit pull requests or open issues for any bugs or feature requests.
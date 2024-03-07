import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.units import inch

# Register a font that supports Chinese characters
font_name = 'ChineseFont'
pdfmetrics.registerFont(TTFont(font_name, 'simhei.ttf'))

def generate_toc(toc_data, toc_filename):
    """Generate a PDF for the Table of Contents."""
    c = Canvas(toc_filename, pagesize=letter)
    width, height = letter
    y_position = height - 2 * inch

    # Define a function to set font, so it can be reused for new pages
    def set_font():
        c.setFont(font_name, 12)

    set_font()  # Set font for the first page

    for title, page_number in toc_data:
        if y_position < inch:  # If there's not enough space, create a new page and reset font
            c.showPage()
            set_font()  # Re-apply font settings for the new page
            y_position = height - 2 * inch  # Reset y_position for the new page

        c.drawString(inch, y_position, f"{title} - Page {page_number}")
        y_position -= 0.2 * inch

    c.save()

def create_music_sheets_pdf(music_sheets_dir, content_filename):
    """Create a PDF for the music sheets, ensure each starts on a new left page, and add page numbers."""
    width, height = letter
    c = Canvas(content_filename, pagesize=letter)
    toc_data = []
    current_page = 1  # Start from page 1 for content

    for music_name in sorted(os.listdir(music_sheets_dir)):
        music_dir = os.path.join(music_sheets_dir, music_name)
        if os.path.isdir(music_dir):
            # Check if the first page of music needs to start on a new left page
            if current_page % 2 == 0:  # If it's even, the next page is odd, add a blank page
                c.showPage()
                current_page += 1
            toc_data.append((music_name, current_page))

            for sheet in sorted(os.listdir(music_dir)):
                sheet_path = os.path.join(music_dir, sheet)
                c.drawImage(sheet_path, 0, 0, width=width, height=height, preserveAspectRatio=True, mask='auto')
                
                # Add page numbers, excluding TOC pages. Adjust positioning based on the page number.
                if current_page % 2 == 0:  # Even page number, right side
                    c.drawRightString(width - inch, 0.5 * inch, str(current_page))
                else:  # Odd page number, left side
                    c.drawString(inch, 0.5 * inch, str(current_page))

                c.showPage()
                current_page += 1

    c.save()
    return toc_data

def merge_pdfs(toc_filename, content_filename, output_filename):
    """Merge the TOC and content PDFs into the final PDF."""
    writer = PdfWriter()

    # Add TOC pages
    toc_reader = PdfReader(toc_filename)
    for page in toc_reader.pages:
        writer.add_page(page)

    # Add content pages
    content_reader = PdfReader(content_filename)
    for page in content_reader.pages:
        writer.add_page(page)

    with open(output_filename, 'wb') as f_out:
        writer.write(f_out)

def create_pdf(output_filename, music_sheets_dir):
    content_filename = "temp_content.pdf"
    toc_filename = "temp_toc.pdf"

    # Create music sheets PDF and get TOC data
    toc_data = create_music_sheets_pdf(music_sheets_dir, content_filename)

    # Generate TOC PDF
    generate_toc(toc_data, toc_filename)

    # Merge TOC and content into the final PDF
    merge_pdfs(toc_filename, content_filename, output_filename)

    # Optionally, remove temporary files
    os.remove(content_filename)
    os.remove(toc_filename)

# Example usage
music_sheets_dir = "./music"  # Adjusted to a more likely path based on your initial example
output_filename = "music_sheets_collection_with_toc.pdf"
create_pdf(output_filename, music_sheets_dir)

import os
import PyPDF2
from fpdf import FPDF
import sys

# List of replacements: (degree program, university name, abbreviation)
replacements = [
    ("M.S. in Computer Science program", "Northwestern University", "NU"),
    ("M.S. in Computer Science program", "University of Chicago", "UChicago"),
    ("MEng in Computer Science program", "Cornell Tech", "CU"),
    ("MCS in Computer Science program", "University of Illinois Urbana-Champaign", "UIUC"),
    ("M.S. in Computer Science program", "Stanford", "Stanford"),
    ("M.S. in Computer Science program", "New York University", "NYU"),
    ("M.S. in Computer Science program", "Georgetown University", "GU")
]

# Function to read PDF content
def extract_text_from_pdf(input_pdf):
    with open(input_pdf, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Function to create PDF from modified content
def create_pdf(output_pdf, content, output_dir):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    lines = content.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)

    output_path = os.path.join(output_dir, output_pdf)
    pdf.output(output_path)

# Function to replace phrases and create new PDFs
def replace_phrases_and_create_pdfs(input_pdf):
    # Ensure output directory exists
    output_dir = "SLueders Rec Letters"
    os.makedirs(output_dir, exist_ok=True)

    # Read original content from the input PDF
    original_content = extract_text_from_pdf(input_pdf)

    for idx, (degree_program, university, abbreviation) in enumerate(replacements, start=1):
        # Replace the specific phrases
        new_content = original_content.replace("M.S. in Computer Science program", degree_program)
        new_content = new_content.replace("Carnegie Mellon University", university)
        new_content = new_content.replace("CMU", abbreviation)

        output_pdf = f"output_university_{idx}_{abbreviation}.pdf"
        create_pdf(output_pdf, new_content, output_dir)

    print(f"Created all PDFs in the '{output_dir}' directory.")

def main():
    if len(sys.argv) != 2:
        print("Usage: rec-transcriber-jdo <filename.pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]

    if not os.path.exists(input_pdf):
        print(f"Error: File '{input_pdf}' not found.")
        sys.exit(1)

    replace_phrases_and_create_pdfs(input_pdf)


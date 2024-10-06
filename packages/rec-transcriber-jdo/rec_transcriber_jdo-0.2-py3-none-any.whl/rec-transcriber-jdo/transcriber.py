import fitz  # PyMuPDF
import os
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

# Function to replace text in a PDF and preserve formatting
def replace_text_in_pdf(input_pdf, output_pdf, replacements, font, font_size):
    # Open the PDF file
    doc = fitz.open(input_pdf)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Replace the degree program
        for degree_program, university, abbreviation in replacements:
            text_instances = page.search_for("M.S. in Computer Science program")
            for instance in text_instances:
                rect = instance
                page.insert_textbox(rect, degree_program, fontsize=font_size, fontname=font)

            # Replace the university name
            instances_university = page.search_for("Carnegie Mellon University")
            for instance in instances_university:
                rect = instance
                page.insert_textbox(rect, university, fontsize=font_size, fontname=font)

            # Replace the abbreviation
            instances_abbreviation = page.search_for("CMU")
            for instance in instances_abbreviation:
                rect = instance
                page.insert_textbox(rect, abbreviation, fontsize=font_size, fontname=font)

    # Save the new PDF
    doc.save(output_pdf)
    doc.close()

# Function to create copies with text replacements
def create_university_pdfs(input_pdf, font, font_size):
    # Ensure output directory exists
    output_dir = "Seb-Lueders-Rec-Letters"
    os.makedirs(output_dir, exist_ok=True)

    for idx, (degree_program, university, abbreviation) in enumerate(replacements, start=1):
        output_pdf = os.path.join(output_dir, f"{idx}_{abbreviation}.pdf")
        replace_text_in_pdf(input_pdf, output_pdf, [(degree_program, university, abbreviation)], font, font_size)

    print(f"Created all PDFs in the '{output_dir}' directory.")

def main():
    if len(sys.argv) != 4:
        print("Usage: rec-transcriber-jdo <filename.pdf> <font> <font-size>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    font = sys.argv[2]
    font_size = float(sys.argv[3])

    if not os.path.exists(input_pdf):
        print(f"Error: File '{input_pdf}' not found.")
        sys.exit(1)

    create_university_pdfs(input_pdf, font, font_size)

if __name__ == "__main__":
    main()

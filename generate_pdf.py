import json
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Questionnaire", align="C", ln=True)
        self.cell(0, 10, "", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        page_number = f"Page {self.page_no()}"
        self.cell(0, 10, page_number, align="C")

def generate_questions(data, pdf: PDF, print_response:  bool = False):
    pdf.add_page()

    question_number = 1
    # Add questions  to the PDF
    for question_data in data:
        question = question_data["question"]
        options = [
            f"A{question_data['A']}",
            f"B{question_data['B']}",
            f"C{question_data['C']}",
            f"D{question_data['D']}"
        ]

        # Add question
        pdf.multi_cell(0, 10, f"{question_number} . {question}")

        # Add options
        for option in options:
            pdf.multi_cell(0, 10, option)

        # Add response
        response = "?"
        if print_response:
            response = question_data["reponse"]
        pdf.cell(0, 10, f"Response: {response}", ln=True)
        pdf.cell(0, 10, "", ln=True)
        question_number += 1
        
    pdf.add_page()

def generate_pdf(filename , json_data):

    # Create PDF document
    pdf = PDF()
    pdf.add_page()

    # Set font style and size
    pdf.set_font("Arial", size=10)

    generate_questions(json_data, pdf, print_response=False)
    generate_questions(json_data, pdf, print_response=True)

    # Save PDF to a file
    pdf.output(filename)

def generate_pdf_quiz(file_name, json_data):

    # remove extension .pdf from file name
    if file_name.endswith(".json"):
        file_name = file_name[:-5]

    # Generate PDF
    generate_pdf(f"{file_name}.pdf", json_data)


from extract_features import extract_features
import json
from flask import current_app
from pdf_blueprint.fpdf_structure import PDF
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_image(filepath):
    image_features = extract_features(filepath)
    return json.dumps(image_features,indent=4)


def generate_pdf(text, name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    reports_dir = os.path.join(BASE_DIR, "reports") 
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    pdf_filename = f"report_{name}.pdf"
    pdf_path = os.path.join(reports_dir, pdf_filename)  
    relative_path = os.path.join("reports", pdf_filename) 
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Analysis")
    pdf.chapter_body(text)

    pdf.output(pdf_path, dest="F")

    return relative_path
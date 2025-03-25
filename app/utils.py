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
    reports_dir = os.path.join("app", "reports")
    os.makedirs(reports_dir, exist_ok=True)  # Ensure directory exists

    complete_source_path = os.path.join(reports_dir, f"report_{name}.pdf")
    print(f"PDF will be saved at: {complete_source_path}")  # Debugging

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Analysis')
    pdf.chapter_body(text)
    pdf.output(complete_source_path, dest="F")

    return os.path.join("reports", f"report_{name}.pdf")  # Return relative path

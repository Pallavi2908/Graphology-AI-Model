from flask import Blueprint,send_from_directory, request, jsonify,current_app,send_file
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

from app.utils import allowed_file, process_image,generate_pdf
from agent import get_traits_from_AI
main = Blueprint('main', __name__)
CORS(main) #allow react to interact

@main.route('/reports/<filename>',methods=['GET'])
def download_file(filename):
     reports_dir = os.path.join(os.getcwd(), 'app', 'reports')  # Adjust this path if needed
     # Debugging - Print file path to check if it exists
     pdf_path = os.path.join(reports_dir, filename)
     if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return jsonify({"error": "PDF not found"}), 404

     return send_from_directory(reports_dir, filename, as_attachment=True)

@main.route('/', methods=['POST'])
def upload_image():    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    name = request.form.get('name', 'Unknown User')  # Prevent KeyError

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure uploads folder exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)     
        file.save(filepath)
        handwriting_traits = process_image(filepath)        
        result = get_traits_from_AI(handwriting_traits)

        if not result:
            return jsonify({"error": "AI processing failed"}), 500
        
        pdf_path = generate_pdf(result, name)       
        pdf_filename = os.path.basename(pdf_path)
        current_app.config['LAST_PDF_PATH'] = pdf_path
        
        return jsonify({
            "message": "Upload successful",
            "pdf_url": f"/reports/{pdf_filename}"
        })

from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app import app
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.ocr_reader import extract_text_from_image
from app.utils.summarizer import generate_summary

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text based on file type
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)

        # Generate summary
        summary_text = generate_summary(text)

        # Clean up uploaded file
        os.remove(file_path)

        return render_template('result.html', summary=summary_text, original_text=text[:500] + '...' if len(text) > 500 else text)
    else:
        flash('Invalid file type. Please upload a PDF or image file.')
        return redirect(url_for('index'))

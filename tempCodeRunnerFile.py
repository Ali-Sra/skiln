from flask import Flask, render_template, request, redirect, url_for
import os
from infer import main as run_inference  # Assuming 'main' is the entry point in infer.py
import argparse

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
OUTPUT_FOLDER = os.path.join('static', 'outputs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # تنظیم آرگومان‌ها برای infer.py
        args = argparse.Namespace(
            input=file_path,
            output=app.config['OUTPUT_FOLDER'],
            show_detections=False,
            save_steps=False
        )

        # اجرای inference
        run_inference(args)  # استفاده از args به جای دو آرگومان

        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'<h1>Processing Complete</h1><img src="/static/outputs/{filename}" alt="Processed Image">'

if __name__ == '__main__':
    app.run(debug=True)

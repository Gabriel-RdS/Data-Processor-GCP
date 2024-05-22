from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app.data_processor import DataProcessor
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        dataset = request.form.get('dataset')
        table = request.form.get('table')
        if file and dataset and table:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            try:
                processor = DataProcessor(file_path)
                processor.process_data()
                processor.upload_to_bigquery(f"{dataset}.{table}", os.getenv('GCP_PROJECT_ID'))
                flash('Arquivo enviado e processado com sucesso!', 'success')
            except Exception as e:
                flash(f'Erro ao carregar o arquivo {file_path}: {e}', 'danger')
            finally:
                # Remove o arquivo após o processamento
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return redirect(url_for('main.index'))
    
    return render_template('index.html')

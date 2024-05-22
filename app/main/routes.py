from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app.data_processor import DataProcessor
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            try:
                processor = DataProcessor(file_path)
                processor.process_data()
                # Use variáveis de ambiente
                processor.upload_to_bigquery(os.getenv('BIGQUERY_TABLE_NAME'), os.getenv('GCP_PROJECT_ID'))
                flash('Arquivo enviado e processado com sucesso!', 'success')
            except Exception as e:
                flash(f'Ocorreu um erro: {e}', 'danger')
            
            return redirect(url_for('main.index'))
    
    return render_template('index.html')

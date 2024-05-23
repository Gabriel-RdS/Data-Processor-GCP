from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from app.data_processor import DataProcessor
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        sheet = request.form.get('sheet', None)  # Obtém o nome da página, se fornecido
        dataset = request.form['dataset']
        table = request.form['table']
        
        if file and dataset and table:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            try:
                processor = DataProcessor(file_path, sheet_name=sheet)
                processor.process_data()
                table_id = f"{dataset}.{table}"
                processor.upload_to_bigquery(table_id, os.getenv('GCP_PROJECT_ID'))
                flash('Arquivo enviado e processado com sucesso!', 'success')
                # Deleta o arquivo após o processamento
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({"success": True, "message": "Arquivo enviado e processado com sucesso!"})
            except Exception as e:
                flash(f'Ocorreu um erro: {e}', 'danger')
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({"success": False, "message": f"Ocorreu um erro: {e}"})
    
    return render_template('index.html')

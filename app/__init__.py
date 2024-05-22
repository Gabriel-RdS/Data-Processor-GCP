from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configura o diretório de templates
    app = Flask(__name__, template_folder='main/templates')
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Importa e registra a Blueprint 'main'
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

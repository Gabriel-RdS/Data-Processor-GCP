import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    # Adicione outras configurações, como credenciais do BigQuery

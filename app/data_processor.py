import pandas as pd
import pandas_gbq as pd_gbq
import os
import unicodedata
import re

class DataProcessor:
    """
    Classe para processar dados de um arquivo Excel e fazer upload para o BigQuery.
    
    Atributos:
        file_path (str): Caminho para o arquivo Excel.
        df (pd.DataFrame): DataFrame carregado do arquivo Excel.
    """
    
    def __init__(self, file_path):
        """
        Inicializa a classe DataProcessor com o caminho do arquivo Excel.
        
        Parâmetros:
            file_path (str): Caminho para o arquivo Excel.
        """
        if not isinstance(file_path, str):
            raise TypeError("O caminho do arquivo deve ser uma string.")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        self.file_path = file_path
        self.df = self._load_excel(file_path)

    def _load_excel(self, file_path):
        """
        Carrega um arquivo Excel em um DataFrame do pandas.
        
        Parâmetros:
            file_path (str): Caminho para o arquivo Excel.
        
        Retorna:
            pd.DataFrame: DataFrame carregado do arquivo Excel, ou None se ocorrer um erro.
        """
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            return df
        except FileNotFoundError:
            print(f"Erro: Arquivo {file_path} não encontrado.")
        except pd.errors.EmptyDataError:
            print(f"Erro: O arquivo {file_path} está vazio.")
        except ImportError as e:
            print(f"Erro ao importar a biblioteca necessária: {e}")
        except Exception as e:
            print(f"Erro ao carregar o arquivo {file_path}: {e}")
        return None


    @staticmethod
    def strip_accents(s):
        """
        Remove acentos, caracteres especiais e substitui espaços por underscores em uma string.
        
        Parâmetros:
            s (str): String a ser normalizada.
        
        Retorna:
            str: String normalizada.
        """
        if not isinstance(s, str):
            raise TypeError("O valor fornecido deve ser uma string.")
        
        try:
            # Normaliza os caracteres acentuados
            s = ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')
            
            # Remove parênteses e caracteres especiais
            s = re.sub(r'[()=,]', '', s)
            
            # Substitui espaços em branco por underscores
            s = re.sub('\s+', '_', s.strip())
            
            # Limita a 300 caracteres
            s = s[:300]
            
            s = s.lower()
            
            return s
        except Exception as e:
            print(f"Erro ao normalizar string {s}: {e}")
            return s

    def process_data(self):
        """
        Processa os dados do DataFrame, renomeando as colunas e convertendo todos os valores para strings.
        
        Este método deve ser chamado após a inicialização da classe para preparar os dados antes de fazer upload para o BigQuery.
        """
        if self.df is not None:
            try:
                self.df = self._rename_columns(self.df)
                self.df = self._convert_to_string(self.df)
            except Exception as e:
                print(f"Erro ao processar dados: {e}")
        else:
            print("Erro: DataFrame não carregado corretamente.")

    def _rename_columns(self, df):
        """
        Renomeia as colunas do DataFrame, removendo acentos e caracteres especiais.
        
        Parâmetros:
            df (pd.DataFrame): DataFrame a ser processado.
        
        Retorna:
            pd.DataFrame: DataFrame com colunas renomeadas.
        """
        try:
            df.rename(columns=lambda x: self.strip_accents(x), inplace=True)
        except Exception as e:
            print(f"Erro ao renomear colunas: {e}")
        return df

    def _convert_to_string(self, df):
        """
        Converte todos os valores do DataFrame para strings.
        
        Parâmetros:
            df (pd.DataFrame): DataFrame a ser processado.
        
        Retorna:
            pd.DataFrame: DataFrame com todos os valores convertidos para strings.
        """
        try:
            df = df.astype(str)
        except Exception as e:
            print(f"Erro ao converter valores para string: {e}")
        return df

    def upload_to_bigquery(self, table_name, project_id):
        """
        Faz upload dos dados processados para uma tabela no BigQuery.
        
        Parâmetros:
            table_name (str): Nome completo da tabela no BigQuery (ex: 'dataset.table').
            project_id (str): ID do projeto do Google Cloud.
        """
        if not isinstance(table_name, str) or not table_name:
            raise ValueError("O nome da tabela deve ser uma string não vazia.")
        
        if not isinstance(project_id, str) or not project_id:
            raise ValueError("O ID do projeto deve ser uma string não vazia.")
        
        if self.df is not None:
            try:
                pd_gbq.to_gbq(self.df, table_name, project_id=project_id, if_exists='replace')
            except Exception as e:
                print(f"Erro ao fazer upload para o BigQuery: {e}")
        else:
            print("Erro: DataFrame não carregado corretamente. Upload não realizado.")

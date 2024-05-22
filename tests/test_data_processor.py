import unittest
import os
import pandas as pd
from app.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'nome': ['José', 'Ana'],
            'idade': [28, 24],
            'cidade': ['São Paulo', 'Rio de Janeiro']
        })
        self.file_path = 'test_file.xlsx'
        self.df.to_excel(self.file_path, index=False)
        self.processor = DataProcessor(self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def test_init_with_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            DataProcessor('invalid_path.xlsx')

    def test_init_with_invalid_type(self):
        with self.assertRaises(TypeError):
            DataProcessor(123)

    def test_strip_accents(self):
        self.assertEqual(DataProcessor.strip_accents('São Paulo'), 'sao_paulo')
        self.assertEqual(DataProcessor.strip_accents('Ana Maria'), 'ana_maria')

    def test_strip_accents_with_invalid_type(self):
        with self.assertRaises(TypeError):
            DataProcessor.strip_accents(123)

    def test_load_excel(self):
        self.assertIsInstance(self.processor.df, pd.DataFrame)
        self.assertEqual(self.processor.df.shape, (2, 3))

    def test_rename_columns(self):
        self.processor.process_data()
        expected_columns = ['nome', 'idade', 'cidade']
        self.assertListEqual(list(self.processor.df.columns), expected_columns)

    def test_convert_to_string(self):
        self.processor.process_data()
        self.assertTrue(all(self.processor.df.dtypes == 'object'))

    def test_upload_to_bigquery_with_invalid_table_name(self):
        with self.assertRaises(ValueError):
            self.processor.upload_to_bigquery('', 'project_id')

    def test_upload_to_bigquery_with_invalid_project_id(self):
        with self.assertRaises(ValueError):
            self.processor.upload_to_bigquery('table_name', '')

    def test_upload_to_bigquery_without_dataframe(self):
        processor = DataProcessor('invalid_path.xlsx')
        with self.assertRaises(Exception):
            processor.upload_to_bigquery('table_name', 'project_id')

if __name__ == '__main__':
    unittest.main()

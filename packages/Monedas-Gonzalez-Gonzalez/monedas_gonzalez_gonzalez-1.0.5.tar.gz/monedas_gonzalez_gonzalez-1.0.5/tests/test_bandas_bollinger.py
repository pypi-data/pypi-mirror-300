import unittest
import pandas as pd
from src.obtencion_datos import KrakenDataFetcher
from src.bandas_bollinger import CalculadorBandasBollinger

class TestBollingerBands(unittest.TestCase):

    def setUp(self):
        self.fetcher = KrakenDataFetcher()
        self.calculator = CalculadorBandasBollinger()

    def test_select_pair(self):
        # Prueba de un par válido
        selected_pair = '1'
        result = self.fetcher.pairs[selected_pair][0]
        self.assertEqual(result, 'XXBTZUSD')

    def test_fetch_ohlc_data(self):
        # Prueba si devuelve un DataFrame con la columna 'Close'
        pair = 'XXBTZUSD'
        df = self.fetcher.fetch_ohlc_data(pair)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Close', df.columns)

    def test_calculate_bollinger_bands(self):
        # Prueba el cálculo con datos simulados
        data = {
            'Time': pd.date_range(start='2023-01-01', periods=30, freq='h'),
            'Close': [i * 10 for i in range(1, 31)]
        }
        df = pd.DataFrame(data)

        df_result = self.calculator.calcular_bandas_bollinger(df)

        self.assertIn('SMA', df_result.columns)
        self.assertIn('Upper Band', df_result.columns)
        self.assertIn('Lower Band', df_result.columns)

    def test_run(self):
        # Prueba de integración para verificar el flujo completo
        pair = 'SOLUSD'
        df = self.fetcher.fetch_ohlc_data(pair)
        if df is not None:
            df = self.calculator.calcular_bandas_bollinger(df)
            self.assertIn('Close', df.columns)
            self.assertIn('Upper Band', df.columns)
            self.assertIn('Lower Band', df.columns)
            self.assertIn('Signal', df.columns)

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)

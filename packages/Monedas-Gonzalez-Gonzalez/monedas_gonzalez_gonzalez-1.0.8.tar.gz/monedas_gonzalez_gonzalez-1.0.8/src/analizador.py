from Monedas_Gonzalez_Gonzalez.obtencion_datos import KrakenDataFetcher
from Monedas_Gonzalez_Gonzalez.bandas_bollinger import CalculadorBandasBollinger
from Monedas_Gonzalez_Gonzalez.mostrador_datos import BollingerBandsPlotter


class AnalizadorBandasBollinger:
    def __init__(self):
        self.fetcher = KrakenDataFetcher()
        self.calculator = CalculadorBandasBollinger()
        self.plotter = BollingerBandsPlotter()

    def run(self):
        try:
            par = self.fetcher.select_pair()
            if par:
                df = self.fetcher.fetch_ohlc_data(par)
                if df is not None and not df.empty:
                    df = self.calculator.calcular_bandas_bollinger(df)

                    # Imprimir las últimas filas con señales y bandas
                    print(df[['Time', 'Close', 'Upper Band', 'Lower Band', 'Signal']].tail(20))

                    self.plotter.plot_bollinger_bands(df, par)
                else:
                    print("No se pudo obtener datos válidos para el par seleccionado.")
        except Exception as e:
            print(f"Error inesperado en el proceso de análisis: {e}")

import pandas as pd

class CalculadorBandasBollinger:
    def __init__(self, window=20, estrechamiento_factor=1.3, estrechamiento_ventana=20):
        self.window = window
        self.estrechamiento_factor = estrechamiento_factor
        self.estrechamiento_ventana = estrechamiento_ventana

    def calcular_bandas_bollinger(self, df):
        try:
            if df.empty:
                raise ValueError("El DataFrame está vacío. No se pueden calcular las bandas de Bollinger.")

            # Calcular la SMA y las bandas
            df['SMA'] = df['Close'].rolling(window=self.window).mean()
            df['STD'] = df['Close'].rolling(window=self.window).std()
            df['Upper Band'] = df['SMA'] + (df['STD'] * 2)
            df['Lower Band'] = df['SMA'] - (df['STD'] * 2)

            # Calcular el ancho de las bandas (Band Width)
            df['Band Width'] = df['Upper Band'] - df['Lower Band']

            # Calcular el promedio móvil del ancho de las bandas (Band Width) en una ventana más larga
            df['Avg Band Width'] = df['Band Width'].rolling(window=self.estrechamiento_ventana).mean()

            # Generar señales de compra/venta considerando el estrechamiento
            df['Signal'] = df.apply(
                lambda row: 'Compra' if row['Close'] < row['Lower Band'] and row['Band Width'] < row['Avg Band Width'] * self.estrechamiento_factor
                else ('Venta' if row['Close'] > row['Upper Band'] and row['Band Width'] < row['Avg Band Width'] * self.estrechamiento_factor
                      else 'Neutral'), axis=1
            )

            # Crear columnas para marcar los puntos de señal
            df['Buy Signal'] = df['Close'].where(df['Signal'] == 'Compra')
            df['Sell Signal'] = df['Close'].where(df['Signal'] == 'Venta')

            return df
        except ValueError as e:
            print(f"Error en los cálculos de las bandas: {e}")
            return None
        except Exception as e:
            print(f"Error al calcular las bandas de Bollinger: {e}")
            return None

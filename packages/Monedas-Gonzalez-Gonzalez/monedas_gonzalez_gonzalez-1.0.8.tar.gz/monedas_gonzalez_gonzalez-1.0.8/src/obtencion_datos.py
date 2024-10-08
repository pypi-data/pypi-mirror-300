import krakenex
import pandas as pd
import time


class KrakenDataFetcher:
    def __init__(self):
        self.k = krakenex.API()
        self.pairs = self.get_available_pairs()  # Llamar a la función para obtener los pares dinámicamente

    def get_available_pairs(self):
        try:
            # Llamada a la API de Kraken para obtener todos los pares de trading
            response = self.k.query_public('AssetPairs')
            if response.get('error'):
                print("Error:", response['error'])
                return {}

            # Extraer la información relevante de los pares de trading
            asset_pairs = response['result']
            pairs_dict = {}
            count = 1
            for pair_key, pair_info in asset_pairs.items():
                # Se puede filtrar solo por pares que tienen un tipo de intercambio como "USD", "EUR", etc.
                pairs_dict[str(count)] = (pair_key, pair_info['wsname'])
                count += 1

            return pairs_dict
        except Exception as e:
            print(f"Error al obtener los pares de Kraken: {e}")
            return {}

    def select_pair(self):
        while True:
            try:
                print("Selecciona la moneda que quieres analizar:")
                for key, (symbol, description) in self.pairs.items():
                    print(f"{key}: {symbol} ( {description} )")

                selected_key = input("Introduce el número de la moneda: ")

                if selected_key not in self.pairs:
                    print("Opción no válida. Por favor, introduce un número válido.")
                else:
                    return self.pairs[selected_key][0]
            except Exception as e:
                print(f"Error al seleccionar el par: {e}")

    def fetch_ohlc_data(self, pair):
        try:
            # Definimos el tiempo de inicio para obtener los datos de la última semana
            inicio_grafico = int(time.time()) - (7 * 24 * 60 * 60)
            params = {
                'pair': pair,
                'interval': 60,
                'since': inicio_grafico
            }
            ohlc_data = self.k.query_public('OHLC', params)
            if ohlc_data.get('error'):
                print("Error:", ohlc_data['error'])
                return None

            pair_key = list(ohlc_data['result'].keys())[0]
            df = pd.DataFrame(
                ohlc_data['result'][pair_key],
                columns=['Time', 'Open', 'High', 'Low', 'Close', 'vwap', 'Volume', 'Count']
            )
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            for col in ['Open', 'High', 'Low', 'Close', 'vwap', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        except KeyError as e:
            print(f"Error al procesar los datos: {e}")
            return None
        except Exception as e:
            print(f"Error al obtener los datos de Kraken: {e}")
            return None

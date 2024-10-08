import matplotlib.pyplot as plt

class BollingerBandsPlotter:
    def plot_bollinger_bands(self, df, pair):
        try:
            if df.empty:
                raise ValueError("El DataFrame está vacío. No se puede generar el gráfico.")

            plt.figure(figsize=(12, 6))
            plt.plot(df['Time'], df['Close'], label='Precio de Cierre', color='blue')
            plt.plot(df['Time'], df['SMA'], label='Media Móvil (SMA)', color='orange')
            plt.plot(df['Time'], df['Upper Band'], label='Banda Superior', color='green')
            plt.plot(df['Time'], df['Lower Band'], label='Banda Inferior', color='red')
            plt.fill_between(df['Time'], df['Lower Band'], df['Upper Band'], color='lightgrey', alpha=0.3)

            plt.scatter(df['Time'], df['Buy Signal'], label='Señal de Compra', marker='^', color='green', s=100)
            plt.scatter(df['Time'], df['Sell Signal'], label='Señal de Venta', marker='v', color='red', s=100)

            plt.title(f'Bandas de Bollinger para {pair}')
            plt.xlabel('Fecha')
            plt.ylabel('Precio')
            plt.legend()
            plt.show()
        except ValueError as e:
            print(f"Error al graficar: {e}")
        except Exception as e:
            print(f"Error inesperado al graficar las bandas de Bollinger: {e}")

from backends.obd_backend import OBDBackend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class PowerBalanceTest:
    def __init__(self):
        print("⚙️ Intentando conectar al dispositivo OBD2...")
        self.backend = OBDBackend()
        if not self.backend.connect():
            raise ConnectionError("❌ No se pudo conectar al dispositivo OBD2.")

    def read_cylinder_data(self):
        """
        Lee los datos de RPM para cada cilindro en tiempo real.
        """
        results = []
        for cyl in range(1, 9):
            rpm = self.backend.read_rpm()
            if rpm is not None:
                results.append(rpm.magnitude)  # Suponiendo que el valor tiene magnitud
            else:
                results.append(0)  # Valor predeterminado si falla la lectura
            time.sleep(0.5)  # Delay entre lecturas
        return results

    def animate(self, i, bars):
        """
        Función de animación para actualizar los datos en el gráfico.
        """
        print("🔄 Actualizando datos en tiempo real...")
        results = self.read_cylinder_data()
        for bar, value in zip(bars, results):
            bar.set_height(value)

    def run_test(self):
        """
        Ejecuta la prueba de balance de potencia con un gráfico animado.
        """
        print("🔄 Ejecutando prueba con gráfico animado...")
        fig, ax = plt.subplots()
        ax.set_title("Prueba de Balance de Potencia (Tiempo Real)")
        ax.set_xlabel("Cilindros")
        ax.set_ylabel("RPM")
        ax.set_ylim(0, 5000)  # Ajustar el rango de RPM según sea necesario
        bars = ax.bar(range(1, 9), [0] * 8, tick_label=[f"C{i}" for i in range(1, 9)])

        ani = FuncAnimation(fig, self.animate, fargs=(bars,), interval=1000)
        plt.show()

if __name__ == "__main__":
    test = PowerBalanceTest()
    test.run_test()
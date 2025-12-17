# simulator_backend.py
from simulator import simulate_f150

class SimulatorBackend:
    def __init__(self, weak_cyl=None, misfire_cyl=None, weakness=0.3, misfire_chance=0.2, noise_level=0.03):
        self.weak_cyl = weak_cyl
        self.misfire_cyl = misfire_cyl
        self.weakness = weakness
        self.misfire_chance = misfire_chance
        self.noise_level = noise_level

    def read_power_balance(self):
        """
        Devuelve un array con los valores de Power Balance simulados.
        """
        values = simulate_f150(
            weak_cyl=self.weak_cyl,
            misfire_cyl=self.misfire_cyl,
            weakness=self.weakness,
            misfire_chance=self.misfire_chance,
            noise_level=self.noise_level
        )
        return values

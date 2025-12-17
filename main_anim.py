# main_anim.py
from simulator import simulate_f150
from plotter import animate_power_balance

animate_power_balance(simulate_f150, weak_cyl=3, misfire_cyl=6, frames=100, interval=300)

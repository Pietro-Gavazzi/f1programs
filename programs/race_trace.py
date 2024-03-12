from lib2to3.pgen2.driver import Driver
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from timeit import default_timer
import pandas as pd
from fastf1 import plotting


fastf1.Cache.enable_cache("C:/Users/pietr/Documents/trop_long/projet-f1")


plotting.setup_mpl()

session = fastf1.get_session(2022, 'Belgium', 'Q')
session.load(laps=True)



for lap in session.pick_drivers([1]).iterlaps():
    lap = lap[1]
    print(lap['Time'])
    # break


import fastf1
fastf1.Cache.clear_cache("C:/Users/pietr/Documents/trop_long/projet-f1")

# Importamos las librerías que vamos a usar
import numpy as np
from shiny import render_plot, reactive
import pandas as pd
from shiny.express import input, render, ui
from pathlib import Path

# Cargamos nuestros datos
from palmerpenguins import load_penguins

# Creamos el título de la página, añadimos fillable para que los objetos rellenen la página
ui.page_opts(title="Dashboard de Pingüinos")

# Modulos
from info_page import info_page
from general_page import general_page
from scatter_page import scatter_page

@reactive.calc
def dat(): 
    locations = {
        "Torgersen": (-64.766667, -64.083333),
        "Dream": (-64.733333, -64.233333),
        "Biscoe": (-65.433333, -65.5),
    }
    df: pd.DataFrame = load_penguins() # type: ignore
    df['latitude'] = df['island'].apply(lambda x: locations[x][0] + np.random.normal(scale=0.005))
    df['longitude'] = df['island'].apply(lambda x: locations[x][1] + np.random.normal(scale=0.005))
    return df


info_page("Información", dat=dat)

general_page("general_info", dat=dat)
            
scatter_page("scatter_plots", dat=dat)

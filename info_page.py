from typing import Callable
import pandas as pd
import ipyleaflet as lf
from shiny.express import module, ui, render
from shiny.types import ImgData
from shinywidgets import render_widget

from pathlib import Path


@module
def info_page(input, output, session, dat: Callable[[], pd.DataFrame]):

    with ui.nav_panel("Descripción del Conjunto de Datos"):
        
        with ui.layout_column_wrap(width=1/2, height="500px"):
            with ui.card():
                ui.card_header("Descripción de datos")
                ui.markdown(
"""1. Datos generales
    - Especie: *Adelie*, *Gentoo* o *Chinstrap*
    - Isla
    - Peso (gramos)
    - Año de nacimiento
2. Descripción del pico
    - Longitud (mm)
    - Grosor vertical (mm)
3. Descripción de las aletas:
    - Longitud.
    """)

            with ui.card():
                @render.image
                def penguins_image():
                    p = Path(__file__).parent / "static/img/lter_penguins-2661170577.png"
                    i: ImgData = {"src": str(p), "height": "100%"}
                    return i

        with ui.card(full_screen=True, height="600px"):
            #### ipyleaflet
            @render_widget
            def leaflet_map():
                data = dat()
                m = lf.Map(
                    center = (data["longitude"].mean(), data["latitude"].mean()),
                    zoom = 7,
                )
                heatmap = lf.Heatmap(
                    locations = data[['latitude', 'longitude']].values.tolist(),
                    radius = 50,
                    )
                m.add(heatmap)
                return m
            
            #### Folium
            # @render.ui
            # def location_map():
            #     data = dat()
            #     m = folium.Map(
            #         # tiles="cartodb positron",
            #         location=(data["longitude"].mean(), data["latitude"].mean()),
            #         zoom_start=9,
            #     )
            #     heatmap_data = data[['latitude', 'longitude']].values
            #     HeatMap(heatmap_data).add_to(m)
            #     return m

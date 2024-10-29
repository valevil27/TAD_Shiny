from typing import Callable
import pandas as pd
from shiny import render
from shiny.express import module, ui
import faicons as fa
import seaborn as sns

sns.set()


@module
def general_page(input, output, session, dat: Callable[[], pd.DataFrame]):

    with ui.nav_panel("Visualización general"):
        # Creamos columnas para las value boxes
        with ui.layout_columns():

            # Creamos una Value Box, que presentará un valor importante
            with ui.value_box(showcase=fa.icon_svg("hashtag")):
                "Número de pingüinos"

                # Valor dinámico
                @render.ui
                def total_penguins():
                    return dat().shape[0]

            with ui.value_box(showcase=fa.icon_svg("feather-pointed")):
                "Tamaño medio de alas"

                @render.ui
                def mean_wings():
                    media = dat()["flipper_length_mm"].mean()
                    return f"{round(media)} mm"

            with ui.value_box(showcase=fa.icon_svg("weight-scale")):
                "Peso máximo"

                @render.ui
                def max_weight():
                    w = dat()["body_mass_g"].mean()
                    return f"{round(w):,} g".replace(",", ".")

        with ui.layout_column_wrap(width=1 / 2):
            # Creamos la ui del proyecto
            # La creación de la UI del proyecto se basa en contextos, usando with
            with ui.card():
                ui.card_header("Histograma")

                with ui.layout_sidebar():
                    with ui.sidebar(bg="#f8f8f8"):
                        "Filtros"
                        ui.input_selectize(
                            "var",
                            "Seleccionar variable",
                            [
                                "bill_length_mm",
                                "bill_depth_mm",
                                "flipper_length_mm",
                                "body_mass_g",
                                "year",
                            ],
                        )
                        ui.input_select("col", "Seleccionar color", choices=["none", "species", "sex", "island", "year"])
                        ui.input_numeric("bins", "Número de bins", 20)

                    @render.plot
                    def histogram_general():
                        ax = sns.histplot(
                            dat().dropna(),
                            x=input.var(),
                            bins=input.bins(),
                            hue=input.col() if input.col() != "none" else None,
                        )
                        return ax

            with ui.card():

                @render.data_frame
                def render_data():
                    return render.DataGrid(dat(), filters=True)

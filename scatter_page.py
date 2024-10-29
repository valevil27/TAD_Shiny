from typing import Callable
from shiny.express import module, ui, render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from shinywidgets import render_plotly, render_widget, as_widget

from pathlib import Path


@module
def scatter_page(input, output, session, dat: Callable[[], pd.DataFrame]):
    scalar_cols = [
        "bill_length_mm",
        "bill_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
    ]
    scalar_dic = {
        "bill_length_mm": "Bill Length (mm)",
        "bill_depth_mm": "Bill Depth (mm)",
        "flipper_length_mm": "Flipper Length (mm)",
        "body_mass_g": "Body mass (g)",
    }
    cat_cols = ["species", "island", "sex"]
    with ui.nav_panel("Visualización de Datos"):
        with ui.layout_columns(col_widths=[8, 4]):
            with ui.card(full_screen=True):
                ui.card_header("Scatterplot")

                @render_plotly
                def scatter_plotly():
                    scale = 10
                    s: pd.Series | None = (
                        dat().dropna()[input.s_pax()]
                        if input.s_pax() != "none"
                        else None
                    )
                    if s is not None:
                        s = (s - s.min()) / (s.max() - s.min())
                    ax = px.scatter(
                        dat().dropna(),
                        x=input.x_pax(),
                        y=input.y_pax(),
                        color=input.hue_pax() if input.hue_pax() != "none" else None,
                        symbol=(
                            input.shape_pax() if input.shape_pax() != "none" else None
                        ),
                        size=s,
                        size_max=5,
                        trendline="lowess" if input.trendline() else None,
                    )
                    ax.update_traces(marker={"size": 12})
                    return ax

            with ui.card():
                ui.card_header("Configuración del gráfico")
                ui.input_selectize(id="x_pax", label="Eje X", choices=scalar_cols)
                ui.input_selectize(
                    id="y_pax",
                    label="Eje Y",
                    choices=scalar_cols,
                    selected="bill_depth_mm",
                )
                ui.input_selectize(
                    id="hue_pax",
                    label="Color",
                    choices=["none", *cat_cols],
                    selected="none",
                )
                ui.input_selectize(
                    id="s_pax",
                    label="Tamaño",
                    choices=["none", *scalar_cols],
                    selected="none",
                )
                ui.input_selectize(
                    "shape_pax",
                    label="Forma",
                    choices=["none", *cat_cols],
                    selected="none",
                )
                ui.input_checkbox("trendline", label="Trendline", value=True)

        with ui.layout_columns(col_widths=[4, 8], height="600px"):
            with ui.card():
                ui.card_header("Configuración del gráfico")
                ui.input_selectize("x_bar", "Eje X", choices=cat_cols)
                ui.input_checkbox_group(
                    "y_bar", 
                    "Eje Y", 
                    scalar_dic, 
                    selected=f"{scalar_cols[0]}",
                )
                ui.input_selectize(
                    "stat_bar",
                    "Stat",
                    choices=["mean", "median", "max", "min", "count", "sum", "var"],
                )

            with ui.card():
                ui.card_header("Barplot")

                @render_plotly
                def barplot():
                    data = dat()
                    bars = list()
                    for y in input.y_bar():
                        ds = (
                            data.groupby(input.x_bar())[scalar_cols]
                            .agg(input.stat_bar())
                            .reset_index()
                        )
                        bars.append(
                            go.Bar(
                                name=scalar_dic[y],
                                x=ds[input.x_bar()],
                                y=ds[y],
                            )
                        )
                    fig = go.Figure(bars)
                    return fig

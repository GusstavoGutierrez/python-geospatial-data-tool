import plotly.express as px

def gerar_mapa_plotly(df):
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="nome",
        zoom=3,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.write_html("mapa.html", auto_open=False)

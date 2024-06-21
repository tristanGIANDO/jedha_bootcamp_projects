import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots


load_dotenv(find_dotenv("./.env"))

# Init database connection
engine = create_engine(os.getenv("RDS_ENDPOINT"), echo=True)
conn = engine.connect()

# Init pandas dataframes
weather_df = pd.read_sql("SELECT * FROM weather", conn)
cities_df = pd.read_sql("SELECT * FROM cities", conn)
hotels_df = pd.read_sql("SELECT * FROM hotels", conn)

conn.close()


def get_best_cities(filter_number: int = 5) -> pd.DataFrame:
    # Merge dataframes : weather_df["city_id"] -> cities_df["id"]
    merged_df = pd.merge(weather_df, cities_df,
                         left_on="city_id", right_on="id",
                         suffixes=("_weather", "_city"))
    merged_df = merged_df.drop(columns=["id_city", "id_weather"])  # duplicates

    # Best cities each day
    return merged_df.groupby("day_id", as_index=False) \
        .apply(
            lambda x: x.sort_values(
                by=["temp_max", "humidity", "clouds", "rain_prob"],
                ascending=[False, True, True, True]).head(filter_number)) \
        .reset_index(drop=True)


def get_best_hotels() -> pd.DataFrame:
    df = hotels_df.groupby("city_id", as_index=False) \
        .apply(
            lambda x: x.sort_values(
                by="rating", ascending=False).head(20)).reset_index()

    return df.drop(columns=["level_0", "level_1"])


def create_best_cities_figure(df: pd.DataFrame) -> go.Figure:
    # Top cities map
    cities_map = go.Figure(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longitude"],
        text=df["city"],
        mode="markers",
        marker=dict(
            size=df["temp_max"],
            color=df["temp_max"],
            colorscale="Bluered",
            showscale=True,
            sizemode="area",
            sizeref=2.*max(df['temp_max'])/(35.**2),
            sizemin=4
        )
    ))

    cities_map.update_layout(
        mapbox=dict(
            style='open-street-map',
            zoom=5,
            center=dict(lat=df['latitude'].mean(),
                        lon=df['longitude'].mean())
        ),
        title={
            "text": "<b>Top 5 destinations orecast</b>",
            "x": 0.5
        },
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return cities_map


def create_best_hotels_figure(df: pd.DataFrame) -> go.Figure:
    coords_df = df.groupby("city_id") \
                   .agg({"latitude": "mean", "longitude": "mean"}) \
                   .reset_index()

    # Création de la carte initiale avec les hôtels marqués
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            text=df["name"],
            mode="markers",
            marker=dict(
                size=df["rating"],
                color=df["rating"],
                colorscale="Bluered",
                showscale=True,
                sizemode="area",
                sizeref=2.*max(df['rating'])/(35.**2),
                sizemin=4
            )
        )
    )

    # Définition de la mise en page initiale de la carte
    fig.update_layout(
        title=go.layout.Title(text="Top 20 best hotels", x=0.5),
        showlegend=True,
        mapbox=dict(
            style="open-street-map",
            zoom=5,
            center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean())
        )
    )

    # Création des boutons pour chaque ville
    buttons = [
        go.layout.updatemenu.Button(
            label=str(r["city_id"]),
            method="update",
            args=[{"visible": True}, {
                "mapbox": {
                    "style": "open-street-map",
                    "zoom": 12,
                    "center": {"lat": r["latitude"], "lon": r["longitude"]}
                }
            }]
        ) for _, r in coords_df.iterrows()
    ]

    # Ajout des boutons à la mise en page de la figure
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(buttons=buttons)]
    )

    return fig


"""
top_cities_df = get_best_cities()
top_cities_fig = create_best_cities_figure(top_cities_df)
"""
top_hotels_df = get_best_hotels()
top_hotels_fig = create_best_hotels_figure(top_hotels_df)
top_hotels_fig.show()

# # Create subplots
# fig = make_subplots(
#     rows=1, cols=2,
#     column_widths=[0.5, 0.5],
#     specs=[[{"type": "scattermapbox"}, {"type": "scattermapbox"}]]
# )

# for trace in top_cities_fig.data:
#     fig.add_trace(trace, row=1, col=1)

# fig.update_layout(
#     height=800,
#     mapbox1=dict(
#         style="open-street-map",
#         zoom=5,
#         center=dict(lat=top_cities_df['latitude'].mean(),
#                     lon=top_cities_df['longitude'].mean())
#     ),
#     mapbox2=dict(
#         style="open-street-map",
#         zoom=5,
#         center=dict(lat=top_cities_df['latitude'].mean(),
#                     lon=top_cities_df['longitude'].mean())
#     ),
#     title={
#         "text": "<b>Top 5 destinations according to the weather forecast</b>",
#         "x": 0.5},
#     margin={"r": 0, "t": 50, "l": 0, "b": 0}
# )

# fig.show()


# if __name__ == "__main__":
#     df = get_best_hotels()
#     coords_df = df.groupby("city_id") \
#         .agg({"latitude": "mean", "longitude": "mean"}) \
#         .reset_index()

#     print(len(coords_df))

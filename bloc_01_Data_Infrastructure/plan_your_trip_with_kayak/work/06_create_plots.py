import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go


load_dotenv(find_dotenv("./.env"))

# Init database connection
engine = create_engine(os.getenv("RDS_ENDPOINT"), echo=True)
conn = engine.connect()

# Init pandas dataframes
weather_df = pd.read_sql("SELECT * FROM weather", conn)
cities_df = pd.read_sql("SELECT * FROM cities", conn)
hotels_df = pd.read_sql("SELECT * FROM hotels", conn)

conn.close()


def get_best_cities() -> pd.DataFrame:
    # Merge dataframes : weather_df["city_id"] -> cities_df["id"]
    merged_df = pd.merge(weather_df, cities_df,
                         left_on="city_id", right_on="id",
                         suffixes=("_weather", "_city"))
    merged_df = merged_df.drop(columns=["id_city", "id_weather"])  # duplicates

    avg_df = merged_df.groupby(["city_id", "city", "latitude", "longitude"]) \
        .agg({"temp_max": "mean",
              "humidity": "mean",
              "clouds": "mean",
              "rain_prob": "mean"}) \
        .reset_index()

    avg_df = avg_df.sort_values(
        by=["temp_max", "humidity", "clouds", "rain_prob"],
        ascending=[False, True, True, True]).head(10)

    return avg_df

    # Best cities each day
    # return merged_df.groupby("day_id", as_index=False) \
    #     .apply(
    #         lambda x: x.sort_values(
    #             by=["temp_max", "humidity", "clouds", "rain_prob"],
    #             ascending=[False, True, True, True]).head(5)) \
    #     .reset_index(drop=True)


def get_best_hotels() -> pd.DataFrame:
    df = hotels_df.groupby("city_id", as_index=False) \
        .apply(
            lambda x: x.sort_values(
                by="rating", ascending=False).head(20)).reset_index()

    return df.drop(columns=["level_0", "level_1"])


def create_best_cities_figure(df: pd.DataFrame) -> go.Figure:
    cities_map = go.Figure(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longitude"],
        text=df["city"],
        mode="markers",
        marker=dict(
            size=df["temp_max"],
            color=df["temp_max"],
            colorscale="bluered",
            showscale=True,
            colorbar=dict(title="Max Temperature"),
            sizemode="area",
            sizeref=2.*max(df['temp_max'])/(35.**2),
            sizemin=4
        )
    ))

    cities_map.update_layout(
        mapbox=dict(
            style='open-street-map',
            zoom=5,
            center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean())
        ),
        title={
            "text": "<b>The best destinations for the next 7 days according to the weather forecast</b>",
            "x": 0.5
        },
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return cities_map


def create_best_hotels_figure(df: pd.DataFrame) -> go.Figure:
    coords_df = df.groupby("city_id") \
                   .agg({"latitude": "mean", "longitude": "mean"}) \
                   .reset_index()
    # need to attribute the city name to its id again
    coords_df = coords_df.merge(cities_df[['id', 'city']],
                                left_on='city_id', right_on='id',
                                how='left')
    coords_df.drop('id', axis=1, inplace=True)

    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            text='<b>' + df["name"] + "</b><br>" + df["rating"].astype(str) + "/10",
            mode="markers",
            marker=dict(
                size=df["rating"],
                color=df["rating"],
                colorscale="hot",
                showscale=True,
                sizemode="area",
                sizeref=2.*max(df['rating'])/(35.**2),
                sizemin=1
            )
        )
    )

    fig.update_layout(
        title=go.layout.Title(text="<b>Top 20 best hotels</b>", x=0.5),
        showlegend=False,
        mapbox=dict(
            style="open-street-map",
            zoom=5,
            center=dict(lat=df["latitude"].mean(), lon=df["longitude"].mean())
        )
    )

    buttons = [
        go.layout.updatemenu.Button(
            label=str(r["city"]),
            method="update",
            args=[
                {"visible": True},
                {"mapbox": {
                    "style": "open-street-map",
                    "zoom": 12,
                    "center": {"lat": r["latitude"], "lon": r["longitude"]}}}]
        ) for _, r in coords_df.iterrows()
    ]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(buttons=buttons)]
    )

    return fig


df_cities = get_best_cities()
fig_cities = create_best_cities_figure(df_cities)

df_hotels = get_best_hotels()
fig_hotels = create_best_hotels_figure(df_hotels)

fig_cities.show()
fig_hotels.show()

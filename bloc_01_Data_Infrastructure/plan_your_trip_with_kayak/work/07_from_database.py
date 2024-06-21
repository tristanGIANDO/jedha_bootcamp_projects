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


top_cities_df = get_best_cities()

# Top cities map
cities_map = go.Figure(go.Scattermapbox(
    lat=top_cities_df['latitude'],
    lon=top_cities_df['longitude'],
    text=top_cities_df['city'],
    mode='markers',
    marker=dict(
        size=top_cities_df['temp_max'],
        color=top_cities_df['temp_max'],
        colorscale='Bluered',
        showscale=True,
        sizemode='area',
        sizeref=2.*max(top_cities_df['temp_max'])/(35.**2),
        sizemin=4
    )
))

cities_map.update_layout(
    mapbox=dict(
        style='open-street-map',
        zoom=5,
        center=dict(lat=top_cities_df['latitude'].mean(),
                    lon=top_cities_df['longitude'].mean())
    ),
    title={
        "text": "<b>Top 5 destinations according to the weather forecast</b>",
        "x": 0.5
    },
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

# Top hotels map
hotels_map = go.Figure(go.Scattermapbox(
    lat=top_cities_df['latitude'],
    lon=top_cities_df['longitude'],
    text=top_cities_df['city'],
    mode='markers',
    marker=dict(
        size=top_cities_df['temp_max'],
        color=top_cities_df['temp_max'],
        colorscale='Bluered',
        showscale=True,
        sizemode='area',
        sizeref=2.*max(top_cities_df['temp_max'])/(35.**2),
        sizemin=4
    )
))

hotels_map.update_layout(
    mapbox=dict(
        style='open-street-map',
        zoom=5,
        center=dict(lat=top_cities_df['latitude'].mean(), lon=top_cities_df['longitude'].mean())
    ),
    updatemenus=[{
        'buttons': [
            {'label': 'Option 1', 'method': 'update', 'args': [{'visible': [True, False]}]},
            {'label': 'Option 2', 'method': 'update', 'args': [{'visible': [False, True]}]},
        ],
        'direction': 'down',
        'showactive': True,
    }],
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    specs=[[{"type": "scattermapbox"}, {"type": "scattermapbox"}]]
)

# Ajouter les traces des cartes à la figure combinée
for trace in cities_map.data:
    fig.add_trace(trace, row=1, col=1)

for trace in hotels_map.data:
    fig.add_trace(trace, row=1, col=2)

# Mettre à jour la disposition de la figure combinée
fig.update_layout(
    height=800,
    mapbox1=dict(
        style="open-street-map",
        zoom=5,
        center=dict(lat=top_cities_df['latitude'].mean(), lon=top_cities_df['longitude'].mean())
    ),
    mapbox2=dict(
        style="open-street-map",
        zoom=5,
        center=dict(lat=top_cities_df['latitude'].mean(), lon=top_cities_df['longitude'].mean())
    ),
    title={"text": "<b>Top 5 destinations according to the weather forecast</b>", "x": 0.5},
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

fig.show()



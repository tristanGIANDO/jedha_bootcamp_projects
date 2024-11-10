# Les interets partages sont-ils plus importants qu’une origine raciale
# partagee ?

import pandas as pd
import envs
import plotly.express as px
from plotly.subplots import make_subplots

df = pd.read_csv(envs.DATASET, encoding="latin1")

# keep interesting columns only
filtered_columns = ["iid", "samerace", "shar7_2", "shar7_3", "dec_o"]
filtered_columns = [col for col in filtered_columns if col in df.columns]
df = df[filtered_columns]


# count number of yes decisions according to 'race'
origins_df = df.groupby("samerace")["dec_o"].sum().reset_index()
# but each participant is mentioned 10 times
origins_df["dec_o_iid"] = origins_df["dec_o"].apply(lambda x: x//10)
# cleaning rows names, dtypes
origins_df["samerace"] = origins_df["samerace"].astype(str)
origins_df.at[0, "samerace"] = "different origins"
origins_df.at[1, "samerace"] = "shared origins"


# count number of yes according to shared interests median
df["shar_mean"] = (df["shar7_2"] + df["shar7_3"]) / 2
shar_score_df = df.groupby("shar_mean")["dec_o"].sum().reset_index()

median = shar_score_df["shar_mean"].median()
lower_df = shar_score_df[shar_score_df["shar_mean"] < median]
higher_df = shar_score_df[shar_score_df["shar_mean"] > median]

data = [
    {"shar": "different interests", "dec_o": lower_df["dec_o"].sum()},
    {"shar": "shared interests", "dec_o": higher_df["dec_o"].sum()}
    ]
shar_df = pd.DataFrame(data)


# create plots
fig1 = px.bar(origins_df, x="samerace", y="dec_o_iid",
              color="samerace",
              color_discrete_map={
                  "different origins": envs.TINDER_ORANGE,
                  "shared origins": envs.TINDER_PINK},
              labels={
                  "samerace": "Number of 'yes' decisions about meeting again"})
fig2 = px.bar(shar_df, x="shar", y="dec_o",
              color="shar",
              color_discrete_map={
                  "different interests": envs.TINDER_ORANGE,
                  "shared interests": envs.TINDER_PINK},
              labels={
                  "shar": "Number of 'yes' decisions about meeting again"})

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=(
                        "Number of second dates by origin",
                        "Number of second dates by area of interest"))

for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    fig.add_trace(trace, row=1, col=2)

fig.update_layout(
    title={
        "text": "<b>Are shared interests more important than a shared racial background?</b>",
        "x": 0.5
        },
    showlegend=False)

fig.show()

# coding utf-8
# Les gens peuvent-ils predire avec précision leur propre valeur perçue sur le
# marche des rencontres ?

import pandas as pd
import envs
import plotly.graph_objects as go

df = pd.read_csv(envs.DATASET, encoding="latin1")
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]

# iid = member id
# pid = partner id
# reduce dataframe
filtered_columns = ["iid", "pid", "attr_o", "attr5_2", "attr5_3"]
filtered_columns = [col for col in filtered_columns if col in df.columns]
df = df[filtered_columns]

# moyenne des notes que les participants pensent avoir
df["estimated"] = (df["attr5_2"] + df["attr5_3"]) / 2
estim_df = df.groupby("iid")["estimated"].mean().reset_index()

# moyenne des notes attribuees a chaque partenaire (pid vaut attr_o)
note_df = df.groupby("pid")["attr_o"].mean().reset_index()
estim_df["note"] = note_df["attr_o"]

fig = go.Figure()

fig.add_trace(go.Box(
    y=estim_df["estimated"].dropna(),
    name="Perceived value",
    marker_color=envs.TINDER_ORANGE
))

fig.add_trace(go.Box(
    y=estim_df["note"],
    name="Assigned value",
    marker_color=envs.TINDER_GREY
))

fig.update_layout(
    title={
        "text": "<b>Can people accurately predict their own perceived value in the dating market?</b>",
        "x": 0.5},
    yaxis_title="Score"
)

# Affichage du graphique
fig.show()

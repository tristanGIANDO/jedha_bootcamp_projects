import pandas as pd
import envs
import plotly.express as px

df = pd.read_csv(envs.DATASET, encoding="latin1")

filtered_columns = ["iid", "goal"]

df = df.groupby("iid")["goal"].value_counts().reset_index()
df = df.groupby("goal")["iid"].count().reset_index()

for i, nice_name in enumerate(["Seemed like a fun night out",
                               "To meet new people",
                               "To get a date",
                               "Looking for a serious relationship",
                               "To say I did it",
                               "Other"], start=1):
    df["goal"] = df["goal"].replace(i, nice_name)

fig = px.pie(df, names="goal", values="iid",
             color="goal",
             color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_traces(textposition="inside", textinfo="label+percent")

fig.update_layout(
    title={
        "text": "<b>Participants' goals</b>",
        "x": 0.5,
        "y": 0.8
        },
    showlegend=False
)

fig.show()

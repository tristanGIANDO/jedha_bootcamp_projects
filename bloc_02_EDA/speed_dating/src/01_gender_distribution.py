import pandas as pd
import plotly.express as px
import envs

df = pd.read_csv(envs.DATASET, encoding="latin1")

print(len(set(df["iid"])))

df = df.groupby("iid")["gender"].mean().reset_index()
female = df[df["gender"] == 0]
male = df[df["gender"] == 1]

print(len(female), len(male))
df = pd.DataFrame([{"gender": "female", "count": len(female)},
                   {"gender": "male", "count": len(male)}])
fig = px.pie(df,
             names="gender",
             values="count",
             color_discrete_sequence=[envs.TINDER_ORANGE])

fig.update_layout(
    title={
        "text": "<b>Gender distribution<b>",
        "x": 0.5
        }
)
fig.show()

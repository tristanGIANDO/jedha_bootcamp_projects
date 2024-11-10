# Is it better to be someone's first speed date or their last?

import pandas as pd
import envs
import plotly.express as px

df = pd.read_csv(envs.DATASET, encoding="latin1")

filtered_columns = ["id", "wave", "dec_o"]
filtered_columns = [col for col in filtered_columns if col in df.columns]
df = df[filtered_columns]

mean_decision = df.groupby("id")["dec_o"].sum().reset_index()

fig = px.histogram(mean_decision,
                   x="id",
                   y="dec_o",
                   nbins=22,
                   color_discrete_sequence=[envs.TINDER_ORANGE],
                   labels={
                       "id": "Rounds",
                       "dec_o": "Number of 'yes' decisions about meeting again"
                    })

fig.update_layout(
    title={
        "text": "<b>Is it better to be someone's first speed date or their last?<b>",
        "x": 0.5
        }
)

fig.show()

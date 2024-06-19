import pandas as pd
import plotly.express as px

import envs
# quel est l'attribut qui a eu le plus de oui ? le moins de oui ?

"""
What are the least desirable attributes in a male partner?
Does this differ for female partners?

Donc en gros, il faut filtrer les attributs
et les trier en fonction de la decision prise
par exemple : 30% ambitious disent oui mais 50% disent non ?
"""


FEMALE = 0
MALE = 1

df = pd.read_csv(envs.DATASET, encoding="latin1")
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]

# 1. Faire un masque pour separer hommes et femmes
df = df[df["gender"] == 0]

attributes = {"attr7_2": "Attractive",
              "sinc7_2": "Sincere",
              "intel7_2": "Intelligent",
              "fun7_2": "Fun",
              "amb7_2": "Ambitious",
              "shar7_2": "Shared Interests"}

data = []
for df_attr, nice_name in attributes.items():
    filtered_df = df[df[f"{df_attr}_adj"].notna()]
    mean_attr = filtered_df[f"{df_attr}_adj"].mean() * 10  # *10 -> percentage
    data.append({"attr": nice_name, "mean": mean_attr})

fig_df = pd.DataFrame(data)
fig_df = fig_df.sort_values(by="mean", ascending=False)

fig = px.bar(fig_df, x="attr", y="mean",
             range_y=[0, 30],
             title="Most desirable attributes",
             color_discrete_sequence=["#fd5564"]
             )

fig.show()

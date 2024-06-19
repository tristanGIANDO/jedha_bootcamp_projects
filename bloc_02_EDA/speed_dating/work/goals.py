# coding utf-8
# Les gens peuvent-ils predire avec précision leur propre valeur perçue sur le
# marche des rencontres ?

import pandas as pd
import envs
import plotly.express as px

df = pd.read_csv(envs.DATASET, encoding="latin1")
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]

filtered_columns = ["iid", "pid", "goal", "dec_o"]
filtered_columns = [col for col in filtered_columns if col in df.columns]
df = df[filtered_columns]
for i, nice_name in enumerate(["Seemed like a fun night out",
                               "To meet new people",
                               "To get a date",
                               "Looking for a serious relationship",
                               "To say I did it",
                               "Other"], start=1):
    df["goal"] = df["goal"].replace(i, nice_name)

positive_decisions = df[df["dec_o"] == 1]
goal_yes_counts = positive_decisions["goal"].value_counts().reset_index()
goal_yes_counts.rename(columns={"count": "y"}, inplace=True)

negative_decisions = df[df["dec_o"] == 0]
goal_no_counts = negative_decisions["goal"].value_counts().reset_index()
goal_no_counts.rename(columns={"count": "n"}, inplace=True)

df = goal_yes_counts.merge(goal_no_counts)

df["total"] = df["y"] + df["n"]
df["Yes"] = (df["y"] / df["total"] * 100).round(1)
df["No"] = (df["n"] / df["total"] * 100).round(1)

df_melted = df.melt(id_vars="goal",
                    value_vars=["Yes", "No"],
                    var_name="Response",
                    value_name="Percentage")
df_melted = df_melted.sort_values(by="Percentage", ascending=True)

fig = px.bar(df_melted, x="Percentage", y="goal",
             color="Response",
             color_discrete_sequence=[envs.TINDER_ORANGE, envs.TINDER_GREY],
             title="<b>Yes/No responses for each goal about a second date</b>",
             barmode="stack",
             text="Percentage")

fig.update_traces(texttemplate="%{text}%", textposition="inside")

fig.show()

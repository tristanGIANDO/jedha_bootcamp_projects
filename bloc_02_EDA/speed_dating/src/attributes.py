import pandas as pd
import envs
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv(envs.DATASET, encoding="latin1")
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]


def compute(d, gender: int):
    d = d[d["gender"] == gender]

    # keep interesting columns only
    attrs = ["attr", "sinc", "intel", "fun", "amb", "shar"]
    for attr in attrs:
        columns = [col for col in d.columns if col.startswith(attr)]
        d[f"{attr}_mean"] = d[columns].mean(axis=1)

    d["attr_higher"] = d[[f"{attr}_mean" for attr in attrs]].idxmax(axis=1)
    d["attr_higher"] = d["attr_higher"].str.replace("_mean", "")

    no_responses = d[d["dec_o"] == 1]
    no_count = no_responses.groupby("attr_higher")["dec_o"].count()

    # ratio of "no"
    total_count = d.groupby("attr_higher")["dec_o"].count()
    no_ratio = no_count / total_count
    least_successful_attr = no_ratio.idxmax()

    d = no_ratio.reset_index()
    for i, nice_name in enumerate(["Ambitious", "Attractive",
                                   "Fun", "Intelligence",
                                   "Shared Interests", "Sincere"]):
        d.at[i, "attr_higher"] = nice_name

    d = d.sort_values(by="dec_o", ascending=False)

    return d


dw = compute(df, 0, envs.TINDER_PINK, "Women")
dm = compute(df, 1, envs.TINDER_GREY, "Men")

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("According to women",
                                    "According to men"))

fig.add_trace(
    go.Bar(
        x=dw["attr_higher"],
        y=dw["dec_o"],
        name="Women",
        marker_color=[envs.TINDER_ORANGE for i in range(6)],
    ),
    row=1,
    col=1)

fig.add_trace(
    go.Bar(
        x=dm["attr_higher"],
        y=dm["dec_o"],
        name="Men",
        marker_color=[envs.TINDER_PINK for i in range(6)],
    ),
    row=1,
    col=2)

fig.update_layout(
    title={"text": "<b>The most desirable attributes</b>",
           "x": 0.5},
    showlegend=False)
fig.update_yaxes(title_text="Ratio", row=1, col=1)
fig.update_yaxes(title_text="Ratio", row=1, col=2)

fig.show()

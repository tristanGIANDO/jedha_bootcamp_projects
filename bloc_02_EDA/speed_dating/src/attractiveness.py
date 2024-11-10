# How important do people think attractiveness is in potential mate selection
# vs. its real impact?

import pandas as pd
import envs
import plotly.express as px


def conform_data(attributes: list, status: str) -> None:
    """
    Convert data to mean and fill missing values.

    Args:
        attributes: List of attributes to conform
        status: Status of the data

     Returns:
        A list of dictionaries with mean and fill missing values
    """
    d = []
    for attr in attributes:
        df[attr] = df[attr].fillna(df[attr].mean())
        mean = df[attr].mean()
        d.append({"status": status, "name": attr, "mean": mean})
    return d


# the attributes to filter
potential_attributes = ["attr1_s", "attr1_2", "attr1_3"]
real_attributes = ["attr7_2", "attr7_3"]

# init and clean dataframe
df = pd.read_csv(envs.DATASET, encoding="latin1")
df = df[~((df["wave"] > 5) & (df["wave"] < 10))]

data = []
data += conform_data(potential_attributes, "Estimated")
data += conform_data(real_attributes, "Reality")

# init a new dataframe with filtered data only
fig_df = pd.DataFrame(data)
fig_df = fig_df.groupby("status")["mean"].mean().reset_index()

# create plot
fig = px.bar(fig_df, y="status", x="mean",
             range_x=[0, 100],
             color_discrete_sequence=[envs.TINDER_ORANGE],
             text="mean",
             labels={
                 "status": " ",
                 "mean": "Mean Percentage"},
             category_orders={
                 "status": fig_df["status"][::-1]  # invert data
                 })

fig.update_traces(
    texttemplate="<b>%{text:.2f}%</b>",  # bold text
    textposition="outside"  # outside the bar
)
fig.update_layout(
    title={
        "text": "<b>Estimated level of attractiveness vs. real impact<b>",
        "y": 0.9,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top"}
)

fig.show()

DATASET = r"resources\Speed+Dating+Data.csv"
TINDER_ORANGE = "#fd5564"
TINDER_GREY = "#424242"
TINDER_PINK = "#ef4a75"


def adjust_column(df, column_name: str):
    return df.apply(lambda x: x[column_name] / 10
                    if x["wave"] < 6 or x["wave"] > 9
                    else x[column_name],
                    axis=1)

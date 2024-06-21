import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("./.env"))

BUCKET_NAME = "tgiandoriggio-bucket-kayak-01"

root = r"C:\Users\giand\OneDrive\Documents\__packages__\jedha\jedha_bootcamp_projects\bloc_01_Data_Infrastructure\plan_your_trip_with_kayak\work\csv_files"

filenames = ["weather_data.csv",
             "hotel_data.csv"]

for file in filenames:
    path = f"{root}/{file}"
    if not os.path.isfile(path):
        raise ValueError()

    data = pd.read_csv(path)
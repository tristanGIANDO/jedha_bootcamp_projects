import os
import boto3
import pandas as pd
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("./.env"))

BUCKET_NAME = "tgiandoriggio-bucket-kayak-01"
KEYS = ["weather_data.csv", "hotel_data.csv"]


def get_dataframes_from_s3() -> list[pd.DataFrame, pd.DataFrame]:
    # init session and bucket
    session = boto3.Session(aws_access_key_id=os.getenv("AWS_KEY"),
                            aws_secret_access_key=os.getenv("AWS_SECRET"))

    s3 = session.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)

    dataframes = []
    for obj in bucket.objects.all():
        file_key = obj.key
        file_path = "C:/Users/giand/AppData/Local/Temp/" + file_key

        try:
            bucket.download_file(file_key, file_path)
            dataframes.append(pd.read_csv(file_path))

        except Exception as e:
            print(f"{file_key} -> {e}")

    return dataframes


hotel_df, weather_df = get_dataframes_from_s3()

print(hotel_df.head())
print(weather_df.head())

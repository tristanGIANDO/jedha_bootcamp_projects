import pandas as pd

"""
Gets the JSON file generated by Booking's scraping and creates a CSV file
"""

input_path = r"C:\Users\giand\OneDrive\Documents\__packages__\jedha\jedha_bootcamp_projects\bloc_01_Data_Infrastructure\plan_your_trip_with_kayak\work\booking_scraper\booking_scraper\hotels.json"
output_path = r"C:\Users\giand\OneDrive\Documents\__packages__\jedha\jedha_bootcamp_projects\bloc_01_Data_Infrastructure\plan_your_trip_with_kayak\work\csv_files\hotel_data.csv"

with open(input_path, "r", encoding="utf-8") as file:
    hotel_content = file.read()

df = pd.DataFrame(eval(hotel_content))
df.to_csv(output_path, index=False, encoding="utf-8")

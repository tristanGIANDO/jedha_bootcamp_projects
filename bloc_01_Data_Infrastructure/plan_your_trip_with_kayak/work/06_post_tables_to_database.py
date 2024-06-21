from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

load_dotenv(find_dotenv("./.env"))

# Initialize database connection
database_url = os.getenv("RDS_ENDPOINT")
if not database_url:
    raise ValueError("Please set the RDS_ENDPOINT environment variable.")

engine = create_engine(database_url, echo=True)
Base = declarative_base()
conn = engine.connect()


# Create tables


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    weather = relationship("Weather", back_populates="city_rel")
    hotels = relationship("Hotel", back_populates="city_rel")


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    day_id = Column(Integer)
    temp = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    clouds = Column(Integer)
    rain_prob = Column(Float)
    city_rel = relationship("City", back_populates="weather")


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name = Column(String)
    url = Column(String)
    rating = Column(Float)
    address = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    city_rel = relationship("City", back_populates="hotels")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Read CSV files
root = Path(r"C:\Users\giand\OneDrive\Documents\__packages__\jedha\jedha_bootcamp_projects\bloc_01_Data_Infrastructure\plan_your_trip_with_kayak\work\csv_files")


def read_csv(file: Path) -> pd.DataFrame:
    if not file.is_file():
        raise FileExistsError()
    return pd.read_csv(file)


def clean_city_name(city_name: str) -> str:
    return city_name.lower().replace(" ", "").replace("%20", "")


weather_df = read_csv(root / "weather_data.csv")
hotel_df = read_csv(root / "hotel_data.csv")

# Insert City data
weather_df["city"] = weather_df["city"].apply(clean_city_name)
cities = weather_df[
    ["city_id", "city", "lat", "lon"]
    ].drop_duplicates().to_dict(orient="records")

for city in cities:
    city_record = City(id=city["city_id"],
                       city=city["city"],
                       latitude=city["lat"],
                       longitude=city["lon"])
    session.add(city_record)

# Insert Weather data
for i, row in weather_df.iterrows():
    weather = Weather(id=i,
                      city_id=row["city_id"],
                      day_id=row["day_id"],
                      temp=row["temp"],
                      temp_min=row["temp_min"],
                      temp_max=row["temp_max"],
                      humidity=row["humidity"],
                      clouds=row["clouds"],
                      rain_prob=row["rain_prob"])
    session.add(weather)

# Insert Hotel data
hotel_df["city"] = hotel_df["city"].apply(clean_city_name)

for i, row in hotel_df.iterrows():
    city = session.query(City).filter_by(city=row["city"]).first()
    try:
        hotel = Hotel(id=i,
                      city_id=city.id,
                      name=row["name"],
                      url=row["url"],
                      rating=row["rating"],
                      address=row["address"],
                      description=row["description"],
                      latitude=row["latitude"],
                      longitude=row["longitude"])
        session.add(hotel)
    except Exception as e:
        print(e)
        continue

session.commit()


# Testing request
result = conn.execute(text("""
    SELECT h.name, h.rating, w.temp
    FROM hotels h
    JOIN weather w ON h.city_id = w.city_id
    WHERE w.day_id = 1
"""))

for row in result:
    print(row)

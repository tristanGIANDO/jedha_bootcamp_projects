import scrapy

CITIES = [
    "Mont Saint Michel",
    "St Malo",
    "Bayeux",
    "Le Havre",
    "Rouen",
    "Paris",
    "Amiens",
    "Lille",
    "Strasbourg",
    "Chateau du Haut Koenigsbourg",
    "Colmar",
    "Eguisheim",
    "Besancon",
    "Dijon",
    "Annecy",
    "Grenoble",
    "Lyon",
    "Gorges du Verdon",
    "Bormes les Mimosas",
    "Cassis",
    "Marseille",
    "Aix en Provence",
    "Avignon",
    "Uzes",
    "Nimes",
    "Aigues Mortes",
    "Saintes Maries de la mer",
    "Collioure",
    "Carcassonne",
    "Ariege",
    "Toulouse",
    "Montauban",
    "Biarritz",
    "Bayonne",
    "La Rochelle"
]


class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    cities = ["montpellier"]
    start_urls = [f"https://www.booking.com/searchresults.html?ss={city}" for city in CITIES]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "ROBOTSTXT_OBEY": False
    }

    def parse(self, response):
        hotels = response.css('div[data-testid="property-card"]')

        for hotel in hotels:
            city = response.url.split("=")[-1]
            name = hotel.css('div[data-testid="title"]::text').get().strip()
            rating = hotel.css("div.f13857cc8c.e008572b71::text").get()
            if not rating:
                rating = "0.0"
            url = hotel.css('a[data-testid="title-link"]::attr(href)').get()

            yield response.follow(url, callback=self.parse_hotel_detail,
                                  meta={"name": name,
                                        "rating": rating,
                                        "city": city
                                        })

        next_page = response.css("a.bui-pagination__link.pagenext::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_hotel_detail(self, response):
        city = response.meta["city"]
        name = response.meta["name"]
        url = response.url
        rating = response.meta["rating"]
        address = response.css("span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text").get().strip()
        description = response.css('p[data-testid="property-description"]::text').get().strip()
        coordinates = response.css("a#hotel_address::attr(data-atlas-latlng)").get()

        if coordinates:
            latitude, longitude = coordinates.split(",")
            latitude = float(latitude)
            longitude = float(longitude)
        else:
            latitude = None
            longitude = None

        yield {
            "city": city,
            "name": name,
            "url": url,
            "rating": rating,
            "address": address,
            "description": description,
            "latitude": latitude,
            "longitude": longitude
        }

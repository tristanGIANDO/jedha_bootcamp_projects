import scrapy


class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = [
        "https://www.booking.com/searchresults.html?ss=Montpellier"
    ]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "ROBOTSTXT_OBEY": False
    }

    def parse(self, response):
        hotels = response.css('div[data-testid="property-card"]')

        for hotel in hotels:
            name = hotel.css('div[data-testid="title"]::text').get().strip()
            rating = hotel.css("div.f13857cc8c.e008572b71::text").get()
            url = hotel.css('a[data-testid="title-link"]::attr(href)').get()

            yield response.follow(url, callback=self.parse_hotel_detail,
                                  meta={"name": name,
                                        "rating": rating,
                                        "url": url})

        next_page = response.css("a.bui-pagination__link.pagenext::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_hotel_detail(self, response):
        name = response.meta["name"]
        url = response.meta["url"]
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
            "name": name,
            "url": url,
            "rating": rating,
            "address": address,
            "description": description,
            "latitude": latitude,
            "longitude": longitude
        }

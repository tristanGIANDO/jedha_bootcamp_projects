import scrapy


class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = [
        'https://www.booking.com/searchresults.html?ss=Montpellier'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response):

        hotels = response.css('div[data-testid="property-card"]')
        print(f'Found {len(hotels)} hotels')

        for hotel in hotels:
            name = hotel.css('div[data-testid="title"]::text').get().strip()
            rating = hotel.css('div.f13857cc8c.e008572b71::text').get()

            yield {
                'name': name,
                'rating': rating
            }

        next_page = response.css('a.bui-pagination__link.pagenext::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

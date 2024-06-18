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
        self.log(f'Parsing page: {response.url}')
        
        hotels = response.css('div[data-testid="property-card"] div[data-testid="title"]')
        self.log(f'Found {len(hotels)} hotels')
        
        for hotel in hotels[:20]:
            name = hotel.css('::text').get().strip()
            self.log(f'Hotel name: {name}')
            yield {
                'name': name
            }

        # Pagination (si nécessaire)
        next_page = response.css('a.bui-pagination__link.pagenext::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


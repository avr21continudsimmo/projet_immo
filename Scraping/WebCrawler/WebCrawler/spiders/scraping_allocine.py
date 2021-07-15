from time import sleep
import scrapy
import requests

class ReviewsAllocineItem(scrapy.Item):
     
    title = scrapy.Field() # Le titre du film
    review = scrapy.Field() # Le commentaire
    stars = scrapy.Field() # La note donnée au film par l'auteur du commentaire
    
from scrapy import Request, Spider
 
class SpiderReviewsAllocine(Spider):
    # Nom du spider
    name = "scraping_allocine"
    # URL de la page à scraper
    url = "https://www.allocine.fr/film/fichefilm-10568/critiques/spectateurs/"
 
    def start_requests(self):
        yield Request(url=url, callback=self.parse_films)
 
    def parse_films(self, response):
        title = response.css("a.titlebar-link::text").extract_first()
        review_blocks = response.css("div.review-card")
        for review_card in review_blocks:
            review = review_card.css("div.content-txt::text").extract_first()
            stars = review_card.css("span.stareval-note::text").extract_first()
             
            # Pour avoir la note (nombre d'étoiles) en float
            stars = float(stars.replace(",", "."))
 
            item = ReviewsAllocineItem()
 
            item['title'] = title
            item['stars'] = stars
            item['review'] = review
 
            yield item
            

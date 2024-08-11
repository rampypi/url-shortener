import random
import threading
import uuid
import validators


class UrlShortner:
    URL_DOMAIN = "https://short.url/"
    urls_collection = {}
    
    def __init__(self):
        self.lock = threading.Lock()
    
    def shorten_url(self, url):
        if not url or not validators.url(url):
            return "Please provide a valid URL"
        short_url = self.URL_DOMAIN+ self.generate_unique_number()
        self.urls_collection[short_url] =url
        return short_url
    
    def generate_unique_number(self):
        while True:
            unique_str = uuid.uuid4().hex[:6]  # Generate a unique 6-character string
            short_url = self.URL_DOMAIN + unique_str        
            with self.lock:
                if short_url not in self.urls_collection:
                        return unique_str
        

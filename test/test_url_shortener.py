"""
Implement a service that can shorten a given URL.
The shortened URL should be unique for each original URL.
The service should be able to handle the mapping between shortened URLs and their original counterparts.
"""

import threading
import unittest
from app.shortener import UrlShortner
import validators

class TestUrlShortner(unittest.TestCase):
    SHORT_URL_DOMAIN = "short.url"
    
    def setUp(self):
        self.instance_url_shortener = UrlShortner()
        
    def test_signle_url_shortener(self):
        short_url = self.instance_url_shortener.shorten_url(url="http://google.com/")
        self.assertTrue(validators.url(short_url), "Shortened URL is not valid")
        
    def test_signle_shorten_url(self):
        short_url = self.instance_url_shortener.shorten_url(url="https://www.example.com/very-long-url-with-lots-of-characters")
        #Example valid shorturl --> https://short.url/abc123
        self.assertTrue(self.SHORT_URL_DOMAIN in short_url, "Domain is not valid")
        
    def test_signle_shorten_url_storage(self):
        short_url =self.instance_url_shortener.shorten_url(url="https://www.example.com/very-long-url-with-lots-of-characters")
        self.assertTrue(short_url in self.instance_url_shortener.urls_collection,"Shortened URL not stored properly")
        
    def test_reetrieve_original_url_from_shorturl(self):
        original_url1 = "https://www.example.com/very-long-url-with-lots-of-characters"
        original_url2 = "https://www.example.com/very-long-url-with"
        short_url1 = self.instance_url_shortener.shorten_url(url=original_url1)
        short_url2 = self.instance_url_shortener.shorten_url(url=original_url2)
        self.assertTrue(original_url1 == self.instance_url_shortener.urls_collection[short_url1],"Not able to retrieve original URL")
        self.assertTrue(original_url2 == self.instance_url_shortener.urls_collection[short_url2],"Not able to retrieve original URL")
        
    def test_empty_url(self):
        empty_result = self.instance_url_shortener.shorten_url(url=None)
        empty_result2 = self.instance_url_shortener.shorten_url(url="")
        empty_result3 = self.instance_url_shortener.shorten_url(url="jdhfd87543jkdf")
        
        self.assertTrue(empty_result == empty_result2==empty_result3== "Please provide a valid URL","Validating URL failed")

    def test_threading_test_for_url_shortener(self):
        
        
        urls = [f"https://www.example.com/very{i}" for i in range(100)]
        
        existing = len(self.instance_url_shortener.urls_collection)
        
        threads = []
        for url in urls:
            threads.append(threading.Thread(target=self.instance_url_shortener.shorten_url, args=(url,)))
       
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        total = len(self.instance_url_shortener.urls_collection)-existing
        self.assertTrue(total==100, "Not all URLs were added correctly not thread safe")

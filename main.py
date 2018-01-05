import lxml.html
import requests
import scraper as sc


class Scraping:

    def __init__(self):
        self.get_url = lambda number: 'http://desiopt.com/search-results-jobs/?searchId=1515187211.36&action=search&page='+str(number)+'&listings_per_page=100&view=list'
        self.data = []

    def get_data(self):
        for number in range(1, 247):
            print(number)
            self.url = self.get_url(number)
            self.source = requests.get(self.url)
            self.etree = lxml.html.fromstring(self.source.content)
            self.tree = self.etree.xpath('//div[@id="listingsResults"]//tr[not(@id)]')
            for element in self.tree:
                self.job = sc.get_href(element.xpath('.//div[@class="listing-title"]/a[@href]'))
                self.location = sc.get_text(element.xpath('.//div[@class="left-side"]/span[1]/following-sibling::span[1]/text()'))
                self.posted = sc.get_text(element.xpath('.//div[@class="left-side"]/span[2]/following-sibling::span[2]/text()'))
                self.link = sc.get_href(element.xpath('.//div[@class="left-side"]/span[3]/following-sibling::span[3]/a[@href]'))
                self.company = sc.get_text(element.xpath('.//div[@class="left-side"]/span[3]/following-sibling::span[3]//text()'))
                self.data.append([self.job, self.location, self.posted, self.link, self.company])
        sc.Database(('job', 'location', 'posted', 'link', 'company')).push_data(self.data)


Scraping = Scraping()
Scraping.get_data()

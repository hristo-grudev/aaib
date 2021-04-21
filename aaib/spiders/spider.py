import scrapy

from scrapy.loader import ItemLoader

from ..items import AaibItem
from itemloaders.processors import TakeFirst


class AaibSpider(scrapy.Spider):
	name = 'aaib'
	start_urls = ['https://aaib.com/mediaRoom/press/type/press?lang=en']

	def parse(self, response):
		post_links = response.xpath('//div[@class="item"]')
		for post in post_links:
			title = post.xpath('.//div[@class="new_title"]/text()').get()
			description = post.xpath('.//div[@class="new_brief"]//text()[normalize-space()]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()
			date = post.xpath('.//div[@class="news_date"]/text()').get()

			item = ItemLoader(item=AaibItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()

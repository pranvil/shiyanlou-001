import scrapy

class Github_spider(scrapy.Spider):
    name = 'robot'
    @property
    def start_urls(self):
        url = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url.format(i) for i in range(1,4))

    def parse(self,response):
        for t in response.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]'):
            yield {
                    'name':t.xpath('.//div[@class="d-inline-block mb-1"]/h3/a/text()').re('\n        (.+)'),
                    'update_time':t.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract()
                }



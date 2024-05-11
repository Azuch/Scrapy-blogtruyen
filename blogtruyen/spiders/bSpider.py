import scrapy
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor


class BspiderSpider(scrapy.Spider):
    name = "bSpider"
    baseUrl = "https://nettruyencc.com"
    
    def start_requests(self):
        with open("links", "r") as f:
            for url in f:
                yield scrapy.Request(url.strip(), callback=self.parse)

    def parse(self, response):
        chapters_links = response.xpath('//div[contains(@class, "chapter")]//a[starts-with(@href, "https")]/@href').extract()
        manga_name = response.url.split("/")[-1]
        for index, chapter_link in enumerate(chapters_links):
            yield scrapy.Request(chapter_link, callback=self.parse_chapter, meta={"manga_name": manga_name, "chapter_name": f"chapter-{index}"})

    def parse_chapter(self, response):
        chapter_name = response.meta["chapter_name"]
        manga_name = response.meta["manga_name"]
        # Extract image URLs
        img_tags = response.xpath('//*[@class="page-chapter"]//img')

        for idx, img_tag in enumerate(img_tags):
            img_urls = img_tag.xpath('./@*[contains(., "https")]').extract()
            for idx_url, img_url in enumerate(img_urls):
                img_name = f'image-{idx}-{idx_url}.jpg'
                img_path = f'manga/{manga_name}/{chapter_name}/{img_name}'
                yield {"chapter_name": chapter_name, "manga_name": manga_name, "img_url": img_url}
                yield scrapy.Request(url=img_url, meta={'img_path': img_path, 'referer': response.url}, callback=self.save_img)

    def save_img(self, response):
        img_path = response.meta['img_path']
        with open(img_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved image {img_path}')



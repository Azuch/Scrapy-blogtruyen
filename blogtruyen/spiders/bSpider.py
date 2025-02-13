import scrapy
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
import os

class BspiderSpider(scrapy.Spider):
    name = "bSpider"
    base = "https://truyenqqto.com" 
    def start_requests(self):
        with open("links", "r") as f:
            for url in f:
                print(url)
                yield scrapy.Request(url.strip(), callback=self.parse)

    def parse(self, response):
        base = "https://truyenqqto.com"
        chapters_links = response.xpath("//div[@class='works-chapter-list']//a/@href").extract()
        manga_name = response.url.split("/")[-1]
        chapters_links.reverse()
        for index, chapter_link in enumerate(chapters_links):
            chapter_link = f"https://truyenqqto.com{chapter_link}"
            print(chapter_link, manga_name)
            yield scrapy.Request(url=chapter_link, callback=self.parse_chapter, meta={"manga_name": manga_name, "chapter_name": f"chapter-{index}"})
            

    def parse_chapter(self, response):
        chapter_name = response.meta["chapter_name"]
        manga_name = response.meta["manga_name"]

        # Extract image URLs
        imgs = response.xpath("//div[@class='page-chapter']//img/@src").extract()
        for idx, img_url in enumerate(imgs):
            img_name = f'image-{idx}.jpg'
            img_dir = f"manga/{manga_name}/{chapter_name}"
            try:
                os.makedirs(img_dir, exist_ok=True)
            except Exception as e:
                print(f"An error occurred: {e}")
            img_path = f'manga/{manga_name}/{chapter_name}/{img_name}'
            #print(img_url, img_path)
            yield scrapy.Request(url=img_url, meta={'img_path': img_path, 'referer': response.url}, callback=self.save_img)

    def save_img(self, response):
        img_path = response.meta['img_path']
        with open(img_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved image {img_path}')

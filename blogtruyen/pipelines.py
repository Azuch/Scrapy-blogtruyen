# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import scrapy

class ImagePipeline:
    def process_item(self, item, spider):
        # Create directory if not exists
        page_dir = f'manga/{item["manga_name"]}/{item["chapter_name"]}'
        os.makedirs(page_dir, exist_ok=True)



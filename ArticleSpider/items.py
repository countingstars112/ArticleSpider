# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
#数据保存的格式
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobble(value):
    return value+"-bobby"


def date_convert(value):
    value = value.strip().replace("·", "").strip()
    try:
        re_time = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        re_time = datetime.datetime.now().date()
    return re_time

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums



#定义所有的list都只取第一个
class AticleItmeLoad(ItemLoader):
    #自定ItmeLoader
    default_output_processor = TakeFirst()

#保持返回的值还是list
def return_value(value):
    return value

class JobboleArticleItem(scrapy.Item):
    re_title = scrapy.Field(
        input_processor=MapCompose(add_jobble)
        # input_processor =MapCompose(lambda x: x+"--jobble", add_jobble)
    )
    re_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    tag = scrapy.Field(
        input_processor=MapCompose(lambda x: x.replace('评论', "")),
        output_processor=Join(",")
    )
    url = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_url_db = scrapy.Field()
    front_image_path = scrapy.Field()
    url_object_id = scrapy.Field()




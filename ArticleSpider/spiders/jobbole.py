# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem, AticleItmeLoad
from ArticleSpider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并嫁给scrapy下载后并进行解析
        1获取下一页的url并交给scrapy来下载，下载完成后交给parser来进行解析
        :param response:
        :return:
        """
        #解析列表中的url
        post_nodes= response.css("#archive .floated-thumb .post-thumb a")
        next_url = response.css(".next.page-numbers::attr('href')").extract_first()
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail, meta={"front_image_url":parse.urljoin(response.url, image_url)})
            # print(post_url)

        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):

        front_image_url = response.meta.get("front_image_url")  # 文章封面图，request传进来的
        #提取文章的具体字段
        # re_title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first(default='not-found')
        # re_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()
        # praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # if praise_num == "":
        #     praise_num = 0
        # fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].replace("收藏", "").strip()
        # if fav_num == "":
        #     fav_num = 0
        # comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].replace("评论", "").strip()
        # if comment_num == "":
        #     comment_num = 0
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        # tag = ",".join(tag_list)
        #
        #
        # #通过css选择器
        # # title = response.css(".entry-header h1::text").extract()
        # # time = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "")
        # # praise_num = response.css(".vote-post-up h10::text").extract()[0]
        # # fav_num = response.css(".bookmark-btn::text").extract()[0].strip().replace("收藏", "").strip()
        # # comment_num = response.css("a[href='#article-comment'] span::text").extract()[0].strip().replace("评论", "").strip()
        #
        #
        # #在items中填充值
        # article_item = JobboleArticleItem()
        #
        # article_item["re_title"] = re_title
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["front_image_url"] = [front_image_url]
        # article_item["front_image_url_db"] = front_image_url
        # try:
        #     re_time = datetime.datetime.strptime(re_time, '%Y/%m/%d').date()
        # except Exception as e:
        #     re_time = datetime.datetime.now().date()
        # article_item["re_time"] = re_time
        # article_item["praise_num"] = praise_num
        # article_item["fav_num"] = fav_num
        # article_item["comment_num"] = comment_num
        # article_item["content"] = content
        # article_item["tag"] = tag
        # article_item["url"] = response.url

        # 通过Itemloader加载item
        item_loader = AticleItmeLoad(item=JobboleArticleItem(), response=response)
        # 直接加值
        item_loader.add_value("url", response.url)
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("front_image_url_db", front_image_url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        #提取后填充
        item_loader.add_xpath("re_title", "//div[@class='entry-header']/h1/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")
        item_loader.add_xpath("praise_num", "//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_num", "//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath("praise_num", "//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath("comment_num", "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("tag", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_css("re_time", "p.entry-meta-hide-on-mobile::text")
        article_item = item_loader.load_item()
        yield article_item


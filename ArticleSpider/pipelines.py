# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#数据存储
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


#数据已经在Item内了
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 图片的下载路径的获取与插入11
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file_path = ''
            for ok, value in results:
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path
        return item

#保存json,自定义
class JosnWithEncodePipline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    #关闭文件
    def spider_closed(self, spider):
        self.file.close()


#JsonItemExporter,调用方法保存为json
class JsonItemExporterPipeline(object):
    #调用srapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

#同步的MysqlPipeline
class MysqlPipleline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '12345', 'article_spider', port=3306, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, sprider):
        insert_sql = """
        insert into jobble (re_title, re_time, tag, url, praise_num,fav_num,comment_num,front_image_url,front_image_path,url_object_id ,content)
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        self.cursor.execute(insert_sql, [item["re_title"], item["re_time"], item["tag"], item["url"], item["praise_num"],
                            item["fav_num"], item["comment_num"], item["front_image_url_db"], item['front_image_path'],
                                         item["url_object_id"], item["content"]])
        self.conn.commit()
        return item


#异步的Mysql数据库插入：
class MsqltwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
        host =settings['MYSQL_HOST'],
        db=settings["MYSQL_DBNAME"],
        user=settings["MYSQL_USER"],
        password=settings["MYSQL_PASSWORD"],
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor,
        use_unicode=True,

        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行,可能会出错
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        print(failure)


    def do_insert(self, cursor, item):
        #写入mysql
        insert_sql = """
                insert into jobble (re_title, re_time, tag, url, praise_num,fav_num,comment_num,front_image_url,front_image_path,url_object_id ,content)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                """
        cursor.execute(insert_sql,
                            [item["re_title"], item["re_time"], item["tag"], item["url"], item["praise_num"],
                             item["fav_num"], item["comment_num"], item["front_image_url_db"], item['front_image_path'],
                             item["url_object_id"], item["content"]])
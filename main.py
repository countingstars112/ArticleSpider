
from scrapy.cmdline import execute

import sys
import  os
#设置项目工程主目录
#sys.path.append("F:\Envs\article_spider\Scripts\ArticleSpider")
#但是放到其他的地方，代码就不能运行了所以用 io

print (os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "zhihu"])
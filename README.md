嗯，第一次写爬虫，写得挺烂的，尤其是在对xml格式优化上还欠缺很多，导致rss源只有FeedDemon能认。。以后慢慢处理吧。。

为什么要写这个东西：
第一，优化教务处通知阅读体验，上网上看那些通知总是不怎么舒服，看得眼睛都花


第二，实时了解教务处通知动态，这个是重点。虽然目前代码还没有完善但还能勉强用


用scrapy写的爬虫，下面说一下使用方法


Windows：先按http://www.cnblogs.com/tigerm/p/scrapy.html  安装scrapy，先填一下/rss/spider/rsspider.py中的学号和密码，之后双击rumme.bat


到最后在BUPT-rss下生成一个rss.xml，最好在根据https://jingyan.baidu.com/album/e2284b2b72bffce2e6118d2c.html  将rumme.bat设置到计划任务中，设置每天执行一次。


之后在 http://www.appinn.com/easywebserver/ 下载安装easywebserver，将网站根目录定到BUPT-rss下，之后就能用FeedDemon导入地址为127.0.0.1/rss.xml的feed了。


linux：能用linux的同学看了上面windows教程应该知道怎么做了我就不多说了哈哈
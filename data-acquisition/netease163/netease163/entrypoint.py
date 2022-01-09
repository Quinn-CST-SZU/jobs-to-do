from datetime import datetime
import logging 
logging.basicConfig(level=logging.WARN,
                    filename='./log/netease163_%s.log' % datetime.today().strftime('%Y%m%d%H%I%S'),
                    format='%(asctime)s - %(filename)s[line:%(lineno)d, func:%(funcName)s] - %(levelname)s: %(message)s')


from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'WYY'])
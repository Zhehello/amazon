# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class AmazonSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from scrapy.http import Response
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

class AmazonLoginDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.b = webdriver.Chrome()

    def process_request(self,spider, request):
        if request.meta.get('selenium'):
            self.b.get(request.url)
            time.sleep(3)
            username = self.b.find_element_by_name("email")
            username.clear()
            username.send_keys('*****')  # ??????????
            password = self.b.find_element_by_name('password')
            password.clear()
            password.send_keys('*****')  # ?????????
            '''
            try:
                captcha = self.b.find_element_by_id('captcha_field')
                captcha.clear()
                capcha_str = input('???????')
                captcha.send_keys(capcha_str)
            except NoSuchElementException:
                print("????????????")
            '''
            input_button = self.b.find_element_by_id("signInSubmit")
            input_button.click()  # ????

            set_cookies = []
            for c in self.b.get_cookies():
                # cookie???????name,value?Domain
                set_cookies.append('{}={}; Domain=.amazon.cn; path=/'.format(c['name'],c['value']))
            print(set_cookies)
            headers = {"Set-Cookie":set_cookies}
            return Response(url=self.b.current_url,body=self.b.page_source.encode('utf8'),request=request,headers=headers)
        else:
            pass

    def process_response(self,spider, request, response):

        return response

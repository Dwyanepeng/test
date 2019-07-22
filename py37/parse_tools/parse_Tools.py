from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from scrapy.selector import Selector
import re
import time


def get_text(source_content):
    """传入部分网页源码
        返回字符串形式的网页源码以及其中的文本内容。
        #获取文章文本内容
    """
    t = str()
    try:
        for s in source_content:
            t = t + str(s)
        soup = BeautifulSoup(t, "lxml")
        source = t
        content = soup.get_text(strip=True)
    except:
        source = "无"
        content = "无"
    return source, content


def get_urls(css,response):
    # 根据网页和css标签，获取网页中链接地址
    le = LinkExtractor(restrict_css=str(css))
    links = le.extract_links(response)
    return links

def get_next_pages(page_count, root_url, middle_url, last_url_tag, begin):
    """
    用于获取那些以index_数字分页的页面，获取每页的地址。
    入参：总页数，基础地址，拼接地址根，网页后缀，以及从第几页开始拼接。
    出参：拼接收的网页链接列表。
    第一页爬虫处理，剩余页链接函数处理
    """
    next_page_urls = []
    for i in range(int(page_count)):
        next_page_url = root_url + str(middle_url) + str(i + begin) + str(last_url_tag)
        next_page_urls.append(next_page_url)
    return next_page_urls

#用于从js脚本中获取总页数
def get_page_count(css,response):
    page_count_str = response.css(css).extract_first()
    try:
        if page_count_str.rfind('createPageHTML') != -1:
            tmp_s = page_count_str[page_count_str.rfind('createPageHTML') + len('createPageHTML'):page_count_str.rfind(
                'createPageHTML') + len('createPageHTML') + 10]  # 从该字符串开始10字符串内找总页数值
        else:
            if page_count_str.find('countPage') != -1:
                tmp_s = page_count_str[page_count_str.find('countPage')+len('countPage'):page_count_str.find('countPage')+len('countPage')+10] #从该字符串开始10字符串内找总页数值
        page_count=int(re.findall("\d+",tmp_s)[0])#第一个数值为总页数
    except Exception as e:
        page_count = 0
    return page_count

# 用于获取动态网页的生成的网页内容，返回为scrapy selector对象。
def get_js_webpage(url,delay=0):
    # 启动driver
    def init_web_driver():
        global driver
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.add_argument('-headless')
        fireFoxOptions.add_argument('--log_level=fatal')
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)  # 某些firefox只需要这个
        firefox_profile.set_preference('browser.migration.version', 9001)  # 部分需要加上这个
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference('javascript.enabled', 'false')

        driver = webdriver.Firefox(firefox_options=fireFoxOptions, firefox_profile=firefox_profile)

    # 关掉driver
    def close_web_driver():
        driver.close()


    # 获取数据
    init_web_driver()
    driver.get(url)
    time.sleep(delay)
    driver.implicitly_wait(10)
    web_page_source = Selector(text=driver.page_source)
    close_web_driver()
    return web_page_source

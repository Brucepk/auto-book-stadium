from selenium import webdriver
from time import sleep
import random
import send_email

'''
作者：pk哥
公众号：Python知识圈
日期：2019/8/12
代码解析详见公众号「Python知识圈」

如有疑问或需转载文章，请联系微信号：dyw520520，备注来意，谢谢。
我的个人博客：https://www.pyzhishiquan.com/
'''


class BookStadium():

    def __init__(self):
        profile_directory = r'--user-data-dir=C:\Users\thinkpad\AppData\Local\Google\Chrome\User Data'
        option = webdriver.ChromeOptions()
        option.add_argument(profile_directory)
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.implicitly_wait(10)

    def search(self, city_id, search_text):
        self.driver.get('http://quyundong.com/search/searchResult?city_id={}&search_text={}'
                        .format(city_id, search_text))
        self.driver.maximize_window()

    def book_time(self, book_time):
        self.driver.find_element_by_partial_link_text(book_time).click()      # 根据部分文字点击预定时间 比如：周五
        sleep(3)
        scroll = "document.getElementById('detail').scrollIntoView(false)"  # 滚动屏幕，使元素出现在屏幕底部
        self.driver.execute_script(scroll)

    def book_stadium(self, book_time):
        self.driver.find_element_by_xpath('//*[@class="business-order"]/div').click()   # 点击立即预定按钮，打开新页面
        sleep(3)
        n = self.driver.window_handles         # 获取当前页句柄
        self.driver.switch_to.window(n[1])     # 切换到新的网页窗口
        self.book_time(book_time)
        sleep(3)
        # 定位你要定的时间段
        while True:
            for i in range(4, 10):    # 我只需要预定第4列和第9列的场地，也就是4号到9号场地
                site = self.driver.find_element_by_xpath('//*[@id="booking"]/div[3]/div[1]/'
                                                         'table/tbody/tr[9]/td[{}]'.format(i))
                sta = site.get_attribute('status')
                if int(sta) != 0:
                    print('%s号场地已被预定' % i)
                else:
                    site.click()      # 场地可预订的话点击场地
                    sleep(3)
                    self.driver.find_element_by_xpath('//*[@id="booking"]/div[3]/div[2]/div[2]/a').click()  # 点击提交订单按钮
                    # 加上登录态失效时的判断，提交订单后，如果弹出登录页面，也会发送邮件给自己提醒场地有空出来
                    head = self.driver.find_element_by_class_name('headText')
                    if head:
                        print('登录态已失效，%s号场地还有，请登录预定！！' % i)
                        send_email.sendMail()
                        return
                    sleep(2)
                    scroll_bottom = "window.scrollTo(0,document.body.scrollHeight)"     # 获取body的高度，滑到底部
                    self.driver.execute_script(scroll_bottom)
                    self.driver.find_element_by_xpath('//*[@class="order"]/a').click()
                    sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="pay_form"]/div[1]/div[5]/div').click()
                    sleep(3)
                    print('%s号场地预定成功，请马上支付！！' % i)
                    send_email.sendMail()
                    return
            sleep(int(format(random.randint(600, 1200))))   # 随机等待10-20分钟
            self.driver.refresh()


if __name__ == '__main__':
    bs = BookStadium()
    city_id = 321
    search_text = '上海霜天羽毛球馆'
    book_time = '周五'
    bs.search(city_id, search_text)
    sleep(3)
    bs.book_stadium(book_time)




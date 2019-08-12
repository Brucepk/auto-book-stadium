import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


'''
作者：pk哥
公众号：Python知识圈
日期：2019/8/12
代码解析详见公众号「Python知识圈」

如有疑问或需转载文章，请联系微信号：dyw520520，备注来意，谢谢。
我的个人博客：https://www.pyzhishiquan.com/
'''

my_sender = 'xxx@qq.com'  # 发件人邮箱账号
my_user = 'xxx@qq.com'  # 收件人邮箱账号


def sendMail():
    try:
        '''发送邮件'''
        msg = MIMEText('10分钟内支付，否则订单失效！！！', "plain", 'utf-8')  # 发送邮件内容
        msg["Subject"] = Header('羽毛球场地已预定，尽快支付！！！', 'utf-8')  # 发送邮件主题/标题
        msg["From"] = formataddr(['Bruce Lee', my_sender])  # 邮件发送方
        msg["To"] = formataddr(['brucepk', my_user])  # 邮件接收方

        s = smtplib.SMTP("smtp.qq.com", 25)  # 邮箱的传输协议，端口默认25
        s.login(my_sender, 'xxxx')  # 登录邮箱，这里的第二个参数为qq邮箱授权码，不要填你的登录密码
        s.sendmail(my_sender, [my_user, ], msg.as_string())  # 发送方，接收方，发送消息
        s.quit()  # 退出邮箱
        print("邮件发送成功！")
    except Exception:
        print("邮件发送失败~~")


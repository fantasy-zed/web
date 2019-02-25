# -*- coding:utf-8 -*-
"""
author: fantasy
time: 2019/02/21
desc:
"""
import json
import hashlib
import web
import receive
import time
import os
import Utils
import logging
import io, traceback, sys
import smtplib
from email.mime.text import MIMEText

# 初始化日志器
log = logging.getLogger()
log.setLevel(logging.DEBUG)
# 创建handler
fh = logging.FileHandler("main.log", "a", encoding="utf-8")
# 创建日志格式
fmt = logging.Formatter(fmt="%(asctime)s [%(lineno)d] %(levelname)s [func:%(funcName)s] %(message)s",datefmt='%Y-%m-%d %H:%M:%S %a')
# 为handler指定输出格式
fh.setFormatter(fmt)
# 为logger指定处理器
log.addHandler(fh)

# url和对应的处理类
urls = (
    '/wx', 'Handle_WX_MSG',
    '/', 'index',
)


def printErr(className):
    log.error(className + ',' + 'exception:' + str(sys.exc_info()[0]) + ',' + str(sys.exc_info()[1]))
    fp = io.StringIO()
    traceback.print_exc(file=fp)
    log.error(className + ',' + fp.getvalue())


class index:

    def GET(self):
        try:
            data = web.input()
            log.info("web.input()>>%s" % data)
            client_ip = Utils.GetClientIP()
            log.info("client ip" + str(client_ip))
            # import smtplib
            # from email.mime.text import MIMEText
            # msg_from = ''  # 发送方邮箱
            # passwd = ''  # 填入发送方邮箱的授权码
            # msg_to = ''  # 收件人邮箱
            # subject = "范特西python邮件测试"  # 主题
            # content = "这是我使用python smtplib及email模块发送的邮件测试"
            # msg = MIMEText(content, "plain", "utf8")
            # msg['Subject'] = subject
            # msg['From'] = msg_from
            # msg['To'] = msg_to
            # s = None
            # try:
            #     s = smtplib.SMTP_SSL("smtp.163.com", 465)
            #     s.login(msg_from, passwd)
            #     s.sendmail(msg_from, msg_to, msg.as_string())
            #     log.info("发送成功")
            # except Exception:
            #     import io, traceback
            #     fp = io.StringIO()
            #     traceback.print_exc(file=fp)
            #     log.info(fp.getvalue())
            # finally:
            #     s.quit()
            info = json.dumps({"code": 0, "msg": "welcome to fantasy."}, ensure_ascii=False)
            return info
        except Exception as e:
            printErr(self.__class__.__name__)


# 处理发给公众号的消息
class Handle_WX_MSG(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            print("handle GET")
            data = web.input()
            log.info("web.input()>>%s" % data)
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "fantasyisnotfantasy"
            list = [token, timestamp, nonce]
            list.sort()
            s = list[0] + list[1] + list[2]
            hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
            log.info("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except (Exception) as Argument:
            printErr(self.__class__.__name__)

    def POST(self):
        try:
            webData = web.data()
            log.info("web.input()>>%s" % webData)
            # 打印消息体日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                log.info("msg>>" + recMsg.Content)
                msg_from = 'fantasyandzed@163.com'  # 发送方邮箱
                passwd = 'saka102400'  # 填入发送方邮箱的授权码
                msg_to = 'fantasy.w@qq.com'  # 收件人邮箱
                subject = "公众号消息"  # 主题
                content = recMsg.Content
                msg = MIMEText(content, "plain", "utf8")
                msg['Subject'] = subject
                msg['From'] = msg_from
                msg['To'] = msg_to
                s = None
                s = smtplib.SMTP_SSL("smtp.163.com", 465)
                s.login(msg_from, passwd)
                s.sendmail(msg_from, msg_to, msg.as_string())

                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "欢迎关注bao笑段子"
                log.info('Reply message info:')
                log.info('toUser = %s' % toUser)
                log.info('fromUser = %s ' % fromUser)
                log.info('content = %s' % content)
                return self.render.reply_text(toUser, fromUser, int(time.time()), content)
            elif recMsg.MsgType == "even":
                log.info("关注")
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                return self.render.reply_text(toUser, fromUser, int(time.time()), "客官您终于来了，关注bao笑段子，天天笑不停")
            else:
                log.info("不支持的消息类型：%s" % recMsg.MsgType)
        except (Exception) as e:
            printErr(self.__class__.__name__)
        finally:
            s.quit()


# 404
def notfound():
    return web.notfound('the page you are looking for is not exist!')


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

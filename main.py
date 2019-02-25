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
import utils

#
logf = utils.CreateLogger("helloworld.log")

# url和对应的处理类
urls = (
    '/wx', 'Handle_WX_MSG',
    '/', 'index',
)


class index:

    def GET(self):
        client_ip = utils.GetClientIP()
        logf.info("client ip" + str(client_ip))
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
        #     logf.info("发送成功")
        # except Exception:
        #     import io, traceback
        #     fp = io.StringIO()
        #     traceback.print_exc(file=fp)
        #     logf.info(fp.getvalue())
        # finally:
        #     s.quit()
        info = json.dumps({"code": 0, "msg": "welcome to fantasy."}, ensure_ascii=False)
        return info


# 处理发给公众号的消息
class Handle_WX_MSG(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            data = web.input()
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
            logf.info("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return echostr
        except (Exception) as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            logf.info("Handle Post webdata is:\n", webData)
            # 打印消息体日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "欢迎关注bao笑段子"
                logf.info('Reply message info:\n')
                logf.info('toUser =', toUser)
                logf.info('fromUser = ', fromUser)
                logf.info('content = ', content)
                return self.render.reply_text(toUser, fromUser, int(time.time()), content)
            else:
                logf.info("不支持的消息类型：", recMsg.MsgType)
        except (Exception) as e:
            utils.print_error(self.__class__.__name__, logf)


# 404
def notfound():
    return web.notfound('the page you are looking for is not exist!')


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

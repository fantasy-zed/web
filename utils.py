# -*- coding:utf-8 _*-
"""
author:fantasy
time: 2018/12/07
desc:
"""
import web
import re
import logging
import smtplib
from email.mime.text import MIMEText



def CreateLogger(logName):
    # 初始化日志器
    log = logging.getLogger('log')
    log.setLevel(logging.DEBUG)
    # 创建handler
    fh = logging.FileHandler(logName, "a", encoding="utf-8")
    # 创建日志格式
    fmt = logging.Formatter(fmt="%(asctime)s [%(lineno)d] %(levelname)s [func:%(funcName)s] %(message)s", datefmt='%Y-%m-%d %H:%M:%S %a')
    # 为handler指定输出格式
    fh.setFormatter(fmt)
    # 为logger指定处理器
    log.addHandler(fh)
    return log


def SendMail(msg_to, msg_from, subject, content, passwd):
    """发送邮件到个人邮箱"""
    msg = MIMEText(content, "plain", "utf8")
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    s = None
    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except Exception:
        import io, traceback
        fp = io.StringIO()
        traceback.print_exc(file=fp)
        print(fp.getvalue())
    finally:
        s.quit()


def GetClientIP():
    remote_addr = str(web.ctx.ip)
    x_forwarded_for = str(web.ctx.env.get('HTTP_X_FORWARDED_FOR', None))
    if not x_forwarded_for:
        return remote_addr
    client_ip = x_forwarded_for.split(', ')[0]
    if CheckIP(client_ip):
        return client_ip
    return remote_addr


def CheckIP(strIP):
    return bool(
        re.match(r"^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$", strIP, re.VERBOSE))

# -*- coding:utf-8 _*-
"""
author:fantasy
time: 2018/12/07
desc:
"""

def CreateLogger(logName):
    import logging
    # 初始化日志器
    log = logging.getLogger('log')
    log.setLevel(logging.DEBUG)
    # 创建handler
    fh = logging.FileHandler(logName, "a", encoding="utf-8")
    # 创建日志格式
    fmt = logging.Formatter(fmt="%(asctime)s %(levelname)s [func:%(funcName)s] %(message)s",
                            datefmt='%Y-%m-%d %H:%M:%S %a')
    # 为handler指定输出格式
    fh.setFormatter(fmt)
    # 为logger指定处理器
    log.addHandler(fh)
    return log


def SendMail(msg_to, msg_from, subject, content, passwd):
    """发送邮件到个人邮箱"""
    import smtplib
    from email.mime.text import MIMEText
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

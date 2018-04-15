# coding: utf8
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_login = os.getenv('SMTP_LOGIN')
smtp_pwd = os.getenv('SMTP_PWD')
recipients = os.getenv('EMAIL_TO')

def deliver_now(items):
    Notifier(items).deliver_now()

class Notifier(object):
    def __init__(self, items):
        self.items = items

    def build_html(self):
        return f"""\
        <html>
        <head></head>
        <body>
          <p>Hi!<br>
            I have some new offers for you! 😇
          </p>
          <table>
            {self.render()}
          </table>
        </body>
        </html>
        """

    def render(self):
        ret = ""
        for item in self.items:
            ret += self.render_item(item)
        return ret

    def render_item(self, item):
        return f"""
        <tr>
            <td>
                <img src="{item['img_url']}" />
            </td>
            <td><a href="{item['url']}">{item['title']}</a></td>
            <td>{item['price']}</td>
        </tr>
        """

    def deliver_now(self):
        if not (smtp_login and smtp_pwd):
            print("Notifier: pass, SMTP not configured. Set SMTP_LOGIN and SMTP_PWD")
            return
        if len(self.items) is 0:
            print("Notifier: no new search results - skipping")
            return
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "New search results"
        msg['From'] = 'OtoDom Bot'
        msg['To'] = recipients
        msg.attach(MIMEText(self.build_html(), 'html'))
        server_ssl = smtplib.SMTP_SSL('smtp.mailgun.com', 465)
        server_ssl.ehlo()
        server_ssl.login(smtp_user, smtp_pwd)
        server_ssl.sendmail(smtp_user, recipients.split(','), msg.as_string())
        server_ssl.quit()
        print(f"Notifier: sent mail to {recipients}")

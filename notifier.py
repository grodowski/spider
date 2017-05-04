# coding: utf8
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user = os.getenv('GMAIL_USER')
gmail_pwd = os.getenv('GMAIL_PWD')
me = os.getenv('EMAIL_FROM', 'my@email.com')
you = os.getenv('EMAIL_TO', 'your@email.com')

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
        if len(self.items) is 0:
            print("No new items - skipping")
            return
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🕷 OtoDom"
        msg['From'] = me
        msg['To'] = you
        msg.attach(MIMEText(self.build_html(), 'html'))
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(gmail_user, gmail_pwd)
        server_ssl.sendmail(me, you, msg.as_string())
        server_ssl.quit()

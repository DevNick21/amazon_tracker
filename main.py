from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("telegram_api_key")
CHAT_ID = os.getenv("my_telegram_chat_id")
my_email = os.getenv("MY_EMAIL")
other_email = "iheanacho.ekene@hotmail.com"
password = os.getenv("EMAIL_PASSWORD")


amazon_url = "https://www.amazon.com/Bluetooth-Belt-Driven-Turntable-Speakers-Headphone/dp/B07N3WYLKZ/ref=sr_1_1_sspa?crid=4JPX636TJ4QJ&keywords=vinyl+player&qid=1692367737&sprefix=vinyl+p%2Caps%2C1197&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&smid=A1P1OHB2JFMIPI"

amz_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Accept-Language': 'en-US, en;q=0.5'
}
res = requests.get(url=amazon_url, headers=amz_headers)
webpage = res.text

soup = BeautifulSoup(webpage, "html.parser")
price_tag = soup.select_one(".a-offscreen")
price = float(price_tag.get_text().strip("$"))


def send_mail(message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Price Alert'
    msg['From'] = my_email
    msg['To'] = other_email

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(my_email, password=password)
        server.send_message(msg)


if price < 30:
    send_mail(
        message=f"Your Vinyl Player Item is now {price}, below your set target")

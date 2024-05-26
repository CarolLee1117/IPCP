'''
    測試如何使用 Python 來發送 Email，
    這裡使用的是 Gmail 的 SMTP 伺服器。
'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    def __init__(self, src, sap):
        self.src = src
        self.sap = sap
    
    def send_email(self, subject, dst, context):
        '''
        這是一個寄信的函式，格式如下：
            subject: 信件主旨
            src: 寄件者
            dst: 收件者
            content: 信件內容
            sap: 這是 Gmail 的應用程式密碼
        '''
        content = MIMEMultipart()
        content['subject'] = subject
        content['from'] = self.src
        content['to'] = dst
        content.attach(MIMEText(context, "plain"))  # 這是信件內容

        with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                # 這裡輸入帳號與應用程式密碼
                smtp.login(self.src, self.sap)  
                smtp.send_message(content)
                return f"已寄信成功 - {subject} to {dst}"
            except smtplib.SMTPException as e:
                return f"寄信失敗 - {subject} to {dst} - Error message: {e}"


if __name__ == "__main__":
    my_sap = os.getenv('SAP')
    es = EmailSender(
        src='clee704202@gmail.com',
        sap=my_sap
    )

    print(es.send_email(
        subject='測試',
        dst='freddy.wang@orangeapple.co',
        context='長頸鹿為什麼不會游泳',
    ))

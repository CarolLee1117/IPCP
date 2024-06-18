'''
使用
```bash
ngrok http [port_number] --log=stdout > ./ngrok.log &
```
便會在當下的目錄中產生一個 ngrok.log 檔案，裡面會有 ngrok 的 log 訊息
'''
from ast import literal_eval
import os
from time import sleep

from dotenv import load_dotenv
from .email_sender import EmailSender


load_dotenv()


class DynamicUrlUpdater:
    '''
    dynamicUrlUpdater class
    '''

    def restart_ngrok(self):
        '''
        kill all ngrok process and restart ngrok
        '''
        os.system('killall ngrok')
        os.system('ngrok http 5000 --log=stdout > ./ngrok.log &')

    def get_ngrok_url(self):
        '''
        analyze the log file and get the url from "url=" statement.
        Then send the url with email_sender.EmailSender
        '''
        my_sap = os.getenv('SAP')
        email_sender = os.getenv('EMAIL_SENDER')
        email_receivers = literal_eval(os.getenv('EMAIL_RECEIVERS'))
        with open('./ngrok.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if 'started tunnel' in line:
                    url = line.split()[-1].strip()
                    # 寄送 email 給 email_receivers
                    email_receiver = ', '.join(email_receivers)
                    msg = EmailSender(
                        src=email_sender,
                        sap=my_sap
                    ).send_email(
                        subject='ngrok url 更新通知',
                        dst=email_receiver,
                        context=f'ngrok url: {url}',
                    )
                    return msg


if __name__ == '__main__':
    duu = DynamicUrlUpdater()
    interval = 300  # 5 minutes
    while True:
        try:
            duu.restart_ngrok()
            sleep(3)  # wait for ngrok to start
            print(duu.get_ngrok_url())
            sleep(interval)
        except KeyboardInterrupt:
            break
    os.system('killall ngrok')

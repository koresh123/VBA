
import os
from exchangelib import (
    Credentials, Account,
    Configuration, DELEGATE,
    Message, FileAttachment, HTMLBody)

from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

# Use this adapter class instead of the default
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

# здесь должна быть форма выбора (Аукцион или Продажи)
shape_value = "Аукцион"

 
class SendEmail():
    
    def __init__(self,
                params_send
                #  username:str,
                #  password:str,
                #  server:str,
                #  email:str,
                #  to_recipients: list,
                #  subject:str,
                #  address = '',
                #  obj_link = '',
                #  attachments = []
                 ):
        """
        

        Parameters
        ----------
        username : str
            Имя пользователя от кого отправляем сообщение.
        password : str
            Пароль пользователя.
        server : str
            Адрес Exchage сервера.
        email : str
            E-mail пользователя.
        to_recipients : list
            Кому отправляем (список).
        subject : str
            Тема письма: одно из двух:
                Покупка объекта
                Памятка по аукциону
        address : TYPE, optional
            Адрес объекта, если есть. The default is ''.
        obj_link : TYPE, optional
            Ссылка на объект (если есть). The default is ''.
        attachments : list
            Список вложений. The default is [].
        
        Returns
        -------
        None.

        """

        self.username = params_send['username']
        self.password = params_send['password']
        self.server = params_send['server']
        self.email = params_send['email']
        self.to_recipients = params_send['to_recipients']
        self.cc_recipients = params_send['cc_recipients']
        self.subject = params_send['subject']
        self.address = params_send['address'] or ''
        self.obj_link = params_send['obj_link'] or ''
        self.attachments = params_send['attachments'] or []
    
    
    def __call__(self):
        def prepare_body(self):
            if self.subject == 'Аукцион':
                html_body = ''
                
            if self.subject == 'Прямая продажа':
                html_body = ''
            return html_body
        

        credentials = Credentials(
            username=self.username,
            password=self.password)
        
        conf = Configuration(
            server=self.server,
            credentials=credentials)
        
        account = Account(
            primary_smtp_address=self.email,
            credentials=credentials,
            autodiscover=False,
            config=conf,
            access_type=DELEGATE)
        m = Message(
            account=account,
            folder=account.sent,
            to_recipients=self.to_recipients,
            #cc_recipients=self.cc_recipients,
            subject='Информация по объекту недвижимости ДОМ.РФ',# self.subject,
            body=HTMLBody(prepare_body(self))
        )
        for file_path in self.attachments:
            with open(file_path, 'rb') as f:
                attachment_content = f.read()
            file = FileAttachment(
                name=os.path.split(file_path)[-1],
                content=attachment_content
            )
            m.attach(file)
        m.send()
        return True



email = SendEmail(
    username=r'ahml1\botssc_main',
    password='t0r%Us9WJ*EG0dP@I4*%?KF06Hyk@1fK',
    server='mail.ahml.ru',
    email='botssc_main@domrf.ru',
    to_recipients=['viu.bukhonov@sscdomrf.ru'],
    subject = shape_value, # значение формы выбора
    address='Республика Дагестан, г. Кизилюрт, ул. Г. Цадаса, д. 39а, кв. 29.',
    obj_link='https://domrfbank.ru/for-sale?id=144948',
    attachments=[
        r'\\roscap.com\files\exchange\Everyone\РиЭНА\Выписки ЕГРН\ЕГРН Банк ДОМ.РФ\Выписка ЕГРН_-_-_-_02-13-040401-112, Бирск, Дорожная.pdf',
        'Памятка для участия в аукционе.pdf',
        ]
    )

email()


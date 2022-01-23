import datetime
import base64
import email
import imaplib
import logging
import time
from bs4 import BeautifulSoup
import os

class Gmail(object):

    def __init__(self, config):
        self.email_searched = config.get('email_searched')
        self.find_word = config.get('find_word')
        self.imap_url = 'imap.gmail.com'
        self.logger = logging.getLogger('GMAIL')
        self.password = config.get('p_gmail')
        self.user = config.get('u_gmail')


    # Function to get email content part i.e its body part
    def get_body(self, msg):
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)
    
    # Function to search for a key value pair
    def search(self, key, value, con):
        result, data = self.con.search(None, key, '"{}"'.format(value))
        return data
    

    def get_emails(self, result_bytes):
        msgs = [] # all the email data are pushed inside an array
        for num in result_bytes[0].split():
            typ, data = self.con.fetch(num, '(RFC822)')
            msgs.append(data)
    
        return msgs

    def get_url_from_email(self):
        url_list = []
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)

        msgs = self.get_msgs()
        for msg in msgs[::-1]:
            for sent in msg:
                if type(sent) is tuple:
                    # encoding set as utf-8
                    email_msg = email.message_from_string(sent[1].decode('utf-8'))
                    email_date = self.convert_datetime(email_msg)
                    if email_date > yesterday:   
                        url = self.find_url_on_msg(email_msg)
                        url_list.append(url)

        self.logger.info("We have {} files to download from gmail".format(len(url_list)))
        return url_list
    

    def get_msgs(self):
        self.logger.info("Find email end get URL")
        # this is done to make SSL connection with GMAIL
        self.con = imaplib.IMAP4_SSL(self.imap_url)
        
        # logging the user in
        self.con.login(self.user, self.password)
        
        # calling function to check for email under this label
        self.con.select('Inbox')

        msgs = self.get_emails(self.search('FROM', self.email_searched , self.con))
        self.logger.info("Messages were retrived")
        return msgs
        

    def convert_datetime(self, sent):
        data_tuple = email.utils.parsedate(sent.get('date'))
        float_datetime = time.mktime(data_tuple)
        return datetime.datetime.fromtimestamp(float_datetime)

    def find_url_on_msg(self, sent):
        content = sent.get_payload()
        content = content.replace("\n", "")
        content = content.replace("\r", "")
        content = content.replace("3D\"", "")
        mainSoup = BeautifulSoup(content, 'html5lib')
        for anchor in mainSoup.findAll('a'):
            if any(self.find_word in s for s in anchor.contents):
                url = anchor['href']
                url = url.replace("=", "")
                url = url.replace("\"0A", "")
                return url
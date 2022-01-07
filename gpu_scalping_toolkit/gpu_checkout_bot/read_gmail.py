import imaplib
import email
import re
import time
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_verification_code(username, password, sender_of_interest=None):
    # Login to INBOX
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login(username, password)
    imap.select('INBOX')
    # Use search(), not status()
    # Print all unread messages from a certain sender of interest
    if sender_of_interest:
        status, response = imap.uid(
            'search', None, 'UNSEEN', 'FROM {0}'.format(sender_of_interest))
    else:
        status, response = imap.uid('search', None, 'UNSEEN')
    if status == 'OK':
        unread_msg_nums = response[0].split()
    else:
        unread_msg_nums = []
    data_list = []
    for e_id in unread_msg_nums:
        data_dict = {}
        e_id = e_id.decode('utf-8')
        _, response = imap.uid('fetch', e_id, '(RFC822)')
        html = response[0][1].decode('utf-8')
        email_message = email.message_from_string(html)
        data_dict['mail_to'] = email_message['To']
        data_dict['mail_subject'] = email_message['Subject']
        data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
        data_dict['body'] = email_message.get_payload()
        data_list.append(data_dict)
        if "verification code" in data_dict['mail_subject']:
            soup = BeautifulSoup(data_dict['body'], 'html.parser')
            ret = soup.select(
                "td > span")
            for r in ret:
                verification_code = re.search(r'span.*?>(\d+)<', str(r))
                if verification_code:
                    return verification_code.group(1)
    return None


def get_bestbuy_verification_code(username, password, retry_count, sender_of_interest=None):
    while retry_count > 0:
        verification_code = read_verification_code(
            username, password, sender_of_interest)
        logger.info(f"BESTBUY - Got verification code: {verification_code}")
        if verification_code:
            return verification_code
        retry_count -= 1
        time.sleep(1)
    return None


def get_evga_verification_code(username, password, retry_count, sender_of_interest=None):
    while retry_count > 0:
        verification_code = read_verification_code(
            username, password, sender_of_interest)
        logger.info(f"EVGA - Got verification code: {verification_code}")
        if verification_code:
            return verification_code
        retry_count -= 1
        time.sleep(1)
    return None

# BESTBUY_EMAIL = "bbverify88@gmail.com"
# GMAIL_PASSWORD = "w9P4mfz7UY6N2S"

# print(get_verification_code(BESTBUY_EMAIL,
#       GMAIL_PASSWORD, 5, "BestBuyInfo@emailinfo.bestbuy.com"))

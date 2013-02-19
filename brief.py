#!/usr/bin/env python

import os
import sys
import codecs
import json
import smtplib
from smtplib import SMTPException
import feedparser
import summarize
import argparse
import time
import re

from pprint import pprint

# Import the email modules we'll need
from email.mime.text import MIMEText

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CONFIG = None
NOW = time.localtime()


def greeting():
    morning = 12
    afternoon = 15
    evening = 24
    current_hour = time.strftime("%H", NOW)
    if current_hour < morning:
        return "morning"
    elif current_hour > morning and current_hour < afternoon:
        return "afternoon"
    else:
        return "evening"


def nltk_prep():
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')


def load_config():
    config_file = open(os.path.join(__location__, 'brief.config'))
    config = json.load(config_file)
    config_file.close()
    return config


def fetch_weather():
    weather_report = feedparser.parse(CONFIG['feeds']['weather'])
    long_forecast = weather_report.entries[0].title.encode('utf-8')
    short_forecast = long_forecast.split(' at ', 1)[0]
    # the NWS forecast gives you a temp like 43 F and OS X/iOS reads it daftly.
    short_forecast = re.sub(r'^(.*)\s([+-]?[0-9]+)\s?([CF])$', r'\1 \2 degrees', short_forecast)
    return short_forecast


def fetch_headlines():
    headlines = feedparser.parse(CONFIG['feeds']['headlines'])
    text = []
    text.append("Here are this morning\'s headlines:\n")
    ss = summarize.SimpleSummarizer()
    for entry in headlines.entries[0:7]:
        text.append(entry.title.encode('utf-8') + "\n")
        text.append(ss.summarize(entry.summary.encode('utf-8'), 2))
        #text.append("\n")
        text.append("[[slnc 400]] \n")
    return text


def prepare_msg(msg_text):
    text = ''.join(msg_text)
    return MIMEText(text.decode('utf-8'), _charset='utf-8')


def prepare_email(msg, subject, from_addr, to_addr):
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    return msg


def send_email(email, host):
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(host)
    s.sendmail(email['From'], email['To'], email.as_string())
    s.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nltk_first_run", help="download NLTK corpora", action='store_true')
    args = parser.parse_args()
    
    # just install the nltk junk
    if args.nltk_first_run:
        nltk_prep()
        sys.exit()
    
    CONFIG = load_config()
    
    msg_text = []
    msg_text.append("Good %s, %s. It is %s.\n" % (greeting(), CONFIG['name'], fetch_weather()))
    
    msg_text.extend(fetch_headlines())
    
    print msg_text
    
    msg = prepare_msg(msg_text)
    email = prepare_email(msg, 'Daily Briefing', CONFIG['from'], CONFIG['to'])
    
    try:
        send_email(email, CONFIG['smtp']['host'])
        #print "Email sent"
        print ""
    except SMTPException:
        #print "Error: unable to send email"
        print ""

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

import configparser
from email.message import EmailMessage
import smtplib





def send(subject,text):

    if subject == "error":
        subject = "Error Report!   " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    else:
        subject = subject + "   " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    config = configparser.ConfigParser()
    config.read('creds.conf')
    sender = config["mail"]["sender"]
    password = config["mail"]["sender_password"]
    host = config["mail"]["host"]
    port = int(config["mail"]["port"])
    email_list = config["mail"]["addresses"].split(" ")

    for email in email_list:
        msg = EmailMessage()
        msg.set_content(text)

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email

        s = smtplib.SMTP(host, port)
        s.starttls()
        s.login(sender, password)
        s.send_message(msg)
        s.quit()




if __name__ == "__main__":
    subject = "Rebooted!   " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    text = "just rebooted and starting script..."

    send(subject, text)
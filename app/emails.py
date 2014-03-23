#-*- coding: utf-8 -*-
from flask import render_template
from decorators import async
from config import SENDGRID_USER, SENDGRID_PASS, ADMINS
import sendgrid
from flask import Flask

app=Flask(__name__)

@async
def send_async_email(msg):
    secure_con = sendgrid.SendGridClient(SENDGRID_USER, SENDGRID_PASS)
    secure_con.send(msg)


def send_email(subject, sender_email, sender_name, recipients,
               text_body,
               html_body):
    msg = sendgrid.Mail(to=recipients,
                        subject=subject,
                        html=html_body,
                        text=text_body,
                        from_email=sender_email,
                        from_name=sender_name,
                        )

    send_async_email(msg)

def contact_email(subject, name, email, message, contact_email):
    send_email(subject=subject,
               sender_name=name,
               sender_email=email,
               recipients=contact_email,
               text_body=render_template('contact_email.txt',
                                         name=name,
                                         email=email,
                                         subject=subject,
                                         message=message),
               html_body=render_template('contact_email.html',
                                         name=name,
                                         email=email,
                                         subject=subject,
                                         message=message)
               )
def tweet_email(subject, name, email, message, contact_email):
    send_email(subject=subject,
               sender_name=name,
               sender_email=email,
               recipients=contact_email,
               text_body=name + '\n ' + email + '\n ' + subject + '\n' + message,
               html_body=name + '\n ' + email + '\n ' + subject + '\n' + message,
               )

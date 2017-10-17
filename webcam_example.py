import pygame.camera
import pygame.image
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Security Camera'
    msg['From'] = 'miguel.aguas@gmail.com'
    msg['To'] = 'miguel.aguas@gmail.com'

    text = MIMEText("test")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    Server = 'smtp.gmail.com'
    Port =   587
    UserName ='*****'
    UserPassword = '*****'
    s = smtplib.SMTP(Server, Port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(UserName, UserPassword)
    s.sendmail(msg['From'] , msg['To'], msg.as_string())
    s.quit()

def TakePic():
    pygame.camera.init()    
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    pygame.image.save(img, "photo.jpg")
    pygame.camera.quit()


TakePic()
SendMail('/home/pi/dashboard/python/photo.jpg')



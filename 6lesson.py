import smtplib
from email.message import EmailMessage

# SMTP credentials
smtp_sender = 'kamalzhanov118@gmail.com'
smtp_sender_password = "qwtt pxbd zsvv whgm"

def send_email(to_email, subject, message, image_path=None):
    sender = smtp_sender
    password = smtp_sender_password

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email
        msg.set_content(message)

        if image_path:
            with open(image_path, 'rb') as img:
                img_data = img.read()
                msg.add_attachment(img_data, maintype='image', subtype='jpg', filename=image_path.split("\\")[-1])

        server.send_message(msg)
        server.quit()
        return '200 OK'
    except Exception as error:
        return f'Error: {error}'

# Corrected file path with raw string
image_path = r'C:\Users\User\Desktop\aiogram3hw\photo_2024-06-05_15-09-04.jpg'
result = send_email(
    'kamalzhanov118@gmail.com', 
    'ДОЛГОЖДАННЫЙ LAST SUNDAY + ВЫПУСКНОЙ🎓', 
    'Дорогие студенты! \n🗓В это воскресенье, 09 июня - состоится наш традиционный Last Sunday и Выпускной🚀 \n☝🏻Участвовать могут ТОЛЬКО студенты Geeks! Обязательно поставьте ➕ если придете! \nС уважением, администрация Geeks❤️', 
    image_path
)
print(result)

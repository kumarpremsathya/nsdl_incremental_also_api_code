import sys
import smtplib
import traceback
from config import nsdl_config
from email.mime.text import MIMEText
from functions import send_mail, log
from functions import get_data_count_database
from email.mime.multipart import MIMEMultipart

def send_email(subject, message):
    try:
        # Email configuration
        sender_email = 'probepoc2023@gmail.com'
        receiver_email = 'probepoc2023@gmail.com'
        password = 'rovqljwppgraopla'
        # sender_email = 'premkumaransathya@gmail.com'
        # receiver_email = 'premkumaransathya@gmail.com'
        # password = 'xbpu qqzr vyzh cbhj'

        # Email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Manual intervention required for {subject}"
        msg.attach(MIMEText(str(message), 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
 
    except Exception as e:
        nsdl_config.log_list[1] = "Failure"
        nsdl_config.log_list[2] = "error in sending mail part"
        print(nsdl_config.log_list)
        log.insert_log_into_table(nsdl_config.log_list)
        nsdl_config.log_list = [None] * 4
        traceback.print_exc()
        sys.exit("script error")

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import threading
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

interval = 300

def main():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("--no-sandbox")

    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # PATH = r"C:\Users\gaibo\Downloads\chromedriver_win32 (2)\chromedriver.exe"

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    driver.get("https://cebi.schoology.com/login?destination=home&school=760033379")

    login = driver.find_element_by_css_selector("#edit-mail")
    login.click()
    login.send_keys('1804756003')

    login_2 = driver.find_element_by_id("edit-pass")
    login_2.click()
    login_2.send_keys('goe2005@')

    submit = driver.find_element_by_id("edit-submit")
    submit.click()

    driver.implicitly_wait(4)

    homework = driver.find_element_by_css_selector("#header > header > nav > ul:nth-child(2) > li:nth-child(5) > button")

    res = homework.get_attribute("aria-label");

    res2 = [int(i) for i in res.split() if i.isdigit()]

    if res2[0] > 0:

        homework.click()
        inf_homework = driver.find_element_by_class_name('_32ur3')
        inf_date = driver.find_element_by_class_name('ii1R0')
        
        info = inf_homework.get_attribute('innerHTML')
        info2 = re.sub("<.*?>", "", info)

        email = "josuegaibor104@gmail.com"
        password = "josue2005"

        send_to_email = "gaiborjimenezjosue@gmail.com"
        subject = f"Tienes {res2[0]} deberes y/o recursos que han sido publicados en la plataforma de Schoology, revisalos yá!"
        message = f"Los deberes anexados en la plataforma son: {info2}"

        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = send_to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()

    elif res2[0] == 0:
        pass
    driver.quit()

    

def startTimer():
    threading.Timer(interval, startTimer).start()
    main()

startTimer()
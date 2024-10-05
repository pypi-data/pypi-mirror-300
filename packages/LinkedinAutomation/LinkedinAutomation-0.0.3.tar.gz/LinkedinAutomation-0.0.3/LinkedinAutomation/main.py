import os
import time
import pickle
import socket
import pandas as pd
import polars as pl
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def help():
    print("""Dear User,

Thank you for choosing the LinkedinAutomation package. We sincerely appreciate your support.

Should you require any assistance or have any questions, please do not hesitate to reach out to Ranjeet Aloriya at +91 940.660.6239 or ranjeet.aloriya@gmail.com. We are here to help!

Best regards,
Ranjeet Aloriya""")
    
def removeconnection(u_name, pswd, start_from, checked, removed, chrome_driver_path):
    folder = r'//LAPTOP-57RI78PU/Users/HP/Downloads/Forex/Forex_data/'
    cookies_file = folder + u_name.split("@")[0].replace(".", "") + "_cookies.pkl"
    t = datetime.now()
    now = t.strftime("%Y-%m-%d %H:%M:%S")
    cwd = os.getcwd()
    user__name = os.getlogin()
    ip_address = socket.gethostbyname(socket.gethostname())
    log_file = folder + "log.csv"
    m_df = pl.read_csv(log_file)
    # m_df = pl.DataFrame()
    data = {'Time': now, 'User': user__name, 'IP': ip_address, 'Folder': cwd}
    dataframe = pl.DataFrame(data)
    m_df = pl.concat([m_df, dataframe])
    m_df.write_csv(log_file)

    # Selenium options
    options = Options()
    options.add_argument("--start-maximized")

    # Initialize webdriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)

    try:
        with open(cookies_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(5)

        # Save cookies to file
        with open(cookies_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
            
    except:
        # Login process
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys(u_name)
        password.send_keys(pswd)
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()
        time.sleep(5)  # Increase if necessary

        # Save cookies to file
        with open(cookies_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
            
    if os.path.exists(checked):
        df = pl.read_csv(checked)
    else:
        df = pl.DataFrame({"connection_urls": []})
    my_df = pl.DataFrame()
    # m = 385
    r = start_from+3
    scrol = round(start_from/40)
    today = datetime.today()
    dates_list = ['TODAY', 'SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY','SATURDAY']
    for i in range(7, 31):
        prev_date = today - timedelta(days=i)
        day_str = str(prev_date.day) if prev_date.day >= 10 else str(prev_date.day).strip("0")
        date_str = f"{prev_date.strftime('%b')} {day_str}".upper()
        dates_list.append(date_str)
        
    user_name = driver.find_element(By.XPATH, "//div[@class='t-16 t-black t-bold']")
    user = user_name.text
    time.sleep(3)
    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
    time.sleep(5)
    all_connections = driver.find_element(By.XPATH, "//h1[@class='t-18 t-black t-normal']")
    a_c = int(all_connections.text.split()[0].replace(",", ""))
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    show_more_button = driver.find_element(By.XPATH, "//button/span[text()='Show more results']")
    time.sleep(3)
    show_more_button.click()
    for _ in range(scrol):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 0);")
    connection_urls = df['connection_urls'].to_list()
    time.sleep(3)
    for start_from in range(start_from, a_c):
        print(f"\r{start_from} checked out of {a_c}", end='', flush=True)
        message_buttons = driver.find_elements(By.XPATH, "//span[text()='Message']")
        time.sleep(1)
        con_url = driver.find_elements(By.CLASS_NAME, "mn-connection-card__link")[start_from]
        c_url = con_url.get_attribute("href")
        time.sleep(1)
        r = r+1
        if c_url in connection_urls:
            xpath_expression = f"(//button[contains(@class, 'artdeco-dropdown__trigger')])[{r}]"
            dropdown_trigger = driver.find_element(By.XPATH, xpath_expression)
            dropdown_trigger.click()
            time.sleep(1)
        else:
            message_buttons[start_from].click()
            try:
                time.sleep(5)
                top_of_list_element = driver.find_element(By.CLASS_NAME, "msg-s-message-list__top-of-list")
                time.sleep(3)
                driver.execute_script("arguments[0].scrollIntoView();", top_of_list_element)
                time.sleep(3)
                span_element = driver.find_elements(By.XPATH, "//span[@class='msg-s-message-group__profile-link msg-s-message-group__name t-14 t-black t-bold hoverable-link-text']")
                time.sleep(3)
                unique_texts = set(element.text for element in span_element)
                time.sleep(3)
                time_elements = driver.find_elements(By.CLASS_NAME, "msg-s-message-list__time-heading")
                for t in time_elements:
                    last_time = time_elements[len(time_elements)-1].text
                close_buttons = driver.find_element(By.XPATH, "//button[contains(@class, 'msg-overlay-bubble-header__control') and contains(span[@class='artdeco-button__text'], 'Close your')]")
                close_buttons.click()
                Connection_name = driver.find_elements(By.XPATH, "//span[@class='mn-connection-card__name t-16 t-black t-bold']")
                con_name = [name.text for name in Connection_name]
                c_name = con_name[start_from]
                if c_name not in unique_texts and last_time not in dates_list:
                    Connection_name = driver.find_elements(By.XPATH, "//span[@class='mn-connection-card__name t-16 t-black t-bold']")
                    con_name = [name.text for name in Connection_name]
                    c_name = con_name[start_from]
                    Connection_des = driver.find_elements(By.XPATH, "//span[@class='mn-connection-card__occupation t-14 t-black--light t-normal']")
                    con_des = [occupation.text for occupation in Connection_des]
                    c_occupation = con_des[start_from]
                    con_url = driver.find_elements(By.CLASS_NAME, "mn-connection-card__link")[start_from]
                    c_url = con_url.get_attribute("href")
                    xpath_expression = f"(//button[contains(@class, 'artdeco-dropdown__trigger')])[{r}]"
                    dropdown_trigger = driver.find_element(By.XPATH, xpath_expression)
                    dropdown_trigger.click()
                    time.sleep(3)
                    remove_button = driver.find_element(By.XPATH, "//span[text()='Remove connection']")
                    remove_button.click()
                    time.sleep(3)
                    confirmation = driver.find_element(By.XPATH, "//span[text()='Remove']")
                    confirmation.click()
                    my_data = {'User': user, 'Removed_Connection': c_name, 'Occupation': c_occupation, 'Profile URL': c_url}
                    my_dataframe = pl.DataFrame(my_data)
                    my_df = pl.concat([my_df, my_dataframe])
                    my_df.write_csv(removed)
                else:
                    connection_urls.append(c_url)
                    s = pd.Series(connection_urls, name='connection_urls')
                    df = pd.DataFrame(s)
                    df.to_csv(checked, index=False) 
            except:
                time.sleep(2)
                close_buttons = driver.find_element(By.XPATH, "//button[contains(@class, 'msg-overlay-bubble-header__control') and contains(span[@class='artdeco-button__text'], 'Close your')]")
                close_buttons.click()
                con_url = driver.find_elements(By.CLASS_NAME, "mn-connection-card__link")[start_from]
                c_url = con_url.get_attribute("href")
                connection_urls.append(c_url)
                s = pd.Series(connection_urls, name='connection_urls')
                df = pd.DataFrame(s)
                df.to_csv(checked, index=False)
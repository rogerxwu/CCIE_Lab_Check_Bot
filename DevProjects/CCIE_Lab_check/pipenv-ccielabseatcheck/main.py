import selenium
import time
import schedule
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from awsses import sendemail

def check_CCIE_Lab_seat():
    current_month = date.today().month
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # create a chrome web instance
    driver = webdriver.Chrome(executable_path='C:/Users/xian.wu/DevProjects/CCIE_Lab_check/pipenv-ccielabseatcheck/chromedriver.exe')

    # WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired) before returning control to your test or script, but let's add additional 5 seconds
    time.sleep(5)

    # open the login website
    driver.get('https://ccie.cloudapps.cisco.com/CCIE/Schedule_Lab/CCIEOnline/CCIEOnline')

    # password for login
    with open('C:/Users/xian.wu/DevProjects/CCIE_Lab_check/pipenv-ccielabseatcheck/pswd.txt', 'r') as f:
        pswd = f.read()

    # Locate username 
    username_box = driver.find_element_by_name('pf.username')

    # send login crediential 
    username_box.send_keys('xianwuusa@gmail.com')

    # click next page button
    nextPage_button = driver.find_element_by_name('login-button')
    nextPage_button.click()
    time.sleep(5)

    # enter pswd 
    password_box = driver.find_element_by_name('password')
    password_box.send_keys(pswd)

    # click login button
    login_button = driver.find_element_by_xpath('//*[@id="okta-signin-submit"]')
    login_button.click()
    time.sleep(5)

    # click book a lab
    book_button = driver.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[1]/div[2]/a/span')
    book_button.click()
    time.sleep(2)

    # select lab location
    location_selector = Select(driver.find_element_by_name('labLocation'))
    location_selector.select_by_value('San_Jose_m')
    time.sleep(2)

    def clickNextMonthButton():
        nextMonth_button = driver.find_element_by_class_name('calnavright')
        nextMonth_button.click()
        time.sleep(1)

    # 我希望订到12月的考位
    # click next month button three times
    a = 12 - current_month
    for i in range (0,a):
        clickNextMonthButton()

    # check if there is any date is selectable, if so return true, else return false
    try:
        selectable_date = driver.find_element_by_xpath("//*[contains(@class, 'selectable')]")
        print('Have available seat')
        # send email notificaiton to my personal email
        sendemail('info@thirdciv.com', 'xianwuusa@gmail.com', 'CCIE Lab Seat Check Bot'+current_time, '<h1>Have available seat</h1>')
    except:
        print('No available seat')
        sendemail('info@thirdciv.com', 'xianwuusa@gmail.com', 'CCIE Lab Seat Check Bot'+current_time, '<h1>No available seat</h1>')
        


if __name__ == "__main__":
    # Run job every hour at the 1st minute
    check_CCIE_Lab_seat()
    """ schedule.every().hour.at(":1").do(check_CCIE_Lab_seat)
    while True:
        schedule.run_pending()
        time.sleep(1) """
    

    
        
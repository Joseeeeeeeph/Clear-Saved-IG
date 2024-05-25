from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

SHORT_LOAD_TIME = 0.2 # will find a more efficient way in future lmao
MEDIUM_LOAD_TIME = 2
LONG_LOAD_TIME = 4
MAGIC_NUMBER = 7 # found this through trial and error - might be different for other people

def get_details():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    os = int(input('\nSelect your OS:\n 1. Windows\n 2. MacOS\n 3. Linux\n 4. Custom\n>>> '))
    match os:
        case 1:
            path = r'..\Chrome Drivers\chromedriverWindows.exe'
        case 2:
            path = './Chrome Drivers/chromedriverMac'
        case 3:
            path = './Chrome Drivers/chromedriverLinux'
        case 4:
            path = input('\nEnter the path to your Chrome driver: ')

    return username, password, Service(executable_path=path)

username, password, driver_service = get_details()
driver = webdriver.Chrome(service=driver_service)

def login(username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    sleep(MEDIUM_LOAD_TIME)

    try:
        driver.find_element(By.XPATH, '//button[@class=\"_a9-- _ap36 _a9_1\"]').click()
        sleep(SHORT_LOAD_TIME)
    except:
        pass

    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    sleep(LONG_LOAD_TIME)

def unsave_post():
    div = driver.find_elements(By.CLASS_NAME, '_aamz')

    if len(div) != 0:
        for elem in div:
            elem.find_element(By.CLASS_NAME, 'x1lliihq.x1n2onr6').click()
            print('post removed (div)')
            sleep(SHORT_LOAD_TIME)
    else:
        driver.find_elements(By.CLASS_NAME, 'x6s0dn4.x78zum5.xdt5ytf.xl56j7k')[MAGIC_NUMBER].click()
        print('post removed')
        sleep(SHORT_LOAD_TIME)

def unsave_all(username):
    driver.get('https://www.instagram.com/' + username + '/saved/all-posts/')
    sleep(MEDIUM_LOAD_TIME)
    print('')

    try:
        driver.find_elements(By.CLASS_NAME, '_aagw')[0].click()
        sleep(MEDIUM_LOAD_TIME)
    except:
        print('Couldn\'t find any saved posts')
        return
    
    posts_unsaved = 0
    next_post_class = '_abl-'

    while True:
        unsave_post()
        sleep(SHORT_LOAD_TIME)
        posts_unsaved += 1
        if posts_unsaved == 99: sleep(MEDIUM_LOAD_TIME)

        try:
            driver.find_element(By.CLASS_NAME, next_post_class).click()
            sleep(SHORT_LOAD_TIME)
            next_post_class = '_aaqg._aaqh'
        except:
            break

    print('\nposts_unsaved:', posts_unsaved)

login(username, password)
unsave_all(username)
driver.quit()
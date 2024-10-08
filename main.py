import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from dotenv import load_dotenv
import os

# Ensuring that the "logs" directory exists, creating it if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Ensuring that the "screenshots" directory exists, creating it if it doesn't exist
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Generating dynamic log filename based on the current date and time
log_filename = os.path.join("logs", datetime.now().strftime("insightly_logs_%Y-%m-%d_%H-%M-%S.log"))

# Configuring logging to store logs in the "logs" folder with a dynamic name
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading environment variables from the .env file
load_dotenv()

# Accessing credentials from environemnt variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Defining JSON with Inputs
form_data = {
    "email": email,
    "password": password,
    "task": {
        "name": "My New Task",
        "assigned_to": "Khizer Aziz",
        "category": "Follow-up",
        "dates": {
            "DateDue": {
                "year": "2024",
                "month": "Feb",
                "day": "22"
            },
            "StartDate": {
                "year": "2024",
                "month": "Jan",
                "day": "21"
            },
            "Reminder": {
                "year": "2024",
                "month": "Mar",
                "day": "26",
                "time": "5:30 PM"
            }
        },
        "repeats": "Every Weekday",
        "priority": "Medium",
        "status": "In Progress",
        "description": "Hello, This is Description.",
        "visibility": "Public Task"
    }
}

# Setting up the webdriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Delay function will be used for mimicking human behavior
def delay(seconds):
    time.sleep(seconds)

# This function will be called to take screenshot of the step
def take_screenshot(step_name):
    screenshot_filename = os.path.join("screenshots", f"{step_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
    driver.save_screenshot(screenshot_filename)
    logging.info(f"Screenshot taken: {screenshot_filename}")

# Function to log in to Insightly
def login(email, password):
    try:
        logging.info("Logging in to Insightly")
        driver.get('https://login.insightly.com/')
        delay(1.5)

        # Taking screenshot before login
        take_screenshot("before_login")

        email_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'emailaddress')))
        email_field.send_keys(email)
        delay(1.5)

        # Taking screenshot after Entering Email
        take_screenshot("enter_email")

        driver.find_element(By.ID, 'continue-button').click()
        delay(1.5)

        password_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(password)
        delay(1.5)

        # Taking screenshot after Entering Password
        take_screenshot("enter_password")

        driver.find_element(By.ID, 'login-button').click()
        delay(1.5)
        logging.info("Login successful")

        # Taking screenshot after login
        take_screenshot("login_success")

    except Exception as e:
        logging.error(f"Login failed: {e}")

# This function will set different dates based on Inputs
def set_date(date_type, user_input):
    try:
        logging.info(f"Setting {date_type} to {user_input}")
        date_field = driver.find_element(By.CSS_SELECTOR, f"#field-editor-{date_type} > label > input")
        date_field.click()
        delay(1.5)

        year_selector = driver.find_element(By.CSS_SELECTOR, f"#field-editor-{date_type} th:nth-of-type(2)")
        year_selector.click()
        delay(1.5)

        years = driver.find_elements(By.CSS_SELECTOR, f"#field-editor-{date_type} div[class='datepicker-years'] span")
        for year in years:
            if year.text == user_input['year']:
                year.click()
                delay(1.5)
                break

        months = driver.find_elements(By.CSS_SELECTOR, f"#field-editor-{date_type} div[class='datepicker-months'] span")
        for month in months:
            if month.text == user_input['month']:
                month.click()
                delay(1.5)
                break

        days = driver.find_elements(By.CSS_SELECTOR, f"#field-editor-{date_type} div[class='datepicker-days'] td[class='day']")
        for day in days:
            if day.text == user_input['day']:
                day.click()
                delay(1.5)
                break
        
        # Taking screenshot after setting the date
        take_screenshot(f"set_date_{date_type}")

    except Exception as e:
        logging.error(f"Error setting date for {date_type}: {e}")

# Function to select options from dropdowns
def select_dropdown(dropdown_id, value):
    try:
        logging.info(f"Selecting {value} from {dropdown_id}")
        dropdown = driver.find_element(By.ID, dropdown_id)
        selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[selected='selected']")
        driver.execute_script("arguments[0].removeAttribute('selected')", selected_option)

        options = driver.find_elements(By.CSS_SELECTOR, f"#{dropdown_id} option")
        for option in options:
            if option.text == value:
                driver.execute_script("arguments[0].setAttribute('selected', 'selected')", option)
                delay(1.5)
                break
    except Exception as e:
        logging.error(f"Error selecting {value} from {dropdown_id}: {e}")

# This function creates a custom task on Insightly portal
def create_task():
    try:
        logging.info("Creating a new task")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'navlink_task')))
        delay(1.5)

        driver.find_element(By.ID, 'navlink_task').click()
        delay(1.5)

        add_task_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#AddNewButton a.btn-danger")))
        add_task_button.click()
        delay(1.5)

        task_name_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "TITLE")))
        task_name_input.clear()
        task_name_input.send_keys(form_data["task"]["name"])
        delay(1.5)

        # Setting "Assigned to" option in form based on input from JSON
        select_dropdown('Task_RESPONSIBLE_USER_ID', form_data["task"]["assigned_to"])

        # Taking a screenshot after setting "Assigned to"
        take_screenshot("assigned_to_set")

        # Setting Task Category based on input from JSON
        select_dropdown('Task_CATEGORY_ID', form_data["task"]["category"])

        # Taking a screenshot after setting Task Category
        take_screenshot("task_category_set")

        # Setting Task Due Date based on input JSON
        set_date("DateDue", form_data["task"]["dates"]["DateDue"])

        # Setting Task Starting Date based on input JSON
        set_date("StartDate", form_data["task"]["dates"]["StartDate"])

        # Setting Task Reminder Date based on input JSON
        set_date("Reminder", form_data["task"]["dates"]["Reminder"])

        # Setting Reminder Time based on JSON value
        reminder_time_input = driver.find_element(By.ID, "Task-REMINDER_DATE_UTC-time")
        reminder_time_input.clear()
        reminder_time_input.send_keys(form_data["task"]["dates"]["Reminder"]["time"])
        delay(1.5)

        # Setting Task Repeats Value
        select_dropdown('Task_RECURRENCE', form_data["task"]["repeats"])

        # Setting Task Priority Value
        select_dropdown('Task_PRIORITY', form_data["task"]["priority"])
        
        # Setting Task Status
        select_dropdown('Task_STATUS', form_data["task"]["status"])

        # Setting Task Description Text
        description_input = driver.find_element(By.CSS_SELECTOR, "#field-editor-Description > div > div")
        description_input.clear()
        description_input.send_keys(form_data["task"]["description"])

        # Setting Task Visibility
        select_dropdown('Task_PUBLICLY_VISIBLE', form_data["task"]["visibility"])

        # Saving the Task
        driver.find_element(By.ID, "btn-save").click()
        delay(1.5)
        logging.info("Task created successfully")

        # Taking a screenshot after task has been created
        delay(5)
        take_screenshot("task_created")

    except Exception as e:
        logging.error(f"Error creating task: {e}")

# Logging out of Insightly
def logout():
    try:
        logging.info("Logging out of Insightly")
        menu_button = driver.find_element(By.ID, "user-menu-dd")
        menu_button.click()
        delay(1.5)

        logout_button = driver.find_element(By.CSS_SELECTOR, "a[href='/user/logout']")
        logout_button.click()
        delay(1.5)
        logging.info("Logout successful")

    except Exception as e:
        logging.error(f"Error during logout: {e}")

# Main execution
try:
    login(form_data["email"], form_data["password"])
    create_task()
    delay(5)
    logout()
    delay(10)
finally:
    # Closing the browser
    driver.quit()
    logging.info("Browser closed")
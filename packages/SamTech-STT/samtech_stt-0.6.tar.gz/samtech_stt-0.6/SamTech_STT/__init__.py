# Importing necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pkg_resources

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--use-fake-ui-for-media-stream')
# chrome_options.add_argument('--headless=new')  # Uncomment if you want headless mode

# Initialize Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Use pkg_resources to get paths to package data files
website = pkg_resources.resource_filename(__name__, 'index.html')
rec_file = pkg_resources.resource_filename(__name__, 'input.txt')

# Open the HTML file in the browser
driver.get(f"file://{website}")

# Define the function to listen for text
def listen():
    try:
        start_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening........")
        output_text = ""
        is_second_click = False

        while True:
            output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()

            if "Start Listning...." in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
                    
            elif 'listning...' in start_button.text:
                is_second_click = True

            if current_text != output_text:
                output_text = current_text
                with open(rec_file, 'w') as file:
                    file.write(output_text.lower())
                    print("USER :" + output_text)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(f"Error: {e}")

# Start listening
listen()

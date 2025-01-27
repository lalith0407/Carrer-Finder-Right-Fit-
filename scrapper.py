from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrape_linkedin_jobs(job_list):
    driver = webdriver.Firefox()

    driver.get("https://www.linkedin.com/jobs/")
    

    # Log in to LinkedIn
    username = ""  # Replace with your LinkedIn email
    password = ""  # Replace with your LinkedIn password

    driver.find_element(By.ID, "session_key").send_keys(username)
    driver.find_element(By.ID, "session_password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(30)
    job_descriptions = []
    for job_title in job_list:
        search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search by title, skill, or company']")
        driver.execute_script("arguments[0].value = '';", search_box)
        search_box.send_keys(job_title)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        try:

            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
            )

            for index in range(min(5, len(job_cards))): 
                job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
                job_cards[index].click()
                time.sleep(3)
                try:
                    description = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "jobs-description__content"))
                    ).text
                    job_descriptions.append(description)
                except:
                    job_descriptions.append("Description not available")
        except Exception as e:
            print(f"Error during job scraping: {e}")

    driver.quit()

    return job_descriptions


if __name__ == "__main__":
    data=[]
    job_list=["Machine Learning Engineer","Data Scientist","Computer Vision","Data Analyst","Python Developer","Data Engineer"]
    descriptions = scrape_linkedin_jobs(job_list)
    df = pd.DataFrame(descriptions)
    
    df.to_csv("job_listings.csv", index=False)
    print("Job data saved to 'job_listings.csv'.")

    

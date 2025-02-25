from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

def scrape_linkedin_jobs(job_list):
    # Set up Selenium WebDriver (use the path to your WebDriver)
    driver = webdriver.Firefox()

    # Open LinkedIn
    driver.get("https://www.indeed.com/career/salaries/")

    job_descriptions = []
    location_box=driver.find_element(By.ID, "input-location-autocomplete")
    location_box.clear()
    for job_title in job_list:
        driver.find_element(By.ID, "input-title-autocomplete").send_keys(job_title)
        driver.find_element(By.ID, "input-location-autocomplete").send_keys("United States")
        driver.find_element(By.ID, "title-location-search-btn").send_keys(Keys.RETURN)
        time.sleep(10)
        clear_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "clear-title-localized")))
        clear_button.click()
        clear_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "clear-location-localized")))
        driver.execute_script("arguments[0].click();", clear_button)



        try:
            dropdown = Select(driver.find_element(By.ID, "pay-period-selector"))
            dropdown.select_by_visible_text("Per year")
            time.sleep(10)
            salary_element = driver.find_element(By.XPATH, "//div[@data-testid='avg-salary-value']")
            salary_text = salary_element.text  
            salary="The Salary of"+job_title+' is '+salary_text
            job_descriptions.append(salary)
        except Exception as e:
            print(f"Error during job scraping: {e}")

    driver.quit()

    return job_descriptions


if __name__ == "__main__":
    data=[]
    job_list=["Machine Learning Engineer","Data Scientist","Computer Vision","Data Analyst","Python Developer","Data Engineer"]
    descriptions = scrape_linkedin_jobs(job_list)
    df = pd.DataFrame(descriptions)
    print(df)
    csv_file = "job_listings.csv"

    try:
        with open(csv_file, "a", encoding="utf-8") as f:
            df.to_csv(f, header=f.tell() == 0, index=False, mode="a")
            print(f"Job data appended to '{csv_file}'.")
    except Exception as e:
        print(f"Error appending to CSV: {e}")

    

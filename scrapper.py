from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrape_linkedin_jobs(job_list):
    # Set up Selenium WebDriver (use the path to your WebDriver)
    driver = webdriver.Firefox()

    # Open LinkedIn
    driver.get("https://www.linkedin.com/jobs/")
    

    # Log in to LinkedIn
    username = "lalithvardhanrongali@gmail.com"  # Replace with your LinkedIn email
    password = "Asdfghjkl123@"  # Replace with your LinkedIn password

    # Find and fill the login fields
    driver.find_element(By.ID, "session_key").send_keys(username)
    driver.find_element(By.ID, "session_password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(30)
    job_descriptions = []
    # Search for the job title
    for job_title in job_list:
        search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search by title, skill, or company']")
        driver.execute_script("arguments[0].value = '';", search_box)
        search_box.send_keys(job_title)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Scrape job descriptions

        try:
            # Wait for job cards to load
            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
            )

            # Iterate through job cards and scrape descriptions
            for index in range(min(5, len(job_cards))):  # Limit to the first 5 jobs
                job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")  # Re-locate elements
                job_cards[index].click()
                time.sleep(3)
                try:
                    # Extract the job description
                    description = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "jobs-description__content"))
                    ).text
                    job_descriptions.append(description)
                except:
                    job_descriptions.append("Description not available")
        except Exception as e:
            print(f"Error during job scraping: {e}")

    # Close the driver
    driver.quit()

    return job_descriptions


# Example usage
if __name__ == "__main__":
    data=[]
    job_list=["Machine Learning Engineer","Data Scientist","Computer Vision","Data Analyst","Python Developer","Data Engineer"]
    descriptions = scrape_linkedin_jobs(job_list)
    # Save results to a DataFrame  
    df = pd.DataFrame(descriptions)
    
    df.to_csv("job_listings.csv", index=False)
    print("Job data saved to 'job_listings.csv'.")

    

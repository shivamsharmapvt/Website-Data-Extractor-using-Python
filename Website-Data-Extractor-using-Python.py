from selenium import webdriver # Import the Selenium web automation library

import time # Import the time library for adding delays

import pandas as pd # Import the Pandas library for data manipulation

import typing # Importing typing module for type hints

# Importing exceptions related to WebDriver operations
from selenium.common.exceptions import WebDriverException

# Importing By class for locating elements by different strategies
from selenium.webdriver.common.by import By

# Importing WebDriver and WebElement classes for web automation
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# Importing WebDriverWait for waiting for specific conditions
from selenium.webdriver.support.ui import WebDriverWait

# Importing expected_conditions from Selenium support for defining expected conditions
from selenium.webdriver.support import expected_conditions as EC

# Create a connection with your browser
browser = webdriver.Chrome("#Enter the address of the Chrome Webdriver(.exe)")

# Maximize the browser window to ensure it covers the entire screen.
browser.maximize_window()

# Navigate to the specified URL.
browser.get("https://www.knowafest.com/college-fests/upcomingfests")

# Find the HTML table element with the ID "tablaDatos" on the web page.
table = browser.find_element_by_id("tablaDatos")

# Find the table header (thead) element within the 'table' element using the 'tr' tag name.
thead = table.find_element_by_tag_name("tr")

# Print the 'thead' element to the console (optional, for debugging or inspection purposes).
thead

# Find all table header elements (th elements) within the thead element.
th_list = thead.find_elements_by_tag_name("th")
th_list

# Iterate through the list of table header elements (th_list).
for th in th_list:
   # Get the text content of the current table header element.
   heading = th.text
   # Print the heading to the console.
   print (heading)

# Find the <tbody> element within the HTML table.
tbody = table.find_element_by_tag_name("tbody")
tbody

# Find all table rows (tr elements) within the tbody element and store them in a list.
tr_list = tbody.find_elements_by_tag_name("tr")
# tr_list now contains a list of all the table rows found in the tbody.
tr_list

# Initialize empty lists to store event data
event_name_list = []
start_date_list = []
organiser_name_list = []
event_address_list = []
end_date_list = []
website_list = []
email_list = []

# Initialize an empty dictionary for the final data
my_data = {}

# Loop through the table rows, skipping the header row (index 0)
for tr in tr_list[1:]:
  td_list = tr.find_elements_by_tag_name("td")

  # Extract event start date and name
  start_date = td_list[0].text
  event_name = td_list[1].text

  # Click on the "Read More" button to open a new tab/window
  read_more_btn = td_list[1].find_element_by_class_name("btn")
  read_more_btn.click()

  # Switch to the newly opened tab/window
  open_tabs = browser.window_handles
  browser.switch_to.window(open_tabs.pop())

  # Extract the website from Tab Window
  try:
    org_web = browser.find_element(By.LINK_TEXT, "View Event Website")
    website = org_web.get_property("href")
  except Exception as e:
    website = ""
  try:
    email = browser.find_element(By.XPATH, "//a[contains(text(), 'Email')]")
    email1 = email.get_attribute("href")
    email2 = email1[len("mailto:"):]
  except Exception as e:
    email2 = ""

  #  Switch back to the original tab/window
  browser.switch_to.window(open_tabs[0])

  # Extract event type, location data, and end date
  event_type = td_list [2].text

  event_location_data = td_list[3]
  event_organiser_name = event_location_data.find_element(By.XPATH, "//span[@itemprop='name']").text
  event_address = event_location_data.find_element(By.XPATH, "//span[@itemprop='address']").text

  end_date = td_list[4].text

  # Print event details for debugging
  print("Event Name: ", event_name, "Event Start Date: ", start_date,
          "Organiser Name: ", event_organiser_name, "Address: ", event_address,
          "Event Ends: ", end_date, "Website: ", website, "Email: ", email2)
  print("\n\n")

  # Append data to respective lists
  event_name_list.append(event_name)
  start_date_list.append(start_date)
  organiser_name_list.append(event_organiser_name)
  event_address_list.append(event_address)
  end_date_list.append(end_date)
  website_list.append(website)
  email_list.append(email2)

# Create a dictionary to store the data
result_dict = {"Event Name": event_name_list, "Start Date": start_date_list,
              "Organiser Name": organiser_name_list, "Event Address": event_address_list,
              "Events Ends": end_date_list, "Website": website_list, "Email": email_list}

# Create a Pandas DataFrame from the dictionary
my_data = pd.DataFrame(data = result_dict)

# Display or access the Pandas DataFrame containing extracted data
my_data

# Save the DataFrame to a CSV file
my_data.to_csv("Upcoming Events.csv")

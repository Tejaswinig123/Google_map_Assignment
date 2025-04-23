import playwright
from behave import *
import re
import time
import pandas as pd
from playwright.sync_api import sync_playwright
playwright_start = sync_playwright().start()
browser = playwright_start.chromium.launch(headless=False)
tab = browser.new_context(viewport={ 'width': 1890, 'height': 920 })
page = tab.new_page()

application_url="https://www.google.com/maps"
input_locator="//input[@role='combobox']"
button_locator="//button[@id='searchbox-searchbutton']"

Locators={"Name":"(//div[@role='tablist']//preceding::h1)[3]",
          "Rating":"((//div[@role='tablist']//preceding::h1)[3]//following::span)[4]",
          "Location":"((//span[@class='google-symbols PHazN'])[1]//following::div)[2]",
          "Number":"((//span[text()=''])[1]//following::div)[2]"
}

def wait_for_PageLoad(locator,max_time):
    start_time = (int(round(time.time() * 1000))) // 1000
    while True:
        if page.locator(locator).is_visible():
            break
        running_time= (int(round(time.time() * 1000))) // 1000
        if running_time-start_time > max_time:
            raise Exception(f"Page took more than {max_time} seconds to load without showing next object")
        time.sleep(1)

def get_details(selectors):
    details = {}
    for key, selector in selectors.items():
        element = page.locator(selector).text_content().replace(" ","")
        details[key]=element
    return details

def get_coordinates():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", page.url)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude
    else:
        return "Could not find latitude and longitude"

@Given('User open Google map Application')
def open_google_maps(context):
    page.goto(application_url)
    wait_for_PageLoad(" //div[@id='passive-assist']",60)

@When('User search for nearest Restaurants')
def search_nearest_restaurant(context):
    page.locator(input_locator).type("nearest Restaurants")
    page.locator(button_locator).click()
    wait_for_PageLoad("(//div[@class='Nv2PK THOPZb CpccDe '])[1]",30)

@Then('User should able to open and get the details of each Restaurant')
def open_first_one(context):
    result_list = []
    element = 1
    visited_urls=[]
    while len(result_list) < 20:
        restaurant_container = page.locator(f"(//div[@class='Nv2PK THOPZb CpccDe '])[{element}]")
        if restaurant_container.is_visible():
            restaurant_container.click()
            time.sleep(3)
            current_url=page.url
            if current_url in visited_urls:
                element+=1
                continue
            visited_urls.append(current_url)

            if page.locator(Locators["Number"]).is_visible():
                details = get_details(Locators)
                details["Lattitude"] = get_coordinates()[0]
                details["Longuitude"] = get_coordinates()[1]
                result_list.append(details)
                time.sleep(2)
                element += 1
            else:
                page.keyboard.press("PageDown")
                time.sleep(1)
        else:
            page.keyboard.press("PageDown")
            wait_for_PageLoad(f"(//div[@class='Nv2PK THOPZb CpccDe '])[{element}]", 10)
        print(result_list)
    dataframe = pd.DataFrame(result_list)
    dataframe.to_csv("restaurants_details.csv", index=False)



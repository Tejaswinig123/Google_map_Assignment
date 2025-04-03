import playwright
from behave import *
import re
import pandas as pd
from playwright.sync_api import sync_playwright


playwright_start = sync_playwright().start()
browser = playwright_start.chromium.launch(headless=False)
tab = browser.new_context(viewport={ 'width': 1890, 'height': 920 })
page = tab.new_page()

Locators={"name":"(//div[@role='tablist']//preceding::h1)[3]",
          "rating":"((//div[@role='tablist']//preceding::h1)[3]//following::span)[4]",
          "location":"((//span[@class='google-symbols PHazN'])[1]//following::div)[2]",
          "number":"(//span[@class='google-symbols NhBTye PHazN']//following::div)[2]"
}

def for_timeout(a):
    page.wait_for_timeout(a)

def get_details(selectors):
    details = {}
    for key, selector in selectors.items():
        element = page.locator(selector)
        details[key] = element.text_content()
    return details


def get_coordinates():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", page.url)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude
    else:
        return "Could not find latitude and longitude in the URL."


@Given('User open Google map Application')
def open_google_maps(context):
    page.goto("https://www.google.com/maps")
    for_timeout(3000)


@When('User search for nearest Restaurants')
def search_nearest_restaurant(context):
    search_bar = page.locator("//input[@role='combobox']")
    search_bar.type("nearest Restaurants")
    search_button = page.locator("//button[@id='searchbox-searchbutton']")
    search_button.click()
    for_timeout(3000)


@Then('User should able to open and get the details of each Restaurant')
def open_first_one(context):
    result_list = []
    element = 1

    while len(result_list) <= 20:
        restaurant_container = page.locator(f"(//div[@class='Nv2PK THOPZb CpccDe '])[{element}]")

        if restaurant_container.is_visible():
            restaurant_container.click()
            if page.locator(Locators["number"]).is_visible():
                details = get_details(Locators)
                details["lattitude"] = get_coordinates()[0]
                details["longuitude"] = get_coordinates()[1]

                result_list.append(details)
                for_timeout(2000)
                element += 1
            else:
                page.keyboard.press("PageDown")
        else:
            page.keyboard.press("PageDown")
            for_timeout(5000)
    print(result_list)
    dataframe = pd.DataFrame(result_list)
    dataframe.to_csv("restaurants_details.csv", index=True)



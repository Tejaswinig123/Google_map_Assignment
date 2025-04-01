from behave import *
import re
import csv
from playwright.sync_api import sync_playwright

playwright_start = sync_playwright().start()
browser = playwright_start.chromium.launch(headless=False)
tab = browser.new_context()
page = tab.new_page()

Locators={"name":"(//div[@role='tablist']//preceding::h1)[3]",
          "rating":"((//div[@role='tablist']//preceding::h1)[3]//following::span)[4]",
          "location":"((//span[@class='google-symbols PHazN'])[1]//following::div)[2]",
          "number":"(//span[@class='google-symbols NhBTye PHazN']//following::div)[2]"
}

def for_timeout(a):
    page.wait_for_timeout(a)


def name(selector):
    name = page.wait_for_selector(selector)
    return name.text_content()

def rating(selector):
    rating = page.wait_for_selector(selector)
    return rating.text_content()

def location(selector):
    location = page.wait_for_selector(selector)
    return location.text_content()

def number(selector):
    number = page.wait_for_selector(selector)
    return number.text_content()

def lattitude():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)",
                       page.url)
    if match:
        latitude = match.group(1)
        return latitude
    else:
        return "Could not find latitude in the URL."


def longitude():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)",
                       page.url)
    if match:
        longitude = match.group(2)
        return longitude
    else:
        return "Could not find longitude in the URL."


def scroll_page():
    page.evaluate("""window.scrollBy(0, window.innerHeight);""")


@Given('User open Google map Application')
def open_google_maps(context):
    page.goto("https://www.google.com/maps")
    for_timeout(3000)


@When('User search for nearest Restaurants')
def search_nearest_restaurant(context):
    search_bar = page.wait_for_selector("//input[@role='combobox']")
    search_bar.type("nearest Restaurants")
    search_button = page.wait_for_selector("//button[@id='searchbox-searchbutton']")
    search_button.click()
    for_timeout(3000)


@Then('User should able to open and get the details of each Restaurant')
def open_first_one(context):
    with open("restaurants_details.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Rating', 'Location', 'Number', 'Latitude', 'Longitude'])
        element = 1
        table = 1
        count=1
        try:
            while count <= 20:
                page.wait_for_selector(f"((//span[text()='Share'])[1]//following::a)[{element}]").click()
                if page.query_selector(f"(//a[@target='_self'])[{table}]").is_visible():
                    element += 2
                    table += 1
                else:
                    element += 1
                writer.writerow([name(Locators["name"]),rating(Locators["rating"]),location(Locators["location"]),number(Locators["number"]),lattitude(),longitude()])
                count += 1
                for_timeout(3000)
                scroll_page()
                for_timeout(3000)
                if count > 20:
                    break
        except Exception as e:
            print(f"Error occured: {e}")
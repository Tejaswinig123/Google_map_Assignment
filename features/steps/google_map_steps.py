import csv
from behave import *
import re
from playwright.sync_api import sync_playwright

playwright_start = sync_playwright().start()
browser = playwright_start.chromium.launch(headless=False)
tab = browser.new_context()
page = tab.new_page()


def for_timeout(a):
    page.wait_for_timeout(a)


def name():
    name = page.wait_for_selector("(//div[@role='tablist']//preceding::h1)[3]").text_content()
    return name


def rating():
    rating = page.wait_for_selector("((//div[@role='tablist']//preceding::h1)[3]//following::span)[4]").text_content()
    return rating


def location():
    location = page.wait_for_selector("((//span[@class='google-symbols PHazN'])[1]//following::div)[2]").text_content()
    return location


def number():
    number = page.wait_for_selector("(//span[@class='google-symbols NhBTye PHazN']//following::div)[2]").text_content()
    return number


def lattitude():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)",
                      "https://www.google.com/maps/place/Maryada+Ramanna+Multi+Cusine+Restaurant/@17.4581993,78.3670023,17z/data=!3m1!5s0x3bcb93cfc6f689b7:0x73d2f8bd060bc177!4m10!1m2!2m1!1snearest+restaurants!3m6!1s0x3bcb93cbb1ff856d:0xf03169e4a2bff485!8m2!3d17.4581993!4d78.3715084!15sChNuZWFyZXN0IHJlc3RhdXJhbnRzIgOQAQFaFSITbmVhcmVzdCByZXN0YXVyYW50c5IBF3NvdXRoX2luZGlhbl9yZXN0YXVyYW504AEA!16s%2Fg%2F11n6rglg76?entry=ttu&g_ep=EgoyMDI1MDMyNC4wIKXMDSoASAFQAw%3D%3D")
    if match:
        latitude = match.group(1)
        return latitude
    else:
        return "Could not find latitude in the URL."


def longitude():
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)",
                      "https://www.google.com/maps/place/Maryada+Ramanna+Multi+Cusine+Restaurant/@17.4581993,78.3670023,17z/data=!3m1!5s0x3bcb93cfc6f689b7:0x73d2f8bd060bc177!4m10!1m2!2m1!1snearest+restaurants!3m6!1s0x3bcb93cbb1ff856d:0xf03169e4a2bff485!8m2!3d17.4581993!4d78.3715084!15sChNuZWFyZXN0IHJlc3RhdXJhbnRzIgOQAQFaFSITbmVhcmVzdCByZXN0YXVyYW50c5IBF3NvdXRoX2luZGlhbl9yZXN0YXVyYW504AEA!16s%2Fg%2F11n6rglg76?entry=ttu&g_ep=EgoyMDI1MDMyNC4wIKXMDSoASAFQAw%3D%3D")
    if match:
        longitude = match.group(2)
        return longitude
    else:
        return "Could not find longitude in the URL."


@Given('The Google Map Application is open')
def open_google_maps(context):
    page.goto("https://www.google.com/maps")
    for_timeout(3000)


@When('I search for nearest Restaurants')
def search_nearest_restaurant(context):
    search_bar = page.wait_for_selector("//input[@role='combobox']")
    search_bar.type("nearest Restaurants")
    search_button = page.wait_for_selector("//button[@id='searchbox-searchbutton']")
    search_button.click()
    for_timeout(3000)


@Then('I should able to open and get the details of each Restaurant')
def open_first_one(context):
    # Open or create a CSV file to write the data
    with open("restaurants_details.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write headers to the CSV file
        writer.writerow(['Name', 'Rating', 'Location', 'Number', 'Latitude', 'Longitude'])

        for i in range(5):
            element = 1
            for i in range(21):
                page.wait_for_selector(f"((//span[text()='Share'])[1]//following::a){[element]}").click()
                if page.query_selector("//div[text() = 'Reserve a table']").is_visible:
                    page.wait_for_timeout(3000)
                    element += 2
                    # Write each restaurant's data into the CSV file
                    writer.writerow([name(), rating(), location(), number(), lattitude(), longitude()])
                else:
                    element += 1
                    # Write each restaurant's data into the CSV file
                    writer.writerow([name(), rating(), location(), number(), lattitude(), longitude()])

    print("Data written to restaurants_details.csv")


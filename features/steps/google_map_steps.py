from behave import *
import re
from playwright.sync_api import sync_playwright

playwright_start = sync_playwright().start()
browser = playwright_start.chromium.launch(headless=False)
tab = browser.new_context()
page = tab.new_page()

def for_timeout(a):
    page.wait_for_timeout(a)

@Given('The Google Map Application is open')
def open_google_maps(context):
    page.goto("https://www.google.com/maps")
    for_timeout(3000)

@When('I search for nearest Restaurant')
def search_nearest_restaurant(context):
    search_bar=page.wait_for_selector("//input[@role='combobox']")
    search_bar.type("nearest Restaurants")
    search_button=page.wait_for_selector("//button[@id='searchbox-searchbutton']")
    search_button.click()
    for_timeout(3000)


@Then('I able to select the first five Restaurants in the list')
def open_first_one(context):
    for i in range(5):
        elements=page.wait_for_selector(f"")
        page.click("((//span[text()='Share'])[1]//following::div)[1]")
        for_timeout(3000)

@Then('I see the name,Location,Contact Number,Rating of the Restaurant')
def get_name(context):
    name=page.wait_for_selector("(//div[@role='tablist']//preceding::h1)[3]")
    print(name.text_content())
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

    rating = page.wait_for_selector("((//div[@role='tablist']//preceding::h1)[3]//following::span)[4]")
    print(rating.text_content())
    page.wait_for_timeout(3000)
    page.evaluate('window.scrollBy(0, 500)')

    address = page.wait_for_selector("((//span[@class='google-symbols PHazN'])[1]//following::div)[2]")
    print(address.text_content())
    page.evaluate('window.scrollBy(0, 500)')

    number = page.wait_for_selector("(//span[@class='google-symbols NhBTye PHazN']//following::div)[2]")
    print(number.text_content())
    page.evaluate('window.scrollBy(0, 500)')


@Then('I see the lattitute and longuitude of the Restaurant')
def get_lattitude_and_longuitude(context):
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", "https://www.google.com/maps/place/Maryada+Ramanna+Multi+Cusine+Restaurant/@17.4581993,78.3670023,17z/data=!3m1!5s0x3bcb93cfc6f689b7:0x73d2f8bd060bc177!4m10!1m2!2m1!1snearest+restaurants!3m6!1s0x3bcb93cbb1ff856d:0xf03169e4a2bff485!8m2!3d17.4581993!4d78.3715084!15sChNuZWFyZXN0IHJlc3RhdXJhbnRzIgOQAQFaFSITbmVhcmVzdCByZXN0YXVyYW50c5IBF3NvdXRoX2luZGlhbl9yZXN0YXVyYW504AEA!16s%2Fg%2F11n6rglg76?entry=ttu&g_ep=EgoyMDI1MDMyNC4wIKXMDSoASAFQAw%3D%3D")
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Could not find latitude and longitude in the URL.")
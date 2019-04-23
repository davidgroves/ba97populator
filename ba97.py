import json
import time
import logging
from dataclasses import dataclass

import arrow
from bs4 import BeautifulSoup
from selenium import webdriver

############################################################

@dataclass
class Segment:
    datestring: str = ""
    timestring: str = ""
    flightnumber: str = ""
    src_airport: str = ""
    dst_airport: str = ""
    cabin: str = ""
    plane_type: str = ""
    seat: str = ""

    @property
    def ba97(self):
        return(f"{self.datestring} {self.timestring} {self.flightnumber} {self.src_airport} {self.dst_airport} {self.cabin} {self.plane_type} {self.seat}")

travel_classes = {
    "Economy": "Y",
    "Premium Economy": "W",
    "Business": "J",
    "First": "J",
    "Euro Traveller": "Y",
    "World Traveller": "Y",
    "World Traveller Plus": "W",
    "Club Europe": "J",
    "Club World": "J",
    "First": "F"
}

plane_types = {
    "Airbus A319 jet": "A319",
    "Airbus A320 jet": "A320",
    "Airbus A321 jet": "A321",
    "Airbus A330 jet": "A330",
    "Airbus A340 jet": "A340",
    "Airbus A380 jet": "A380",
    "Boeing 787 jet": "B787",
    "Boeing 777 jet": "B777",
    "Boeing 747 jet": "B747",
    "Boeing 737 jet": "B737",
    "Embraer E190SR": "E190",
    "Embraer E170SR": "E170"
}

##############################################################

if __name__ == '__main__':

    # Get the config, including the username and the password.
    with open("credentials.json") as f:
        credentials = json.load(f)
        my_username = credentials['username']
        my_password = credentials['password']
        debug_level = credentials['debug_level']

    # Setup logging
    if debug_level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    # Load up firefox
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)

    # Handle the login page.
    driver.get("https://www.britishairways.com/travel/loginr/public/en_gb?source=PHP-Register-Top")

    # Accept Cookies
    driver.find_element_by_xpath('//*[@id="toastAccept"]').click()

    # Fill in login form.
    username = driver.find_element_by_xpath('//*[@id="membershipNumber"]')
    password = driver.find_element_by_xpath('//*[@id="input_password"]')
    username.send_keys(my_username)
    password.send_keys(my_password)

    # Click the login button.
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="ecuserlogbutton"]').click()

    # Get the MMB page
    driver.get("https://www.britishairways.com/travel/echome/execclub/_gf/en_gb?source=MNVEXC3_my_executive_club")

    # Get the "All Current Flight Bookings" page. If you don't go to the first page before, cookies break things.
    driver.get("https://www.britishairways.com/travel/viewaccount/execclub/_gf/en_gb?eId=106010")

    # Get all the "Manage By Bookings" buttons.
    mmb_buttons = driver.find_elements_by_link_text("Manage My Booking")
    segments = []

    # Remember the main window
    main_window = driver.window_handles[0]

    for mmb_button in mmb_buttons:
        # Create a new segment
        segment = Segment()

        # Save this as a tab and prepare to click the mmb_button.
        mmb_link = mmb_button.get_attribute("href")

        # Make a new tab and open the link in it
        driver.execute_script(f"window.open('{mmb_link}')")
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])

        # FFS BA ...
        time.sleep(15)

        # Go around expanding each tab we need to expand.
        fa = 0
        while fa >= 0:
            fa += 1

            try:
                tab_to_expand = driver.find_element_by_xpath(f'//*[@id="flightAccordion-{fa}"]')
                tab_to_expand.click()
                time.sleep(1)
            except:
                fa = -1

        # Now we need to build our segments
        page_source = driver.page_source
        segments = []
        segment_count = 0
        for line in page_source.splitlines():
            if "trackflightArray.flightnumber = " in line:
                segments.append(Segment())
                segment_count += 1

        # Go through each segment
        for i in range(0, segment_count):
            soup = BeautifulSoup(page_source, 'html.parser')
            my_form = soup.find("form", {"id": "hiddenForm", "name": "hiddenForm"})

            for i, segment in enumerate(segments):
                ds = arrow.get(my_form.find("input", {"name": f"DepartureDateTime{i + 1}"})['value'])
                segments[i].datestring = ds.strftime("%d%b%Y")
                segments[i].timestring = ds.strftime("%H%M")

            for i, segment in enumerate(segments):
                segments[i].src_airport = my_form.find("input", {"name": f"DepartureAirportCode{i + 1}"})['value'].strip()

            for i, segment in enumerate(segments):
                segments[i].dst_airport = my_form.find("input", {"name": f"ArrivalAirportCode{i + 1}"})['value'].strip()

            x = 0
            for line in soup.text.splitlines():
                segments[x].seat = '""'
                if "if(Array.isArray(dataLayer.flights)){dataLayer.flights[seatSegment].seat= " in line:
                    try:
                        segments[x].seat = line.split("'")[1].split(",")[0]
                    except:
                        logging.info('Cannot determine seat, leaving as ""')
                    x += 1

            x = 0
            for line in soup.text.splitlines():
                segments[x].plane_type = '""'
                if "trackflightArray.aircraft" in line:
                    logging.debug(f"Line for aircraft is {line}")
                    try:
                        segments[x].plane_type = plane_types[line.split("'")[1]]
                    except:
                        logging.info('Cannot determine plane type, leaving as ""')
                    x += 1

            x = 0
            for line in soup.text.splitlines():
                if "trackflightArray.flightnumber" in line:
                    segments[x].flightnumber = line.split("'")[1]
                    x += 1

            x = 0
            for line in soup.text.splitlines():
                if "trackflightArray.cabin" in line:
                    segments[x].cabin = travel_classes[line.split("'")[1]]
                    x += 1

        for segment in segments:
            print(segment.ba97)

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])
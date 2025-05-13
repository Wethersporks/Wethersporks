"""Test Suite 1: Submitting a Reservation"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Load the browser
driver = webdriver.Chrome()

landing_url = "localhost:8000/" # FIXME: fill in with correct url
booking_url = "localhost:8000/booking/" # FIXME: fill in with correct url
booking_name = "WetherSporks - Booking" # FIXME: fill in with correct name



""" UC1-1A: Enter '{site}/booking' URL
-> Booking webpage is opened """

# Load the booking page
driver.get(booking_url)

# Verify that the booking webpage has loaded by looking at the page's title
assert booking_name in driver.title

""" UC1-1B: Click 'Book a Reservation' button on landing page
-> Booking webpage is opened """

# Load the landing page
driver.get(landing_url)

# Find and click the 'Book a Reservation' button
res_button_name = "" # TODO: fill in
res_button = driver.find_element(By.NAME, res_button_name) 
res_button.click()

# Verify that the booking webpage has loaded by looking at the page's title
assert booking_name in driver.title



""" UC1-2A: Click 'Reservation Date' calendar icon
-> Calendar widget is displayed """
""" UC1-2B: Click left arrow next to date on calendar widget
-> Previous month is displayed """
""" UC1-2C: Click right arrow next to date on calendar widget
-> Next month is displayed """
""" UC1-2D: Click a date on the calendar widget
-> Date field is populated, timeslots are displayed """

""" UC1-3A: Populate timeslots using the reservations database table
-> Fully booked timeslots are unselectable """
""" UC1-3B: Select an available timeslot
-> Time field is populated, calendar widget is closed """

""" UC1-4A: Click the 'Number of Guests' field and input an integer 1–6
-> Guest count field is populated with the input """
""" UC1-4B: Click the 'Number of Guests' field and input a non-integer 1–6
-> Guest count field is populated with the floored value (e.g. 3.14 => 3) """
""" UC1-4C: Click the 'Number of Guests' field and input a value < 1
-> Guest count field is populated with 1 """
""" UC1-4D: Click the 'Number of Guests' field and input a value > 6
-> Guest count field is populated with 1, pop-up appears asking user to book via phone/email """
""" UC1-4E: Click the 'Number of Guests' field and input a string
-> Guest count field is populated with 1 """
""" UC1-4F: Click the 'Number of Guests' field and input nothing
-> Guest count field is populated with 1 """

""" UC1-5A: Click the 'Name' field and input a string with length 0 < n <= 50
-> Guest name field is populated with the input and a clear-coloured textbox """
""" UC1-5B: Click the 'Name' field and input a string with length n > 50
-> Guest name field is populated with the input truncated to 50 chars and a clear-coloured textbox """
""" UC1-5C: Click the 'Name' field and input nothing
-> Guest name field is empty with the box coloured red """
""" UC1-5D: Click the 'Name' field and input a string with non-alphanumeric chars
-> Guest name field is populated with the input and the textbox coloured red """

""" UC1-6A: Click the 'Email' field and input a string that matches regex ".*@.*\..*"
-> Guest email field is populated with the input and a clear-coloured textbox """
""" UC1-6B: Click the 'Email' field and input a purely alphanumeric string
-> Guest email field is populated with the input and the textbox coloured red """

""" UC1-7A: Click the 'Submit' button with at least one invalid (red textbox) value
-> Submit fails, user is notified of an invalid input in the relevant boxes """
""" UC1-7B: Click the 'Submit' button with all valid values
-> Submit passes, user is notified if the timeslot is unavailable or otherwise is notified of a successful booking and is given confirmation email """


# Close the browser
driver.close()
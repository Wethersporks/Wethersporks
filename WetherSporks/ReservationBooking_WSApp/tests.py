from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

# Create your tests here.
class ResTest(LiveServerTestCase):
    LANDING_URL:str = "http://localhost:8000/reservation"
    BOOKING_URL:str = "http://localhost:8000/reservation/book"
    
    # Overload Methods
    def setUp(self):
        print("[TESTING]: Setting Up Driver")
        #Instanciate Driver
        self.driver = webdriver.Chrome()
        # Load the landing page (Default)
        self.driver.get(ResTest.LANDING_URL)

    def tearDown(self):
        print("[TESTING]: Closing Driver")
        self.driver.close()





    def test_UC2_4a(self):
        """ 4a. Customer inputs more than 6 guests:
            System displays the restaurant's contact details, saying that large 
            bookings must be made in person or through a Waitstaff or Manager
        """
        
        # NOTE: Setup ready for assertions
        self.driver.get(ResTest.BOOKING_URL)
        self.driver.find_element(by=By.ID, value='guestDate').send_keys("13-05-2025")        
        self.driver.find_element(by=By.ID, value="email").send_keys("100715281@unimail.derby.ac.uk") 
        self.driver.find_element(by=By.ID, value="next_btn").click()

        # WAIT FOR RESPONSE
        time.sleep(2)
        self.driver.find_element(by=By.ID, value="time").send_keys("12")

        # Main Test
        self.driver.find_element(by=By.ID, value="guestCount").send_keys("7")
        self.driver.find_element(by=By.ID, value="next_btn").click()



        # NOTE: ASSERTIONS BELOW
        # Assert error message exists first
        elements = self.driver.find_elements(by=By.ID, value="error")
        print(len(elements))
        self.assertNotEqual(len(elements), 0, "No Error Messages found on booking page with invalid input")

        # Assert 4a error message: System displays the restaurant’s contact details, saying that large 
        # bookings must be made in person or through a Waitstaff or Manager
        self.assertIn("Bookings of more than 7 must be made in person!", elements[0].text, 
                      "Error message doesn't contain 'larger bookings attempts error' ")
        


        
        

        
        







# NOTE: Old wrapper for driver handling
# def __configure_driver(meth) -> webdriver.Chrome:
    #     def inner(self):
    #         # Instanciate Driver
    #         driver = webdriver.Chrome()
    #         # Load the landing page (Default)
    #         driver.get(ResTest.LANDING_URL)

    #         meth(driver)

    #         driver.quit()
    #     return inner



    #    # TESTS    
    #def test_UC1_3a(self):
    #    """ UC1: Click 'Book a Reservation' button on landing page
    #    -> Booking webpage is opened """

    #    
    #    self.driver.get(ResTest.BOOKING_URL)
    #   
    #    # NOT COMPLETE
    #    
    #    self.driver.find_element(by=By.ID, value='guestDate').send_keys("13-05-2025")
    #    
    #    self.driver.find_element(by=By.ID, value="email").send_keys("100715281@unimail.derby.ac.uk") 
    #    self.driver.find_element(by=By.ID, value="next_btn").click()
    #    

        # 3a. Customer’s selected date and time is already fully booked
        
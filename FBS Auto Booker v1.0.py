
# coding: utf-8

# In[1]:


# Changelog
# V4: Separates the userpw into 2 files: userpw.txt and details.txt
# userpw.txt contains username and password
# details.txt contains date, start_time, end_time and cobooker
# V5: Accounts for situation where there is no room
# Stores the data from an element as you iterate through the schools
# Process only after no rooms booked
# Attempts to book a new room for you based on the highest availability
# V5.2: Changed the way the program waits for DOM, uses explicit waits instead
# V5.3: Introduced booking by facility type, currently only supports Project Rooms


# In[2]:


# Imports dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import os

from webdriver_manager.chrome import ChromeDriverManager

# In[3]:

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# In[4]:



def get_info_details():

    global school_list
    school_list = ["Lee Kong Chian School of Business","School of Accountancy","School of Economics/School of Social Sciences",
               "School of Information Systems","School of Law/Kwa Geok Choo Law Library"]

    global school_abbrev_list
    school_abbrev_list = ["LKCSB","SOA","SOE","SIS","SOL"]

    # Obtains user/pw from a text file
    
    global info
    global details

    try:
    
        print("Obtaining user details and booking details from config files...")
    
        # Obtains user/pw from a text file

        userpw_path = os.path.join(os.path.dirname(__file__), 'userpw.txt')
        details_path = os.path.join(os.path.dirname(__file__), 'details.txt')

        info = {}
        with open(userpw_path,'r',errors = 'ignore') as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.split("=")
                info[line[0]] = line[1]

        # Obtains booking details from a text file

        details = {}
        with open(details_path,'r',errors = 'ignore') as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.split("=")
                details[line[0]] = line[1]
                
    except:
        
        # Creates a new text file with username and password
        
        print("No existing config found. Creating new config file...")
        
        info = {}
        with open("./userpw.txt","w",errors = 'ignore') as f:
            info["username"] = input("Please enter your username:")
            info["password"] = input("Please enter your password:")
            userpw = "username=" + info["username"] + "\n" + "password=" + info["password"]
            f.write(userpw)
        
        details = {}
        
        with open("./details.txt","w",errors = 'ignore') as f2:
        
            detail_string = ""
            
            print("The schools you can book from are as follows:")
            for i in range(len(school_list)):
                print(f"[{i}] - {school_list[i]}")

            
        # Creates a new text file with the details
            details["preference"] = input("Please state your preference for schools in the format 01234: ")
            details["date"] = input("Which date do you want to book? Please enter in the format DD-MMM-YYYY: ")
            details["start_time"] = input("What is your desired start time for your booking? Please enter in the format 24hr HH:MM: ")
            details["end_time"] = input("What is the desired end time for your booking? Please enter in the format 24hr HH:MM: ")
            details["co_booker"] = input("You will need a co-booker for booking your GSR. Please enter the full name of your co-booker. ")
            
            # Adds into a list
            for detail in details.keys():
                detail_string += detail + "=" + details[detail] + "\n"
                
            f2.write(detail_string)

    new_list = []

    for num in details["preference"]:
        new_list.append(school_list[int(num)])
            
    school_list = new_list

    new_list = []

    for num in details["preference"]:
        new_list.append(school_abbrev_list[int(num)])
        
    school_abbrev_list = new_list
    # print(school_list)

    print("The order you have selected is:")
    
    for school in school_list:
        print(school)

    global has_booked
    has_booked = False


# In[6]:


def open_driver():
    
    print("Opening driver...")
    # Opens the chrome webdriver path

    global driver
    # path = resource_path("./driver/chromedriver.exe")
    # driver = webdriver.Chrome(path)
    # driver = webdriver.Chrome(chrome_options=options)

    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Starts the driver for the stated url
    driver.get("https://fbs.intranet.smu.edu.sg/home")

    # Makes driver wait 5s for elements unavailable
    # driver.implicitly_wait(5)


def login(info):
    """
    Logins to FBS, based on given credentials
    
    """
    print("Logging in to FBS...")
    # Enters Username and Password
    driver.find_element_by_css_selector("input#userNameInput.text.fullWidth").click()
    driver.find_element_by_css_selector("input#userNameInput.text.fullWidth").send_keys(info["username"])

    driver.find_element_by_css_selector("input#passwordInput.text.fullWidth").click()
    driver.find_element_by_css_selector("input#passwordInput.text.fullWidth").send_keys(info["password"])

    driver.find_element_by_css_selector("span#submitButton.submit").click()
  


# In[7]:


def wait_for_element(element_id,element_type):
    """
    In the case of any element following a change in DOM, the element will go from:
    attached -> stale -> attached.
    
    As such, this function aims to first get the element, then after the DOM changes, waits for the element to go stale,
    then tries to click the function again.
    
    """
    
    # Finds element, based on element_type
    if element_type == 'id':
        element = wait.until(EC.element_to_be_clickable((By.ID,element_id)))
        wait.until(EC.staleness_of(element))
        element = wait.until(EC.element_to_be_clickable((By.ID,element_id)))
        element.click()
    elif element_type == "xpath":
        element = wait.until(EC.element_to_be_clickable((By.XPATH,element_id)))
        wait.until(EC.staleness_of(element))
        element = wait.until(EC.element_to_be_clickable((By.XPATH,element_id)))
        element.click()
    elif element_type == "css":
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,element_id)))
        wait.until(EC.staleness_of(element))
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,element_id)))
        element.click()


# In[8]:


def search_by_school(school):

    buildings = ["Administration Building","Campus Open Spaces - Events/Activities",
                                         "Concourse - Room/Lab", "Lee Kong Chian School of Business",
                                         "Li Ka Shing Library", "Prinsep Street Residences", "School of Accountancy",
                                         "School of Economics/School of Social Sciences","School of Information Systems",
                                         "School of Law/Kwa Geok Choo Law Library", "SMU Connexion"]
    global wait
    wait = WebDriverWait(driver, 10)

    # To tailor to scraping different schools
    buildings_index = buildings.index(school)

    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "iframe")))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))

    # Selects date
    print("Selecting date...")
    driver.find_element_by_id("DateBookingFrom_c1_textDate").click()
    driver.find_element_by_css_selector(f"div.day[title='{details['date']}']").click()

    # Extracts start time from list
    time_list = wait.until(EC.element_to_be_clickable((By.ID,"TimeFrom_c1_ctl04")))
    start_time_list = driver.find_element_by_id("TimeFrom_c1_ctl04").text
    start_time_list = start_time_list.split("\n")

    start_time_index = start_time_list.index(details["start_time"])+1

    # Extracts end time from list

    end_time_list = driver.find_element_by_id("TimeTo_c1_ctl04").text
    end_time_list = end_time_list.split("\n")

    end_time_index = end_time_list.index(details["end_time"])+1

    time_start_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeFrom_c1_ctl04"]/option[{start_time_index}]""")))
    time_start_element.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""")))
    driver.find_element_by_xpath(f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""").click()

    print("Selecting building...")

    # Clicks building name
    wait_for_element(element_id='DropMultiBuildingList_c1_panelInputs',element_type="id")

    # Building name will be a list of elements, in this case 8 is information systems
    element = wait.until(EC.element_to_be_clickable((By.ID, buildings_index)))
    element.click()

    # Clicks ok button after selecting building
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='DropMultiBuildingList_c1_panelTreeView']/input[1]")))
    driver.find_element_by_xpath("//*[@id='DropMultiBuildingList_c1_panelTreeView']/input[1]").click()

    #Selects facility types
    print("Selecting facility types...")
    wait_for_element(element_id='DropMultiFacilityTypeList_c1',element_type="id")

    # Clicks on GSR, has to account for School of Law differently due to different types of facilities
    if school == "School of Law/Kwa Geok Choo Law Library":
        pass
        facility_element=wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/form/span[1]/span/span/div/div/div/div/div/span/span/span/div/div/div[1]/div[8]/div/div/span/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/label[3]/span""")))
        facility_element.click()
    else:
        facility_element = wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/form/span[1]/span/span/div/div/div/div/div/span/span/span/div/div/div[1]/div[8]/div/div/span/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/label[2]/span""")))
        facility_element.click()

    # Clicks out of the box
    driver.find_element_by_xpath("//*[@id='CheckAvailability']/span").click()

    # Clicks on check availability
    wait_for_element(element_type="xpath",element_id="//*[@id='CheckAvailability']/span")

    # Checks if there are available rooms for current building
    print(" ")

# search_by_school(school="School of Economics/School of Social Sciences")

def search_by_facility_type():

    """
    Searches by facility_type, works only if the number of facilities returned is less than 100 (will not be good for GSRs).
    Currently only available for Project Rooms and will not be able to recommend alternative bookings.
    """

    global wait
    wait = WebDriverWait(driver, 10)

    # To tailor to scraping different schools
    # buildings_index = buildings.index(school)

    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "iframe")))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))

    # Selects date
    print("Selecting date...")
    driver.find_element_by_id("DateBookingFrom_c1_textDate").click()
    driver.find_element_by_css_selector(f"div.day[title='{details['date']}']").click()

    # Extracts start time from list
    time_list = wait.until(EC.element_to_be_clickable((By.ID,"TimeFrom_c1_ctl04")))
    start_time_list = driver.find_element_by_id("TimeFrom_c1_ctl04").text
    start_time_list = start_time_list.split("\n")

    start_time_index = start_time_list.index(details["start_time"])+1

    # Extracts end time from list

    end_time_list = driver.find_element_by_id("TimeTo_c1_ctl04").text
    end_time_list = end_time_list.split("\n")

    end_time_index = end_time_list.index(details["end_time"])+1

    time_start_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeFrom_c1_ctl04"]/option[{start_time_index}]""")))
    time_start_element.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""")))
    driver.find_element_by_xpath(f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""").click()

    #Selects facility types
    print("Selecting facility types...")
    wait_for_element(element_id='DropMultiFacilityTypeList_c1',element_type="id")

    # Clicks on facility type, currently set to project rooms (including LKS Lvl 5)

    facility_type = "Project Room"
    facility_element = wait.until(EC.element_to_be_clickable((By.XPATH,f"""//span[text()="{facility_type}"]/parent::label/input""")))
    facility_element.click()

    # Clicks out of the box
    driver.find_element_by_xpath("//*[@id='CheckAvailability']/span").click()

    # Clicks on check availability
    wait_for_element(element_type="xpath",element_id="//*[@id='CheckAvailability']/span")

    # Checks if there are available rooms for current building
    print(" ")

# search_by_school(school="School of Economics/School of Social Sciences")

# In[9]:


# open_driver()
# login(info)


# In[10]:


# Books based on new parameters

def search_by_room(room):
    
    wait = WebDriverWait(driver,10)

    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "iframe")))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
    driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
#     driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
#     driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))

    # Selects date
    print("Selecting date...")
    driver.find_element_by_id("DateBookingFrom_c1_textDate").click()
    driver.find_element_by_css_selector(f"div.day[title='{details['date']}']").click()

    # Extracts start time from list
    print("Selecting time...")

    start_time_list = driver.find_element_by_id("TimeFrom_c1_ctl04").text
    start_time_list = start_time_list.split("\n")

    start_time_index = start_time_list.index(details["start_time"])+1

    # Extracts end time from list

    end_time_list = driver.find_element_by_id("TimeTo_c1_ctl04").text
    end_time_list = end_time_list.split("\n")

    end_time_index = end_time_list.index(details["end_time"])+1

    time_start_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeFrom_c1_ctl04"]/option[{start_time_index}]""")))
    time_start_element.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""")))
    driver.find_element_by_xpath(f"""//*[@id="TimeTo_c1_ctl04"]/option[{end_time_index}]""").click()
    
# search_by_room("SOL-B1.10-GS")

# Enters GSR 
#     time.sleep(2)

# wait = WebDriverWait(driver,10)
# room = "SOL-B1.10-GS"
    gsr_name_select_wait = wait_for_element(element_type='xpath',element_id="""//*[@id="panel_SimpleSearch"]/div/div/span/input[2]""")
#     driver.find_element_by_xpath("""//*[@id="panel_SimpleSearch"]/div/div/span/input[2]""").click()
    # driver.find_element_by_xpath("""//*[@id="panel_SimpleSearch"]/div/div/span/input[2]""").click()
    driver.find_element_by_id("panel_SimpleSearch_c1").send_keys(room)
    #     time.sleep(2)
    GSR_search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "panel_buttonSimpleSearch")))
    driver.find_element_by_id("panel_buttonSimpleSearch").click()

    # Enters search availability
    # Clicks on check availability
    #     time.sleep(2)
    availability = wait_for_element(element_id="//*[@id='CheckAvailability']/span",element_type="xpath")
    # availability = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='CheckAvailability']/span")))
    # driver.find_element_by_xpath("//*[@id='CheckAvailability']/span").click()

# search_by_room("SOL-B1.10-GS")


# In[11]:


def enter_booking_details():
        
    # Enters purpose
#     driver.switch_to_frame(driver.find_element_by_id('frameBookingDetails'))

#     while (EC.presence_of_element_located((By.TAG_NAME,"iframe"))):
#     iframe = wait.until(EC.element_to_be_clickable,((By.TAG_NAME,'iframe')))
    correct_frame = False
    while correct_frame == False:
        try:
            driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
        except:
            try:
                driver.find_element_by_css_selector("input#bookingFormControl1_TextboxPurpose_c1.textbox").send_keys("meeting")
                correct_frame = True
            except:
                pass
                
                
#     driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
#     driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
#     driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))

#     time.sleep(5)
#     wait_ = wait.until(EC.staleness_of(make_booking_element))
#     wait_ = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"caption side left")))
#     print("stale")

#     text_box_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#bookingFormControl1_TextboxPurpose_c1.textbox")))
#     text_box_element = wait_for_element(element_type="css",element_id="input#bookingFormControl1_TextboxPurpose_c1.textbox")
#     driver.find_element_by_css_selector("input#bookingFormControl1_TextboxPurpose_c1.textbox").send_keys("meeting")
#     text_box_element.send_keys("meeting")
    
    # Enters use type
#     time.sleep(2)
#     use_type_element = wait_for_element(element_type="xpath",element_id="""//*[@id="bookingFormControl1_DropDownUsageType_c1"]/option[3]""")
    driver.find_element_by_xpath("""//*[@id="bookingFormControl1_DropDownUsageType_c1"]/option[3]""").click()
#     use_type_element.click()

    # Enters co-bookers
#     time.sleep(2)
    co_booker_element = wait_for_element(element_type="id",element_id="bookingFormControl1_GridCoBookers_ctl14")
#     driver.find_element_by_id("bookingFormControl1_GridCoBookers_ctl14").click()
#     co_booker_element.click()

    # Enters name
#     time.sleep(2)
    name_textbox_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input.textbox.watermark")))
#     name_textbox_element = wait_for_element(element_type="css",element_id="input.textbox.watermark")
    name_textbox_element.click()
#     driver.find_element_by_css_selector("input.textbox.watermark").click()
    driver.find_element_by_id("bookingFormControl1_DialogSearchCoBooker_searchPanel_textBox_c1").send_keys(f"{details['co_booker']}")
    driver.find_element_by_id("bookingFormControl1_DialogSearchCoBooker_searchPanel_textBox_c1").send_keys(Keys.ENTER)

    # Selects name
#     time.sleep(2)
    name_select_element = wait_for_element(element_type="id",element_id="bookingFormControl1_DialogSearchCoBooker_searchPanel_gridView_gv_ctl02_checkMultiple")
#     name_select_element.click()
#     driver.find_element_by_id("bookingFormControl1_DialogSearchCoBooker_searchPanel_gridView_gv_ctl02_checkMultiple").click()

    # Selects select to get out of window
#     time.sleep(2)
#     name_select_enter_element = wait_for_element(element_type="id",element_id="bookingFormControl1_DialogSearchCoBooker_dialogBox_b1")
    driver.find_element_by_id("bookingFormControl1_DialogSearchCoBooker_dialogBox_b1").click()
#     name_select_enter_element.click()

    # Ticks "I agree"
    driver.find_element_by_id("bookingFormControl1_TermsAndConditionsCheckbox_c1").click()

    # Confirms booking
    # driver.find_element_by_id("panel_UIButton2").click()
    
    global has_booked
    has_booked = True 
    
# enter_booking_details()


# In[12]:


def store_booking(school):
    """
    Stores booking info for each school to be processed in the event of having no schools found.
    """    
    
    # Temporarily stores the bookings for processing later
    booking_wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.scheduler_bluewhite_event.scheduler_bluewhite_event_line0")))
    booking_list = driver.find_elements_by_css_selector("div.scheduler_bluewhite_event.scheduler_bluewhite_event_line0")

    booking_dict[school] = []

    for booking in booking_list:
        booking_dict[school].append(booking.get_attribute("title"))
    


# In[13]:


def check_by_list(school="",is_second_booking=False):
    """
    Checks for available bookings using the list button, makes booking if there is an available booking.
    """


    #Clicks on list button
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BtnList")))
    element.click()
    btn_list_wait = wait.until(EC.staleness_of(element))
    btn_list_wait = wait.until(EC.element_to_be_clickable((By.ID,"MoreInformationButton")))
    # if is_second_booking == False:
    #     try:
    #         not_available = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, """//*[@id="GridQuick_gv"]/tbody/tr/td"""),'Sorry, no available slot(s) found. Please try again with another criteria.'))
    #         if not_available:
    #             driver.refresh()
    #             if school != "":
    #                 print(f"No bookings in {school}. Continuing to other schools...")            
    #     except:
    #         try:
    #             driver.find_element_by_css_selector("#GridQuick_gv_ctl02_checkMultiple").click()
                
    #             print("Room found! Making booking...")
        
    #             # Clicks make booking
    #             make_booking_element = wait.until(EC.element_to_be_clickable((By.ID,"btnMakeBooking")))
    #             make_booking_element.click()

    #             enter_booking_details()
    #         except:
    #             checklist = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#GridQuick_gv_ctl02_checkMultiple")))
    #             checklist.click()
    #             print("Room found! Making booking...")
        
    #             # Clicks make booking
    #             make_booking_element = wait.until(EC.element_to_be_clickable((By.ID,"btnMakeBooking")))
    #             make_booking_element.click()

    # else:
    #     checklist = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#GridQuick_gv_ctl02_checkMultiple")))
    #     checklist.click()
        
    #     print("Room found! Making booking...")
        
    #     # Clicks make booking
    #     make_booking_element = wait.until(EC.element_to_be_clickable((By.ID,"btnMakeBooking")))
    #     make_booking_element.click()
    try:
        driver.find_element_by_css_selector("#GridQuick_gv_ctl02_checkMultiple").click()
        
        print("Room found! Making booking...")

        # Clicks make booking
        make_booking_element = wait.until(EC.element_to_be_clickable((By.ID,"btnMakeBooking")))
        make_booking_element.click()

        enter_booking_details()

    except:
        if school != "":
            print(f"No bookings in {school}. Continuing to other schools...")            
        driver.refresh()
    


# In[14]:


def get_available_bookings():
    
    """
    Gets a list of available bookings. 
    
    Currently returns a list of the available bookings with the highest duration with the specified time frame.
    """

    overall_dict = {}
    # temp_list = []
    for school in school_list:

        # Gets a list of facilities from the respective schools
        abbrev = school_abbrev_list[school_list.index(school)]

        facility_file = abbrev + "_GSR.csv"
        facility_path = resource_path("./facilities/"+ facility_file)
        facility_list = pd.read_csv(facility_path, delimiter = ',', header = 0, usecols = [1]).values.tolist()


        # Removes nested list from file
        for i in range(len(facility_list)):
            facility_list[i] = facility_list[i][0]
    #     print(facility_list)
        # Processes booking per school
        bookings_list = booking_dict[school]

        # Counter for facility list
        count = 0

    #     print(f"The length is : {len(facility_list)}")
        for booking in bookings_list:
            if "23:59" in booking:
                count += 1
            elif "not available" not in booking:
                booking = booking.split("\n")
    #             pause = input("")
    #             print(f"Booking is {booking} facility is {facility_list[count]}")
                facility = facility_list[count]
                booking_time = booking[0][booking[0].find(":")+2:]
    #             print(temp_list)
                if facility not in overall_dict:
                    overall_dict[facility] = [booking_time]
                else:
                    overall_dict[facility].append(booking_time)
    return overall_dict
                    
def get_bookings_with_longest_duration(overall_dict):
    """
    Based on a list of overall bookings, return a list of facilities and their time period that are in the specified time.
    """
    
    available_dict = {}
    booking_time = details["start_time"] +"-"+ details["end_time"]
    
#     print(overall_dict)
    
    for facility in overall_dict.keys():
        
        # Gets a list of available timings for each GSR
        available_timings = _get_empty_timeslots(overall_dict[facility],details["date"])
    #     print(f"{facility}:{available}")
        
        # Converts into a dict in the format:
        # Duration : [{GSR:Timing}]
        # eg. 2 : {'GSR 2-20':'9-11:00','GSR 3-37':'10:00-12:00'}
        
        for timing in available_timings:
    #         print(booking_time,timing)
            if suitable_time(booking_time,timing) != False:
            # Checks if timing is suitable
                timing, duration = suitable_time(booking_time,timing)
                if duration not in available_dict:
                    available_dict[duration] = {}
                    available_dict[duration][facility] = timing
                else:
                    available_dict[duration][facility] = timing
                    
#     print(available_dict)
    longest_duration_period = sorted(available_dict.keys())[-1]   
    longest_duration_dict = available_dict[longest_duration_period]
    
    return longest_duration_dict,longest_duration_period

def choose_new_booking(longest_duration_dict,longest_duration_period):
    print(" ")
    print(f"The longest duration found is {longest_duration_period} hours.")
               
    count = 0
    for available_booking in longest_duration_dict.keys():
        print(f"{count} - Room: {available_booking} | Duration: {longest_duration_dict[available_booking]}")
        count += 1
    
#     print(longest_duration_dict)
    selected_booking_room_index = int(input("Enter the number beside the room you want to book instead."))
    
    while not(0 <= selected_booking_room_index < count):
        print("There is no such room. Please re-enter your selection.")
        print(" ")
        selected_booking_room_index = int(input("Re-enter the room you want to book instead. "))
    
    selected_booking_room = list(longest_duration_dict.keys())[selected_booking_room_index]
    selected_booking_time = longest_duration_dict[selected_booking_room]
    return [selected_booking_room,selected_booking_time]
        

# print(overall_dict)
   


# In[15]:


a = {'a':1,"b":2}
list(a.keys())[0]


# In[16]:


def _get_empty_timeslots(list_of_booked_timings, date):
    
    """
    list_of_booked_timings -> list of booked timings 
    day -> string, 'Monday', .,..

    given list of booked timings in the format ['11:30-14:30', '15:00-19:00']
    return all the timings where the GSR is available, in the same format
   

    """
    day = datetime.strptime((details["date"]), '%d-%b-%Y').strftime('%A')
    
    #weekday 8.30 to 10.30
    #weekend 8.30 to 5
    
    list_of_available_timings = []
    
    list_of_booked_timings.sort()
    
    for i in range(len(list_of_booked_timings)-1):
        time_range1 = list_of_booked_timings[i].split('-')
        start_time1 = int(time_range1[0].replace(':', ""))
        end_time1 = int(time_range1[1].replace(':',""))
        
        
        time_range2 = list_of_booked_timings[i+1].split('-')
        start_time2 = int(time_range2[0].replace(':', ""))
        end_time2 = int(time_range2[1].replace(':',""))
        
        if i == 0:
            check = start_time1 - 800
            if check > 0:
                first = '08:30' + '-' + time_range1[0]
                list_of_available_timings.append(first)
               
                
        if i == len(list_of_booked_timings)-2: 
            check = 2230 - end_time2
            if check > 0: 
                if day == 'Saturday' or day == 'Sunday':
                    last = time_range2[1] + '-' + '17:00'
                    list_of_available_timings.append(last)
                else:
                    last = time_range2[1] + '-' + '22:30'
                    list_of_available_timings.append(last)
        
        if start_time2 - end_time1  > 0:
            add =  time_range1[1] + '-' + time_range2[0]
            list_of_available_timings.append(add)
        
    list_of_available_timings.sort()
        
    return list_of_available_timings

def suitable_time(booking_time, available_time):
    """
    Checks if the booking time will fit into the available time
    
    Time should be input in the format hh:mm-hh:mm (24 hour)
    
    For example,
    
    For a booking time of 09:30-11:30:
    
    for the following available times:
    9:00-11:00 should return 09:30-11:00, 1.5 
    10:00-11:00 should return 10:00-11:00, 1
    10:00-12:00 should return 10:00-11:30, 1.5
    08:00-09:30 should return False
    12:00-13:00 should return False
    
    """
    
    # Splits booking time into start and end time
    
    booking_time_list = booking_time.split("-")
    booking_time_start = booking_time_list[0]
    booking_time_end = booking_time_list[1]    
    
    # Splits available time into start and end time
    
    available_time_list = available_time.split("-")
    available_time_start = available_time_list[0]
    available_time_end = available_time_list[1]
    
    if ((available_time_end <= booking_time_start and available_time_start <= booking_time_start) 
        or 
        (available_time_start >= booking_time_end and available_time_end >= booking_time_end)):
        
        # Returns false for available timings that are out of range
        return False
    
    elif available_time_start >= booking_time_start and available_time_end <= booking_time_end:
        
        # Returns the available timing as a whole if it is a subset of booking timing
        return available_time, get_half_hr_iterations(available_time) * 0.5
    
    else:
        
        result_time_start = max(available_time_start,booking_time_start)
        result_time_end = min(available_time_end,booking_time_end)
        result_time = result_time_start+"-"+result_time_end
        return result_time, get_half_hr_iterations(result_time) * 0.5
        
        
def get_half_hr_iterations(time_range):
    """
    Given string of booking time-range eg '1030-1200', return the number of 30minutes interval 
    between them eg ['0800-1030', '1200-1400','1630-2230']
    
    hold_start_and_end_timings -> list of start and end timings
    
    time_object_1 & time_object_2 -> converts the start and end timings to datetime.time objects
    whether the day is a weekday or not. 8am to 1030pm
    
    start_booking_time_mins & end_booking_time_mins -> Convert the booking timings into minutes for calculation
    of the number of 30 minutes interval. e.g. 240 minutes -> 4 hours -> 8 thirty minute intervals

    """
    hold_start_and_end_timings = time_range.split('-')
    time_object_1 = datetime.strptime(hold_start_and_end_timings[0],'%H:%M').time()
    time_object_2 = datetime.strptime(hold_start_and_end_timings[1],'%H:%M').time()
    h1, m1, s1 = time_object_1.hour, time_object_1.minute, time_object_1.second
    h2, m2, s2 = time_object_2.hour, time_object_2.minute, time_object_2.second
    
    start_booking_time_mins = (m1 + 60*h1) 
    end_booking_time_mins = (m2 + 60*h2)
    
    return int((end_booking_time_mins - start_booking_time_mins)/60/0.5)


# print(get_half_hr_iterations('08:30-12:30'))        

# print(suitable_time("09:30-11:30","09:00-11:00"))
# print(suitable_time("09:30-11:30","09:30-11:00"))
# print(suitable_time("09:30-11:30","10:00-11:00"))
# print(suitable_time("09:30-11:30","08:30-09:30"))
# print(suitable_time("09:30-11:30","11:30-12:00"))
# print(suitable_time("09:30-11:30","10:30-12:00"))

        


# In[17]:


def main():
       
    # Gets user details from text file in the same directory
    get_info_details()

    # Opens the chromedriver
    open_driver()
    
    # Logins to FBS
    login(info)

    # Initialises booking_dict
    global booking_dict
    booking_dict = {}   
    
    booking_type = int(input("Press 0 for GSR Booking \nPress 1 for Project Room Booking"))

    if booking_type == 0:
        # Checks every school if there are available slots and books if there is
        for school in school_list:
            if has_booked == False:
                print(" ")
                search_by_school(school)
                print(f"Checking for available rooms in {school}...")
                store_booking(school)        
                check_by_list(school)

                if has_booked == False:
                
                    # Lists schools checked for rooms so far
                
                    print("Schools checked so far: ")
                    current_index = school_list.index(school)
                    for i in range(current_index+1):
                        print(school_list[i])

                    print(" ")

                    # Lists schools left on the list that have yet to be tried
                    if current_index < len(school_list) - 1:
                        print("Schools left to try: ")
                        for i in range(current_index+1,len(school_list)):
                            print(school_list[i])
            else:
                break
        if has_booked == False:
            # Prints when there are no more schools left to find and there is no room booked.
            print("I'm sorry, but there are no available rooms for your specified requirements. :(")
            print("Please select another timeslot from the subsequent list of available timeslots.")
            print("Generating list of available timeslots...")
            
            # If there are no available bookings, process data and find new booking
            overall_dict = get_available_bookings()
            longest_duration_dict,longest_duration_period = get_bookings_with_longest_duration(overall_dict)
            new_booking = choose_new_booking(longest_duration_dict,longest_duration_period)
            
            print(f"You have choosed to book {new_booking[0]} at {new_booking[1]}")
            room = new_booking[0]
            new_time = new_booking[1]
            start_time = new_time.split("-")[0]
            end_time = new_time.split("-")[1]
            
            details['start_time'] = start_time
            details['end_time'] = end_time
            
            search_by_room(room)
            check_by_list()

    else:
        search_by_facility_type()
        check_by_list()


        
    # Happens when room is successfully booked.

    print("Your booking is complete!")
    print(f"Please remind {details['co_booker']} to accept the booking.")
    close = input("Press Enter once you have completed to close the browser.")
    driver.close()

    


# In[19]:


main()


from multiprocessing import Process
import yaml
from pathlib import Path
from cryptography.fernet import Fernet
from percy_objects import PercyObjects
import sys
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from percy import percy_snapshot
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException, ElementNotVisibleException
from mongo_key_encryption import decrypt_browserstack_password, get_mongo_collection, decrypt_user_password
from percy_branch_name import get_percy_branch_name
from percy_configs import get_desired_caps, get_snapshots_to_take

MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&directConnection=true'

class PercySupport:
    # ------------------------------------------------------------------------------------------------------------------
    # Name: __init__()
    # Purpose: Run Percy tests
    # Usage: Called by percy_run() in qa_app.py
    # Parameters: wd: the webdriver
    #             site_name: Class Copy or whichever site was chosen (ie. QA Auto Template)
    #             script_cases:=
    #
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # init the page locators
        self.percy_objects = PercyObjects()
        self.percy_token = ''
        
        
        self.snapshots_to_take = get_snapshots_to_take()
        
        # load unique tester values
        configs_path = Path(os.path.dirname(os.path.abspath(__file__)) + "/" + 'tester_configs.yaml')
        with open(configs_path, 'r') as file:
            tester_configs = yaml.load(file, Loader=yaml.FullLoader)
            # Ask for the name and add the date for context
            percy_branch = get_percy_branch_name()

        # browserstack username & password
        browserstack_username = tester_configs['browserstack_username']
        browserstack_pw = decrypt_browserstack_password(browserstack_username, is_percy=False)

        # Init Percy
        percy_token = os.environ.get('PERCY_TOKEN')
        if percy_token is None:
            percy_token = decrypt_browserstack_password(browserstack_username, is_percy=True)

        os.environ['PERCY_TOKEN'] = percy_token  # initialize the percy_files token
        os.environ['PERCY_BRANCH'] = percy_branch  # initialize the percy_files token


        # prepare the child process
        self.child_process = Process(target=child_process)

        # for capturing screenshots of potential selenium problems
        self.directory_path = os.getcwd()

        # init the web driver
        self.driver = webdriver.Remote(
            command_executor='http://' + browserstack_username + ':' + browserstack_pw + '@hub.browserstack.com:80/wd/hub',
            desired_capabilities = get_desired_caps())

        # 30 second wait variable
        print('Waiting for elements to load... 30sec timeout')
        self.wait = WebDriverWait(self.driver, 30)

        # open hostname url
        self.driver.get(tester_configs['percy_url'])
        self.driver.maximize_window()

    ####################################################################################################################
    # wait_for_element()
    # Wait for an element on the page to load
    ####################################################################################################################
    def wait_for_element(self, locator):
        try:
            self.wait.until(ec.visibility_of_element_located((locator[0], locator[1])))
            sleep(2)
        except TimeoutException:
            print('TimeoutException: ', locator[0] + " - " + locator[1])
            self.driver.save_screenshot(self.directory_path + '/wait_for_element_key.png')
            self.end_test()

    ####################################################################################################################
    # wait_for_invisibility()
    # Wait for an element on the page to go away
    ####################################################################################################################
    def wait_for_invisibility(self, locator):
        try:
            self.wait.until(ec.invisibility_of_element_located((locator[0], locator[1])))
            sleep(2)
        except TimeoutException:
            print('TimeoutException: ', locator[0] + " - " + locator[1])
            self.driver.save_screenshot(self.directory_path + '/wait_for_invisibility_key.png')
            self.end_test()

    ####################################################################################################################
    # is_element_displayed()
    #  wait for the element to appear on the page
    ####################################################################################################################
    def is_element_displayed(self, locator):
        print('is_element_displayed: ', locator[0] + " - " + locator[1])
        try:
            element = self.wait.until(ec.visibility_of_element_located((locator[0], locator[1])))
            return element.is_displayed()
        except TimeoutException:
            return False

    ########################################################################################################################
    # click_element()
    # click an element
    ########################################################################################################################
    def click_element(self, locator):
        try:
            element = self.driver.find_element(locator[0], locator[1])
        except NoSuchElementException:
            print('NoSuchElementException: ', locator[0] + " - " + locator[1])
            self.driver.save_screenshot(self.directory_path + '/click_element_key.png')
            self.end_test()
            return
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException):
            print('Click Exception: ', locator[0] + " - " + locator[1])
            self.driver.save_screenshot(self.directory_path + '/click_element_key.png')
            self.end_test()

    ########################################################################################################################
    # input_text()
    # input text into a text field
    ########################################################################################################################
    def input_text(self, by, value, text):
        try:
            element = self.driver.find_element(by, value)
        except NoSuchElementException:
            print('NoSuchElementException: ', value)
            self.driver.save_screenshot(self.directory_path + '/input_text_key.png')
            self.end_test()
            return
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
            if text:
                element.send_keys(text)
        except (ElementClickInterceptedException, ElementNotInteractableException):
            print('Input Text Exception: ', value)
            self.driver.save_screenshot(self.directory_path + '/input_text_key.png')
            self.end_test()

    ####################################################################################################################
    # Login Page
    ####################################################################################################################
    def login_page(self):
        print('self.percy_objects.cookie_banner_btn: ', self.percy_objects.cookie_banner_btn)
        self.wait_for_element(self.percy_objects.cookie_banner_btn)

        # percy snapshot
        if self.snapshots_to_take['Login Page']:
            percy_snapshot(self.driver, 'Login Page')

        # Accept Cookies
        self.click_element(self.percy_objects.cookie_banner_btn)

        # Open Forgot Password View
        self.click_element(self.percy_objects.forgot_pw_btn)
        self.wait_for_element(self.percy_objects.pw_reset_cancel_btn)
        if self.snapshots_to_take['Forgot PW']:
            percy_snapshot(self.driver, 'Forgot PW')

        # Return to Login Page
        self.click_element(self.percy_objects.pw_reset_cancel_btn)
        self.wait_for_element(self.percy_objects.username_input)

        # input username
        self.input_text('id', 'username', 'percy_user0001')

        # input password
        mongo_account_info_collection = get_mongo_collection('automationDB', 'accountInfo')

        # mongo_db = mongo_client.automationDB
        # mongo_account_info_collection = mongo_db.accountInfo

        account_info_doc = mongo_account_info_collection.find_one({'account_info': 'normal'})
        encrypted_password = account_info_doc['password1']
        decrypted_pw = decrypt_user_password(encrypted_password)
        self.input_text('id', 'password', decrypted_pw)

        # login
        self.click_element(self.percy_objects.signin_btn)

    ####################################################################################################################
    # Splash Page
    ####################################################################################################################
    def splash_page(self):
        # self.wait_for_element('id', 'account-menu-trigger')
        self.wait_for_element(self.percy_objects.account_menu_user_image)
        if self.snapshots_to_take['Splash Page']:
            percy_snapshot(self.driver, 'Splash Page')

        # start the class
        self.click_element(self.percy_objects.qa_auto_start_class_btn)


    ####################################################################################################################
    # navigate_to_page
    ####################################################################################################################
    def navigate_to_page(self, click_element, page_objects):
        print('NAVIGATE TO PAGE: ', click_element[0] + " - " + click_element[1])
        if not self.is_navbar_open():
            self.open_navbar()

        self.click_element(click_element)
        self.wait_for_element(page_objects)

        if self.is_navbar_open():
            self.close_navbar()


    ####################################################################################################################
    # NAVBAR STATE
    ####################################################################################################################
    def is_navbar_open(self):
        button = self.driver.find_element(By.CSS_SELECTOR, "button[data-agile-lh='navigationToggleBtn']")
        return button.get_attribute("aria-expanded") == "true"

    def open_navbar(self):
        self.click_element(self.percy_objects.nav_open_menu_btn)
        self.wait_for_element(self.percy_objects.nav_points_progress_circle)


    def close_navbar(self):
        self.click_element(self.percy_objects.nav_close_menu_btn)
        self.wait_for_element(self.percy_objects.nav_open_menu_btn)

    ####################################################################################################################
    # TAKE PAGE SNAPSHOT
    ####################################################################################################################
    def take_page_snapshot(self, page_name):
        if self.snapshots_to_take[page_name]:
            print('taking snapshot: ', page_name)
            percy_snapshot(self.driver, page_name)
    

    #################################################################################################################### 
    # NAVBAR PAGE
    ####################################################################################################################
    def navbar_page(self):
        # check navbar state
        print('checking navbar state it is open')
        # Find the button element
        navbar_is_open = self.is_navbar_open()

        # open navbar if it's closed
        print('opening navbar if it is closed')
        if not navbar_is_open:
            self.click_element(self.percy_objects.nav_open_menu_btn)
            self.wait_for_element(self.percy_objects.nav_points_progress_circle)

        # wait for navbar image to load
        self.wait_for_element(self.percy_objects.nav_close_menu_btn)

        # take snapshot
        self.take_page_snapshot('Nav Menu')

    ####################################################################################################################
    # Home Page
    ####################################################################################################################
    def home_page(self):
        # check navbar state
        navbar_is_open = self.is_navbar_open()

        # close navbar if it's open
        if navbar_is_open:
            self.click_element(self.percy_objects.nav_close_menu_btn)
            self.wait_for_element(self.percy_objects.nav_open_menu_btn)

        self.take_page_snapshot('Home Page')

    ####################################################################################################################
    # FAQ Page
    ####################################################################################################################
    def faq_page(self):
        self.navigate_to_page(
            self.percy_objects.nav_faq_launch, 
            self.percy_objects.faq_page_description
        )
        self.take_page_snapshot('FAQ Page')

    ####################################################################################################################
    # Contact Page
    ####################################################################################################################
    def contact_page(self):
        self.navigate_to_page(
            self.percy_objects.nav_contact_launch,
            self.percy_objects.contact3_image
        )
        self.take_page_snapshot('Contact Page')

    ####################################################################################################################
    # Learning Path Page
    ####################################################################################################################
    def learning_path_page(self):

        self.click_element(self.percy_objects.nav_learning_paths_launch)
        self.wait_for_element(self.percy_objects.learning_path_accordion)
        self.click_element(self.percy_objects.learning_path_accordion)
        self.wait_for_element(self.percy_objects.large_learning_path)
        if self.snapshots_to_take['Learning Path Page']:
            percy_snapshot(self.driver, 'Learning Path Page')
        if self.snapshots_to_take['Learning Path Modal']:
            self.click_element(self.percy_objects.large_learning_path)
            self.wait_for_element(self.percy_objects.close_modal_btn)
            percy_snapshot(self.driver, 'Learning Path Modal')
            self.click_element(self.percy_objects.close_modal_btn)
            self.wait_for_invisibility(self.percy_objects.close_modal_btn)
            
    ####################################################################################################################
    # Mission Page
    ####################################################################################################################
    def mission_page(self):
        self.navigate_to_page(
            self.percy_objects.nav_missions_launch,
            self.percy_objects.mission_accordion
        )
        self.click_element(self.percy_objects.mission_accordion)
        self.wait_for_element(self.percy_objects.mission_tile)
        
        self.take_page_snapshot('Mission Page')
        
    ####################################################################################################################
    # Multicategory Page
    ####################################################################################################################
    def multicat_page(self):
        self.click_element(self.percy_objects.nav_multicat_launch)
        self.wait_for_element(self.percy_objects.mission_open_btn)
        # open accordion & scroll down
        self.click_element(self.percy_objects.content_accordion)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.wait_for_element(self.percy_objects.audio_open_btn)
        if self.snapshots_to_take['Multicat Page']:
            percy_snapshot(self.driver, 'Multicat Page')

    ####################################################################################################################
    # MISSION MODAL
    ####################################################################################################################
    def mission_modal(self):
        # open mission - SHARE STEP
        self.click_element(self.percy_objects.mission_open_btn)
        self.wait_for_element(self.percy_objects.close_modal_btn)
        sleep(0.5)  # time for content animation
        if self.snapshots_to_take['Mission Share Step']:
            percy_snapshot(self.driver, 'Mission Share Step')

        # FILE UPLOAD STEP (7)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_attachments_limit)
        sleep(0.5)  # time for content animation
        if self.snapshots_to_take['Mission File Upload Step']:
            percy_snapshot(self.driver, 'Mission File Upload Step')

        # MOV VIDEO UPLOAD STEP (6)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_video_requirements)
        sleep(0.5)  # time for content animation
        if self.snapshots_to_take['Mission MOV Upload Step']:
            percy_snapshot(self.driver, 'Mission MOV Upload Step')

        # MP4 VIDEO UPLOAD STEP (5)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_video_requirements)
        sleep(1)  # time for content animation
        if self.snapshots_to_take['Mission MP4 Upload Step']:
            percy_snapshot(self.driver, 'Mission MP4 Upload Step')

        # IMAGE UPLOAD STEP (4)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_img_limit)
        sleep(0.5)  # time for content animatio
        if self.snapshots_to_take['Mission Image Step']:
            percy_snapshot(self.driver, 'Mission Image Step')

        # TEXT LIST INPUT STEP (3)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_text_list_input1)
        sleep(0.5)  # time for content animation
        if self.snapshots_to_take['Text List Step']:
            percy_snapshot(self.driver, 'Text List Step')

        # TEXT FIELD INPUT STEP (2)
        self.click_element(self.percy_objects.mission_back_btn)
        self.wait_for_element(self.percy_objects.mission_step_text_input)
        sleep(0.5)  # time for content animation
        if self.snapshots_to_take['Text Field Step']:
            percy_snapshot(self.driver, 'Text Field Step')

        # MESSAGE PROMPT STEP (1)
        self.click_element(self.percy_objects.mission_back_btn)
        sleep(5)  # time for content animation
        if self.snapshots_to_take['Message Prompt Step']:
            percy_snapshot(self.driver, 'Message Prompt Step')

        # Close Mission
        self.click_element(self.percy_objects.close_modal_btn)
        sleep(0.5)  # waits take a minimum of 0.5 seconds anyways

    ####################################################################################################################
    # PROJECT MODAL
    ####################################################################################################################
    def project_modal(self):
        # open project to intro
        self.click_element(self.percy_objects.project_open_btn)
        self.wait_for_element(self.percy_objects.project_start_btn)
        sleep(5)  # make sure field report area loads
        if self.snapshots_to_take['Project Intro']:
            percy_snapshot(self.driver, 'Project Intro')
        # start project
        self.click_element(self.percy_objects.project_start_btn)
        self.wait_for_element(self.percy_objects.project_codemirror_wrapper)
        if self.snapshots_to_take['Project Modal']:
            percy_snapshot(self.driver, 'Project Modal')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # CUSTOM CONTENT
    ####################################################################################################################
    def custom_content_modal(self):
        # open custom content
        self.click_element(self.percy_objects.custom_content_open_btn)
        # self.wait_for_element(self.custom_content_abstract_image)
        self.wait_for_element(self.percy_objects.custom_content_abstract_image)
        if self.snapshots_to_take['Custom Content']:
            percy_snapshot(self.driver, 'Custom Content')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # MULTICAT PAGE PART 2
    ####################################################################################################################
    def multicat_page_part2(self):
        # open custom content
        self.click_element(self.percy_objects.content_accordion)
        # scroll down
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.wait_for_element(self.percy_objects.audio_open_btn)
        if self.snapshots_to_take['Multicat2']:
            percy_snapshot(self.driver, 'Multicat2')

    ####################################################################################################################
    # AUDIO
    ####################################################################################################################
    def audio_modal(self):
        # open audio
        self.click_element(self.percy_objects.audio_open_btn)
        self.wait_for_element(self.percy_objects.close_modal_btn)
        sleep(0.5)  # some items haven't loaded on page (icons mainly)
        if self.snapshots_to_take['Audio']:
            percy_snapshot(self.driver, 'Audio')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # CONTEXT
    ####################################################################################################################
    def context_modal(self):
        # open custom content
        self.click_element(self.percy_objects.context_open_btn)
        self.wait_for_element(self.percy_objects.close_modal_btn)
        if self.snapshots_to_take['Context']:
            percy_snapshot(self.driver, 'Context')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # DOCUMENT
    ####################################################################################################################
    def document_modal(self):
        # open custom content
        self.click_element(self.percy_objects.document_open_btn)
        self.wait_for_element(self.percy_objects.close_modal_btn)
        if self.snapshots_to_take['Document']:
            percy_snapshot(self.driver, 'Document')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # EXTERNAL LINK
    ####################################################################################################################
    def external_link_modal(self):
        # open external link
        self.click_element(self.percy_objects.external_link_open_btn)
        self.wait_for_element(self.percy_objects.close_modal_btn)
        if self.snapshots_to_take['External Link']:
            percy_snapshot(self.driver, 'External Link')

        # Close Custom Content
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # QUIZ - todo - incomplete?
    ####################################################################################################################
    def quiz_modal(self):
        self.click_element(self.percy_objects.multicat_tab3)
        self.wait_for_element(self.percy_objects.quiz_open_btn)

        # open quiz
        self.click_element(self.percy_objects.quiz_open_btn)
        self.wait_for_element(self.percy_objects.start_quiz_btn)
        if self.snapshots_to_take['Quiz Intro']:
            percy_snapshot(self.driver, 'Quiz Intro')

        # step 1
        self.click_element(self.percy_objects.start_quiz_btn)
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_answer1)
        # if self.snapshots_to_take['Quiz Step 1']:
        #   percy_snapshot(self.driver, 'Quiz Step 1')
        self.click_element(self.percy_objects.quiz_question_multichoice_answer1)
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_feedback)
        if self.snapshots_to_take['Quiz Step 1 Answered']:
            percy_snapshot(self.driver, 'Quiz Step 1 Answered')
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 2
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_answer2)
        # if self.snapshots_to_take['Quiz Step 2']:
        #   percy_snapshot(self.driver, 'Quiz Step 2')
        self.click_element(self.percy_objects.quiz_question_multichoice_answer2)
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_feedback)
        if self.snapshots_to_take['Quiz Step 2 Answered']:
            percy_snapshot(self.driver, 'Quiz Step 2 Answered')
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 3
        self.wait_for_element(self.percy_objects.quiz_step3_correct_answer)
        # if self.snapshots_to_take['Quiz Step 3']:
        # percy_snapshot(self.driver, 'Quiz Step 3')
        self.click_element(self.percy_objects.quiz_step3_correct_answer)
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_feedback)
        if self.snapshots_to_take['Quiz Step 3 Answered']:
            percy_snapshot(self.driver, 'Quiz Step 3 Answered')
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 4
        self.wait_for_element(self.percy_objects.quiz_question_binary_left_btn)
        # if self.snapshots_to_take['Quiz Step 4']:
        # percy_snapshot(self.driver, 'Quiz Step 4')
        self.click_element(self.percy_objects.quiz_question_binary_left_btn)
        self.wait_for_element(self.percy_objects.quiz_question_binary_okay_btn)
        if self.snapshots_to_take['Quiz Step 4 Answered A']:
            percy_snapshot(self.driver, 'Quiz Step 4 Answered A')
        self.click_element(self.percy_objects.quiz_question_binary_okay_btn)
        self.wait_for_invisibility(self.percy_objects.quiz_question_binary_okay_btn)
        self.click_element(self.percy_objects.quiz_question_binary_left_btn)
        self.wait_for_element(self.percy_objects.quiz_question_binary_okay_btn)
        if self.snapshots_to_take['Quiz Step 4 Answered B']:
            percy_snapshot(self.driver, 'Quiz Step 4 Answered B')
        self.click_element(self.percy_objects.quiz_question_binary_okay_btn)
        self.wait_for_invisibility(self.percy_objects.quiz_question_binary_okay_btn)
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 5
        self.wait_for_element(self.percy_objects.quiz_question_binary_left_btn)
        # if self.snapshots_to_take['Quiz Step 4 A']:
        # percy_snapshot(self.driver, 'Quiz Step 4 A')
        self.click_element(self.percy_objects.quiz_question_binary_left_btn)
        self.wait_for_element(self.percy_objects.quiz_question_binary_okay_btn)
        if self.snapshots_to_take['Quiz Step 5 Answered A']:
            percy_snapshot(self.driver, 'Quiz Step 5 Answered A')
        self.click_element(self.percy_objects.quiz_question_binary_okay_btn)
        self.wait_for_invisibility(self.percy_objects.quiz_question_binary_okay_btn)
        self.click_element(self.percy_objects.quiz_question_binary_right_btn)
        self.wait_for_element(self.percy_objects.quiz_question_binary_okay_btn)
        if self.snapshots_to_take['Quiz Step 5 Answered B']:
            percy_snapshot(self.driver, 'Quiz Step 5 Answered B')
        self.click_element(self.percy_objects.quiz_question_binary_okay_btn)

        # step 6
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_answer1)
        self.click_element(self.percy_objects.quiz_question_multichoice_answer1)
        self.click_element(self.percy_objects.quiz_question_multichoice_answer2)
        self.click_element(self.percy_objects.quiz_next_btn)
        self.wait_for_element(self.percy_objects.quiz_question_multichoice_feedback)
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 7
        self.wait_for_element(self.percy_objects.quiz_step7_img)
        if self.snapshots_to_take['Quiz Step 6']:
            percy_snapshot(self.driver, 'Quiz Step 6')
        self.click_element(self.percy_objects.quiz_next_btn)

        # step 8
        self.wait_for_element(self.percy_objects.quiz_finish_btn)
        if self.snapshots_to_take['Quiz Step 7']:
            percy_snapshot(self.driver, 'Quiz Step 7')
        self.click_element(self.percy_objects.quiz_finish_btn)

        # step finish
        self.wait_for_element(self.percy_objects.quiz_summary_text)
        if self.snapshots_to_take['Quiz Complete']:
            percy_snapshot(self.driver, 'Quiz Complete')

        # close quiz
        self.click_element(self.percy_objects.close_modal_btn)
        self.wait_for_invisibility(self.percy_objects.close_modal_btn)

    ####################################################################################################################
    # Account Menu
    ####################################################################################################################
    def account_menu(self):
        # open my profile
        self.click_element(self.percy_objects.account_menu_drop_down)
        self.wait_for_element(self.percy_objects.account_menu_my_profile)
        if self.snapshots_to_take['Account Menu']:
            percy_snapshot(self.driver, 'Account Menu')
        self.click_element(self.percy_objects.account_menu_drop_down)
        self.wait_for_invisibility(self.percy_objects.account_menu_my_profile)

    ####################################################################################################################
    # User Profile
    ####################################################################################################################
    def user_profile(self):
        # open my profile
        self.click_element(self.percy_objects.account_menu_drop_down)
        self.wait_for_element(self.percy_objects.account_menu_my_profile)
        self.click_element(self.percy_objects.account_menu_my_profile)
        self.wait_for_element(self.percy_objects.my_profile_user_image)
        if self.snapshots_to_take['My Profile']:
            percy_snapshot(self.driver, 'My Profile')

    ####################################################################################################################
    # Account Settings
    ####################################################################################################################
    def account_settings(self):
        # open account settings
        self.click_element(self.percy_objects.account_menu_drop_down)
        self.wait_for_element(self.percy_objects.account_menu_account_settings)
        self.click_element(self.percy_objects.account_menu_account_settings)
        self.wait_for_element(self.percy_objects.account_settings_email_input)
        if self.snapshots_to_take['Account Settings']:
            percy_snapshot(self.driver, 'Account Settings')

    ####################################################################################################################
    # Announcements
    ####################################################################################################################
    def announcements(self):
        # open announcements
        self.click_element(self.percy_objects.announcements_btn)
        self.wait_for_element(self.percy_objects.announcement_video1)
        if self.snapshots_to_take['Announcements']:
            percy_snapshot(self.driver, 'Announcements')
        self.click_element(self.percy_objects.announcements_btn)
        self.wait_for_invisibility(self.percy_objects.announcement_video1)

    ####################################################################################################################
    # Search Page
    ####################################################################################################################
    def search_page(self):
        # open announcements
        self.click_element(self.percy_objects.search_menu_btn)
        self.wait_for_element(self.percy_objects.search_menu_input)
        self.input_text(self.percy_objects.search_menu_input[0], self.percy_objects.search_menu_input[1], "IntrepidLorem")
        self.click_element(self.percy_objects.search_menu_all_results_btn)
        self.wait_for_element(self.percy_objects.search_page_class_content_btn)
        if self.snapshots_to_take['Search All Results']:
            percy_snapshot(self.driver, 'Search All Results')
        self.click_element(self.percy_objects.search_page_class_content_btn)
        self.wait_for_element(self.percy_objects.search_page_document_tile)
        if self.snapshots_to_take['Search Class Content']:
            percy_snapshot(self.driver, 'Search Class Content')
        self.click_element(self.percy_objects.search_page_community_content_btn)
        self.wait_for_invisibility(self.percy_objects.search_page_document_tile)
        self.wait_for_element(self.percy_objects.search_page_field_report)
        if self.snapshots_to_take['Search Community Content']:
            percy_snapshot(self.driver, 'Search Community Content')
        self.click_element(self.percy_objects.search_page_people_btn)
        self.wait_for_invisibility(self.percy_objects.search_page_field_report)
        self.wait_for_element(self.percy_objects.search_page_user_card)
        if self.snapshots_to_take['Search People']:
            percy_snapshot(self.driver, 'Search People')

    ####################################################################################################################
    # GWS Page
    ####################################################################################################################
    def group_workspace_page(self):
        self.click_element(self.percy_objects.gws_header_btn)
        self.wait_for_element(self.percy_objects.gws_project1_title)
        self.click_element(self.percy_objects.gws_project1_title)
        self.wait_for_element(self.percy_objects.gws_project1_intro_title)
        self.click_element(self.percy_objects.gws_project1_intro_title)
        self.wait_for_element(self.percy_objects.gws_project1_intro_img)
        if self.snapshots_to_take['GWS Page']:
            percy_snapshot(self.driver, 'GWS Page')

    ####################################################################################################################
    # Timeline Page
    ####################################################################################################################
    def timeline(self):
        self.click_element(self.percy_objects.nav_timeline_launch)
        self.wait_for_element(self.percy_objects.timeline_context_tile)
        if self.snapshots_to_take['Timeline Page']:
            percy_snapshot(self.driver, 'Timeline Page')

    ####################################################################################################################
    # Leaderboard Page
    ####################################################################################################################
    def leaderboard(self):
        self.click_element(self.percy_objects.nav_leaderboard_launch)
        self.wait_for_element(self.percy_objects.leaderboard_div)
        if self.snapshots_to_take['Leaderboard Page']:
            percy_snapshot(self.driver, 'Leaderboard Page')

    ####################################################################################################################
    # Content Page 1
    ####################################################################################################################
    def content_page1(self):
        self.click_element(self.percy_objects.nav_chinese_page_launch)
        self.wait_for_element(self.percy_objects.page_title)
        if self.snapshots_to_take['Content Page 1']:
            percy_snapshot(self.driver, 'Content Page 1')

    ####################################################################################################################
    # Content Page 2
    ####################################################################################################################
    def content_page2(self):
        
        self.navigate_to_page(self.percy_objects.nav_new_page_launch, self.percy_objects.page_title, 'Content Page 2')

    ####################################################################################################################
    # 404 Not Found Page
    ####################################################################################################################
    def not_found_404_page(self):
        self.driver.get("https://qa.s.intrepidagile.com/not_found404")
        self.wait_for_element(self.percy_objects.not_found_page_label)
        if self.snapshots_to_take['404 Not Found Page']:
            percy_snapshot(self.driver, '404 Not Found Page')

    ####################################################################################################################
    # End Test
    ####################################################################################################################
    def end_test(self):
        self.child_process.kill()
        self.child_process.join()
        self.driver.quit()
        print('Percy test ended')
        os.system('npx percy exec:stop')
        sys.exit()




def child_process():
    print('child_process')
    os.system("npx percy exec -- python3")
    print("does this print?")

import os
import sys
from time import sleep
from percy_support import PercySupport


def run_percy():
    print('run_percy')
    percy_support = PercySupport()

    percy_support.child_process.start()

    sleep(5)  # give percy time to boot up

    # run percy tests
    # Login Page
    percy_support.login_page()
    # Splash Page
    percy_support.splash_page()
     # Nav Menu
    percy_support.navbar_page()
    # Home Page
    percy_support.home_page()
   
    # # FAQ
    # if percy_support.snapshots_to_take['FAQ Page']:
    #     percy_support.faq_page()
    # # Contact Page
    # if percy_support.snapshots_to_take['Contact Page']:
    #     percy_support.contact_page()
    # if percy_support.snapshots_to_take['Learning Path Page'] or \
    #    percy_support.snapshots_to_take['Learning Path Modal']:
    #     percy_support.learning_path_page()
    # if percy_support.snapshots_to_take['Mission Page']:
    #     percy_support.mission_page()
    # # Multicat Page
    # percy_support.multicat_page()
    # # Mission Modal
    # if percy_support.snapshots_to_take['Mission Share Step'] or \
    #    percy_support.snapshots_to_take['Mission File Upload Step'] or \
    #    percy_support.snapshots_to_take['Mission MOV Upload Step'] or \
    #    percy_support.snapshots_to_take['Mission MP4 Upload Step'] or \
    #    percy_support.snapshots_to_take['Mission Image Step'] or \
    #    percy_support.snapshots_to_take['Text List Step'] or \
    #    percy_support.snapshots_to_take['Text Field Step'] or \
    #    percy_support.snapshots_to_take['Message Prompt Step']:
    #     percy_support.mission_modal()
    # # Project Modal
    # if percy_support.snapshots_to_take['Project Intro'] or \
    #    percy_support.snapshots_to_take['Project Modal']:
    #     percy_support.project_modal()
    # # Custom Content
    # if percy_support.snapshots_to_take['Custom Content']:
    #     percy_support.custom_content_modal()
    # # Multicat Page Open Accordion
    # # percy_support.multicat_page_part2()
    # # Audio Modal
    # if percy_support.snapshots_to_take['Audio']:
    #     percy_support.audio_modal()
    # # Context Modal
    # if percy_support.snapshots_to_take['Context']:
    #     percy_support.context_modal()
    # if percy_support.snapshots_to_take['Document']:
    #     percy_support.document_modal()
    # if percy_support.snapshots_to_take['External Link']:
    #     percy_support.external_link_modal()
    # if percy_support.snapshots_to_take['Quiz Intro'] or \
    #    percy_support.snapshots_to_take['Quiz Step 1 Answered'] or \
    #    percy_support.snapshots_to_take['Quiz Step 2 Answered'] or \
    #    percy_support.snapshots_to_take['Quiz Step 3 Answered'] or \
    #    percy_support.snapshots_to_take['Quiz Step 4 Answered A'] or \
    #    percy_support.snapshots_to_take['Quiz Step 4 Answered B'] or \
    #    percy_support.snapshots_to_take['Quiz Step 5 Answered A'] or \
    #    percy_support.snapshots_to_take['Quiz Step 5 Answered B'] or \
    #    percy_support.snapshots_to_take['Quiz Step 6'] or \
    #    percy_support.snapshots_to_take['Quiz Step 7'] or \
    #    percy_support.snapshots_to_take['Quiz Complete']:
    #     percy_support.quiz_modal()
    # # percy_support.checklist_modal()
    # if percy_support.snapshots_to_take['Account Menu']:
    #     percy_support.account_menu()
    # if percy_support.snapshots_to_take['My Profile']:
    #     percy_support.user_profile()
    # if percy_support.snapshots_to_take['Account Settings']:
    #     percy_support.account_settings()
    # if percy_support.snapshots_to_take['Announcements']:
    #     percy_support.announcements()
    # if percy_support.snapshots_to_take['Search All Results'] or \
    #    percy_support.snapshots_to_take['Search Class Content'] or \
    #    percy_support.snapshots_to_take['Search Community Content'] or \
    #    percy_support.snapshots_to_take['Search People']:
    #     percy_support.search_page()
    # if percy_support.snapshots_to_take['GWS Page']:
    #     percy_support.group_workspace_page()
    # if percy_support.snapshots_to_take['Timeline Page']:
    #     percy_support.timeline()
    # if percy_support.snapshots_to_take['Leaderboard Page']:
    #     percy_support.leaderboard()
    # if percy_support.snapshots_to_take['Content Page 1']:
    #     percy_support.content_page1()
    # if percy_support.snapshots_to_take['Content Page 2']:
    #     percy_support.content_page2()
    # if percy_support.snapshots_to_take['404 Not Found Page']:
    #     percy_support.not_found_404_page()

    # kill child process & stop percy
    percy_support.child_process.kill()
    percy_support.child_process.join()
    os.system('npx percy exec:stop')
    percy_support.driver.quit()
    sys.exit()


if __name__ == "__main__":
    run_percy()



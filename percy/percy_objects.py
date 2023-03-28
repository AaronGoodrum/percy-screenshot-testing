class PercyObjects:
    def __init__(self):
        ################################################################################################################
        # LOCATORS
        ################################################################################################################
        # login page
        self.username_input = ['id', 'username']
        self.forgot_pw_btn = ['id', 'forgotpwd-btn']
        self.pw_reset_cancel_btn = ['id', 'password-reset-cancel']
        self.cookie_banner_btn = ['css selector', 'button[class*="cookie-banner-button"]']
        self.signin_btn = ['id', 'signin-btn']

        # splash page & nav menu (language specific locators
        self.qa_auto_start_class_btn = ['css selector', 'div[class*="course-enrollment"] a[href="/class/qa-automation/"]']
        self.qa_auto2_start_class_btn = ['css selector', 'div[class*="course-enrollment"] a[href="/class/qa-automation2/"]']

        # header bar
        self.announcements_btn = ['css selector', 'button[title="Announcements"]']
        self.announcement_video1 = ['id', 'content_c8746bb7-a40d-4578-a806-a081b9050aa3']
        self.account_menu_user_image = ['css selector', 'button[id="account-menu-trigger"] div[class="user-image"] div[class*="img-circle"]']
        self.account_menu_drop_down = ['id', 'account-menu-trigger']
        self.account_menu_my_profile = ['css selector', 'div[class*="open"] li>a[href*="/learnerProfile"]']
        self.account_menu_account_settings = ['css selector', 'div[class*="open"] a[href*="account-settings"]']
        self.search_menu_btn = ['id', 'search-btn']
        self.search_menu_input = ['id', 'search-query']
        self.search_menu_all_results_btn = ['css selector', 'a[href*="/content/search/all"]']
        self.gws_header_btn = ['id', 'header-workGroups']
        
        # navbar
        self.nav_open_menu_btn = ['css selector', 'div[class="navigation-controls"]>button[aria-expanded="false"]']
        self.nav_close_menu_btn = ['css selector', 'div[class="navigation-controls"]>button[aria-expanded="true"]']
        self.nav_button_toggle = ['css selector', 'button[data-agile-lh="navigationToggleBtn"]']
        
        #navbar links
        self.nav_points_progress_circle = ['css selector', 'nav[class*="pinned"] div[class="navigation-progress__indicator"]:nth-child(1) svg[class="progress-circle"]']
        self.nav_faq_launch = ['css selector', 'a[href*="/faq"]']
        self.nav_contact_launch = ['css selector', 'a[href*="/contact"]']
        self.nav_learning_paths_launch = ['css selector', 'li>a[href*="paths1"]']
        self.nav_missions_launch = ['css selector', 'li>a[href*="missions"]']
        self.nav_multicat_launch = ['css selector', 'ul[class="navigation-menu__items"]>li>a[href*="multicategory-panel-1"]']
        self.nav_timeline_launch = ['css selector', 'ul[class="navigation-menu__items"]>li>a[href*="timeline"]']
        self.nav_leaderboard_launch = ['css selector', 'ul[class="navigation-menu__items"]>li>a[href*="leaderboard"]']
        self.nav_chinese_page_launch = ['xpath', '//a//span[text()="中文面板"]']
        self.nav_new_page_launch = ['xpath', '//a//span[text()="QA-Cre8pg &過"]']

        # my profile
        self.my_profile_user_image = ['xpath', '//div[@class="personal"]//div[contains(@class, "avatar") and contains(@style, "toad_png")]']

        # account settings
        self.account_settings_email_input = ['id', 'email']

        # contact page
        self.contact3_image = ['xpath', '//img[contains(@src, "person3.png")]']

        # faq page
        self.faq_page_description = ['id', 'description']
        
        # search page
        self.search_page_class_content_btn = ['css selector', 'ul[role="menubar"]>li[class=""]>a[href*="/content/search?q="]']
        self.search_page_people_btn = ['css selector', 'ul[role="menubar"]>li[class=""]>a[href*="/content/search/people"]']
        self.search_page_community_content_btn = ['css selector', 'ul[role="menubar"]>li[class=""]>a[href*="/content/search/community?q="]']
        self.search_page_document_tile = ['css selector', 'div[data-id="content_7497a21e-b125-41eb-abc7-4993898f2279"] a']
        self.search_page_user_card = ['css selector', 'a[href*="users_4c43b337-5be6-43a5-a1b4-e765396cbe56"]>div[class="person-info"]>h4[class*="person-name"]']
        self.search_page_field_report = ['css selector', 'div[data-id="fieldReports_ff254533-c04e-4cac-b627-a4c1af14b2e6"] img[class="tile__author"]']

        # learning path page
        self.learning_path_accordion = ['xpath', '(//div[@class="accordion-toggle"]/span)[2]']
        self.large_learning_path = ['css selector', 'div[data-agile-lh="optionalQuestAccordion"] div[data-id="quests_92d8e5aa-8088-4d9c-a598-558b484cb7fd"] h3']

        # mission_page
        self.mission_accordion = ['css selector', 'a[data-agile-lh="optionalMissionToggle"]']
        self.mission_tile = ['xpath', '//h2[contains(text(), "QA Automation Mission1")]']

        # multicat page
        self.multicat_tab3 = ['css selector', 'div[class*="menubar"]>ul>li:nth-child(3)>a']
        self.mission_open_btn = ['css selector', 'div[data-id="missions_7de32692-a774-433b-96f0-6385bcba1869"] a']
        self.custom_content_open_btn = ['css selector', 'div[data-id="content_79bd7b54-61f7-449a-8c19-83cb07f28741"] a']
        self.audio_open_btn = ['css selector', 'div[data-id="content_36bb499f-36cf-4e86-9b03-906af72fe8a3"] a']
        self.document_open_btn = ['css selector', 'div[data-id="content_bbf6f23d-044c-4928-97f8-0382cf2a84e1"] a']
        self.external_link_open_btn = ['css selector', 'div[data-id="content_e49a9647-3f64-40a3-8ecf-3a6b1c0d66cd"] a']
        self.context_open_btn = ['css selector', 'div[data-id="content_0db6a9d4-36eb-4ad8-bbb4-0a696e44d524"] a']
        self.quiz_open_btn = ['css selector', 'div[data-id="assessments_02b20bb0-5441-44c0-8869-b53931d4dfe3"] a']
        self.content_accordion = ['css selector', 'div[id="accordion-list"] a:nth-of-type(1)']

        # content modal
        self.close_modal_btn = ['id', 'viewer-close']
        self.custom_content_abstract_image = ['css selector', 'div[class="editor-html"]']

        # quiz modal
        self.start_quiz_btn = ['css selector', 'button[class*="start-assessment"]']
        self.quiz_question_multichoice_answer1 = ['css selector', 'div[class*="question-answers"]>div:nth-child(1) span']
        self.quiz_question_multichoice_answer2 = ['css selector', 'div[class*="question-answers"]>div:nth-child(2) span']
        self.quiz_step3_correct_answer = ['css selector', 'div[class*="question-answers"]>div:nth-child(1) img']
        self.quiz_question_multichoice_feedback = ['css selector', 'div[class="question-answer-feedback"] div[class*="editor-html"]']
        self.quiz_question_binary_left_btn = ['id', 'btn-left']
        self.quiz_question_binary_right_btn = ['id', 'btn-right']
        self.quiz_question_binary_okay_btn = ['css selector', 'button[class*="js-next-statement"]']
        self.quiz_step7_img = ['xpath', '(//div[contains(@class, "question-info")])[1]/div[contains(@class, "question-body")]//img[contains(@class, "img-responsive")]']
        self.quiz_next_btn = ['xpath', '//div[contains(@class, "assessment-controls")]/button[contains(@class, "next-question") and not(@disabled="disabled")]']
        self.quiz_finish_btn = ['css selector', 'div[class*="assessment-controls"]>button']
        self.quiz_summary_text = ['xpath', '//div[contains(@class, "assessment-summary")]//div[contains(@class, "summary-text")]']

        # mission modal
        self.mission_back_btn = ['css selector', 'div[class*="mission-controls"] button[class*="pull-left"]']
        self.mission_step_attachments_limit = ['css selector', 'div[class*="attachment-control"] label']
        self.mission_step_video_requirements = ['css selector', 'p[class="attachment-requirements"]']
        self.mission_step_img_limit = ['css selector', 'div[class="action-body"]>label']
        self.mission_step_text_list_input1 = ['css selector', 'ul[class="action-input-list"]>li:nth-child(1)>textarea']
        self.mission_step_text_input = ['css selector', 'div[class="tox-edit-area"]>iframe']
        self.mission_step_prompt = ['css selector', 'header[class="action-header"]']

        # project
        self.project_open_btn = ['css selector', 'div[data-id="missions_e311f06e-97f5-499f-837b-4854b15d9f69"] a']
        self.project_start_btn = ['css selector', 'button[data-agile-action="start"]']
        self.project_codemirror_wrapper = ['xpath', '//div[contains(@class, "project-report-container")]//div[contains(@class,"CodeMirror-code") and @role="presentation"]']

        # gws page
        self.gws_project1_title = ['xpath', '//div[contains(@class, "accordion-heading") and contains(@class, "collapse")][1]']
        self.gws_project1_intro_title = ['css selector', 'div[data-target="#missions_2b3d4bf5-86ca-4343-b247-c5593c1eb512"]']
        self.gws_project1_intro_img = ['css selector', 'img[data-img-id="content_543f2a68-ff7b-4b4a-ba96-8023fcab855d"]']

        # timeline page
        self.timeline_context_tile = ['css selector', 'div[data-id="content_0db6a9d4-36eb-4ad8-bbb4-0a696e44d524"]']

        # leaderboard page
        self.leaderboard_div = ['id', "leaderboard"]

        # content page
        self.page_title = ['css selector', 'h1[data-agile-lh="contentHeaderTitle"]']

        # 404 not found page
        self.not_found_page_label = ['id', "not-found-container"]

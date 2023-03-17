
build_name = input('Enter the name of the CM build Number: ')
if not build_name:
    print('Default build name used "Basic Percy Test"')
    build_name = 'Basic Percy Test'
    exit()


def get_desired_caps():
    desired_cap = {'project': 'Intrepid Percy',
                   'build': build_name,
                   'os': 'Windows',
                   'os_version': '10',
                   'browser': 'Chrome',
                   'browser_version': 'latest',
                   'browserstack.use_w3c': 'true',
                   }
    return desired_cap

def get_snapshots_to_take():
    snapshots_to_take = {
        'Login Page': True,
        'Forgot PW': True,
        'Splash Page': True,
        'Home Page': True,
        'FAQ Page': True,
        'Contact Page': True,
        'Mission Page': True,
        'Learning Path Page': True,
        'Learning Path Modal': True,
        'Multicat Page': True,
        'Mission Share Step': True,
        'Mission File Upload Step': True,
        'Mission MOV Upload Step': True,
        'Mission MP4 Upload Step': True,
        'Mission Image Step': True,
        'Text List Step': True,
        'Text Field Step': True,
        'Message Prompt Step': True,
        'Project Intro': True,
        'Project Modal': True,
        'Content Descriptions': True,
        'Custom Content': True,
        'Multicat2': True,
        'Audio': True,
        'Context': True,
        'Document': True,
        'External Link': True,
        'Quiz Intro': True,
        'Quiz Step 1 Answered': True,
        'Quiz Step 2 Answered': True,
        'Quiz Step 3 Answered': True,
        'Quiz Step 4 Answered A': True,
        'Quiz Step 4 Answered B': True,
        'Quiz Step 5 Answered A': True,
        'Quiz Step 5 Answered B': True,
        'Quiz Step 6': True,
        'Quiz Step 7': True,
        'Quiz Complete': True,
        'Account Menu': True,
        'My Profile': True,
        'Account Settings': True,
        'Announcements': True,
        'Search All Results': True,
        'Search Class Content': True,
        'Search Community Content': True,
        'Search People': True,
        'GWS Page': True,
        'Timeline Page': True,
        'Leaderboard Page': True,
        'Content Page 1': True,
        'Content Page 2': True,
        '404 Not Found Page': True,
    }
    return snapshots_to_take

import datetime
import yaml

CONFIG_FILE_PATH = 'tester_configs.yaml'

def get_percy_branch_name():
    """
    Get the name of the Percy branch to use for the current run.
    """
    branch_name = input('Enter the name of the USER running the Percy branch: ' )
    
    if branch_name == 'MASTER' or branch_name == 'master':
        confirm_overwrite = input('WARNING: You are attempting to push to the master branch. Do you want to continue? (y/n): ')
        if confirm_overwrite.lower() != 'y' or 'Y' or 'yes' or 'Yes' or 'YES':
            print('Exiting without pushing to Percy...')
            exit()
    else:
        current_date = datetime.datetime.now()
        month_abbr = current_date.strftime('%b')
        day = str(current_date.day)
        branch_name = f"{branch_name}_STAGE_{month_abbr}_{day}"
        
    # Update the config file with the new branch name
    # Load the YAML file
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f)

    # Update the percy_branch field
    config['percy_branch'] = branch_name
    
    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.safe_dump(config, f)
    
    return branch_name

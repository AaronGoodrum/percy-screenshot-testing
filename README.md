# percy-screenshot-testing
A suite of tests that uses Percy to take and compare screenshots of web app

Percy Screenshot Testing
This is a Python-based automation framework for taking and comparing screenshots using Percy.

Setup
# Percy Screenshot Testing

This repository contains code for performing visual regression testing with Percy.

## Getting Started

### Prerequisites

- Python 3.x
- Pip

### Installation

1. Clone the repository:

git clone https://github.com/AaronGoodrum/percy-screenshot-testing.git


2. Install the required Python packages:

pip install -r requirements.txt

3. Setup
    Create a .env file in the root directory with the following variables:

        BROWSERSTACK_USERNAME: Your BrowserStack username
        BROWSERSTACK_PASSWORD: Your BrowserStack access key
        ENCRYPTION_KEY: A string to use as the encryption key for the encrypted password in the browserstack_key.key file
        PERCY_TOKEN: Your Percy project token


4. Run mongo_key_encryption.py to create a browserstack_key.key file with your encrypted BrowserStack password.


5. Create a `tester_configs.yaml` file in the root directory of the project with the following contents:

        operating_system: "OS"
        browserstack_username: "<your-browserstack-username>"
        chromedriver_local_path: "/chromedriver"
        browserstack_timezone: "TIMEZONE"
        percy_url: "https://<your-percy-url>/"
        percy_branch: "<your-percy-branch-name>"
        
    Before running the tests, make sure to set the percy_branch value in tester_configs.yaml to the name of the branch you are testing. You can set this manually or use the get_percy_branch_name() function to automatically generate a branch name with the current date and time.

    Will be able to update each time Percy run the test.


### Usage

To run the Percy visual regression tests, run the following command in the root directory of the project:

python percy_main.py


## Contributing

If you have suggestions for how to improve this repository, please [open an issue](https://github.com/AaronGoodrum/percy-screenshot-testing/issues/new).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

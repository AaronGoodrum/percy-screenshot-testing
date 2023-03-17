import os
from pymongo import MongoClient
from cryptography.fernet import Fernet

MONGO_URI = 'mongodb://localhost:27017/?readPreference=primary&directConnection=true&ssl=false'
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browserstack_key.key')
userkey_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intrepid_key.key')


def get_encryption_key():
    """
    Retrieve the encryption key from the file system. If the key file is not found,
    a new key will be generated and saved.
    """
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
    
    return key


def encrypt(data):
    """
    Encrypt the data using Fernet symmetric encryption.
    """
    key = get_encryption_key()
    fernet_key = Fernet(key)
    encrypted_data = fernet_key.encrypt(data.encode())
    return encrypted_data


def decrypt(data):
    """
    Decrypt the data using Fernet symmetric encryption.
    """
    key = get_encryption_key()
    fernet_key = Fernet(key)
    decrypted_data = fernet_key.decrypt(data.encode())
    return decrypted_data.decode()


def save_encrypted_data(username, password, percy_token):
    """
    Save the encrypted data to the MONGODB collection in the database.
    """
    mongo_browserstack_access_collection = get_mongo_collection('automationDB', 'browserstackAccess')


    encrypted_password = encrypt(password)
    encrypted_percy_token = None
    if percy_token is not None:
        encrypted_percy_token = encrypt(percy_token)

    user_record = {
        'username': username,
        'password': encrypted_password,
        'percy_token': encrypted_percy_token,
    }

    mongo_browserstack_access_collection.insert_one(user_record)


def get_mongo_collection(database_name, collection_name):
    """
    Return a MongoDB collection object for the specified database and collection.
    """
    mongo_client = MongoClient(MONGO_URI, 27017)
    mongo_db = mongo_client[database_name]
    mongo_collection = mongo_db[collection_name]
    
    return mongo_collection


def decrypt_browserstack_password(username, is_percy=False):
    """
    Decrypt the browserstack password or percy token using Fernet symmetric encryption.
    """
    mongo_browserstack_access_collection = get_mongo_collection('automationDB', 'browserstackAccess')

    # Load Fernet key
    key = get_encryption_key()
    fernet_key = Fernet(key)

    # Retrieve the user record from MongoDB
    user_record = mongo_browserstack_access_collection.find_one({'username': username})
    if not user_record:
        return None

    if is_percy:
        encrypted_password = user_record.get('percy_token')
    else:
        encrypted_password = user_record.get('password')

    if encrypted_password:
        decrypted_password = fernet_key.decrypt(encrypted_password).decode()
        return decrypted_password
    else:
        return None
    

def decrypt_user_password(encrypted_password):
    # Read the key file and initialize the Fernet object
    with open(userkey_path, 'rb') as key_file:
        key = key_file.read()
    f = Fernet(key)

    # Decrypt the password
    if encrypted_password:
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password
    else:
        return None


if __name__ == '__main__':
    # Get the username and password from the environment variables
    browserstack_username = os.environ.get('BROWSERSTACK_USERNAME')
    browserstack_password = os.environ.get('BROWSERSTACK_PASSWORD')
    percy_token = os.environ.get('PERCY_TOKEN')

    # Encrypt and save the password to MongoDB
    save_encrypted_data(browserstack_username, browserstack_password, percy_token)

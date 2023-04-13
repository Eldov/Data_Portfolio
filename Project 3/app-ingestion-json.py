from datetime import datetime
from decimal import Decimal
import json
import time
import boto3
from faker import Faker
import os
from dotenv import load_dotenv


# Loading environment variables from .env file
load_dotenv()

numEvents = int(os.environ.get('numEvents'))

# Define custom encoder class for json files
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomEncoder, self).default(obj)


# Creating Faker lib's instance
fake = Faker(locale='en_GB')

# Getting Access Variables from .env file 
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Setting AWS Session using Access Variables
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

# Defining the bucket name

bucket_name = os.environ.get('BUCKET_RAW')

# Defining app's page list
pages = [
    'home',
    'products',
    'product_details',
    'cart',
    'checkout',
    'profile'
]

# Defining users' action list
actions = [
    'view_page',
    'click_link',
    'add_to_cart',
    'remove_from_cart',
    'checkout',
    'purchase'
]

# Generates random users events
for i in range(numEvents):
    # Defines user's data
    user_data = {
        'id': fake.random_int(min=1, max=100),
        'name': fake.name(),
        'sex': fake.random_element(elements=('Male', 'Female')),
        'address': fake.address(),
        'ip': fake.ipv4(),
        'state': fake.state(),
        'latitude': fake.latitude(),
        'longitude': fake.longitude()
    }

    # Defines event's data
    event_data = {
        'timestamp': int(time.time()),
        'page': fake.random_element(elements=pages),
        'action': fake.random_element(elements=actions),
        'product_id': fake.random_int(min=1, max=100),
        'quantity': fake.random_int(min=1, max=5),
        'estoque_id': fake.random_int(min=1, max=100),
        'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2))),
        'estoque_id_number': fake.random_int(min=10, max=100),
        'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)))
    }
    
    # Matches user and event data in a single object
    data = {
        'user': user_data,
        'event': event_data
    }

    # Writes the result in a json file on premise
    now = datetime.now()
    frt_date = now.strftime("%d_%m_%Y_%H_%M_%S")

    with open(f"event_customers_mobile{i}_{frt_date}.json", "w") as f:
        time.sleep(1)
        json.dump(data, f, cls=CustomEncoder)

    # # Saaves the files in a S3 bucket
    #time.sleep(3)
    s3.Object(bucket_name, f"event_customers_mobile{i}_{frt_date}.json").put(Body=json.dumps(data, cls=CustomEncoder))
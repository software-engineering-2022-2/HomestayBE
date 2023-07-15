import re, faker
import csv, json
import random
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
from tqdm import tqdm

cloudinary.config( 
  cloud_name = "dp9km8tmk", 
  api_key = "649821629756593", 
  api_secret = "KoF4eTbX-cr9o7_Pc77_W3ro1MQ" 
)

def login_admin():
    url = 'http://127.0.0.1:8000/api/token/'
    login_data = {'username': 'admin', 'password': '123456'}
    response = requests.post(url, data=json.dumps(login_data), headers={'Content-Type': 'application/json'})
    token = response.json()['access']

    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    
def prepare():
    with open('data_generation/utils_data/vietnamese_cities_districts.txt', 'r') as f:
        data = f.read()
        cities = {}
        current_city = None
        for line in data.split('\n'):
            match = re.match(r'(\d{1,2})-(.+)', line)
            if match:
                current_city = match.group(2).strip()
                cities[current_city] = []
            else:
                match = re.match(r'(\d{3})-(.+)', line)
                if match:
                    district_name = match.group(2).strip()
                    cities[current_city].append(district_name)

    with open('data_generation/utils_data/vietnamese_streets.txt', 'r') as f:
        streets = f.read().split('\n')
    
    return cities, streets

def generate_users(cities, streets, headers, num_customers=80, num_managers=20):
    fake = faker.Faker('vi_VN')
    num_users = num_customers + num_managers
    users = []
    manager_usernames = []

    # fetch full avatar urls from cloudinary
    resources = cloudinary.api.resources(type = 'upload', prefix = "homestay-renting-website/user_avatars", max_results=500)
    urls = []
    for resource in resources['resources']:
        url = cloudinary.utils.cloudinary_url(resource['public_id'])
        urls.append(url[0])

    for i in range(num_users):
        # fake a Vietnamese name
        username = fake.user_name()
        password = username + '123'
        is_superuser = 'false'
        first_name = fake.first_name()
        last_name = fake.last_name()
        if i < num_managers:
            is_staff = 'true'
            manager_usernames.append(username)
        else:
            is_staff = 'false'
        is_active = 'true'
        phone_number = fake.phone_number().replace('-', '').replace('x', '')
        city = list(cities.keys())[i % len(cities)]
        district = cities[city][i % len(cities[city])]
        street_name = random.choice(streets)
        street_number = random.randint(1, 999)
        email = fake.email().replace('@', str(random.randint(0, 1000000007)) + '@')
        avatar = random.choice(urls)
        user_data = {
            'username': username,
            'password': password,
            'is_superuser': is_superuser,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_active': is_active,
            'phone_number': phone_number,
            'street_name': street_name,
            'street_number': street_number,
            'city': city,
            'district': district,
            'email': email,
            'avatar': avatar
        }
        users.append(user_data)
    
    # send data to server
    print('Generating users...')
    url = 'http://127.0.0.1:8000/api/users/'
    num_rows = len(users)
    for user in tqdm(users, total=num_rows):
        # Convert the user data to a JSON payload
        payload = json.dumps(user)

        # Send the POST request with the JSON payload for the current user
        response = requests.post(url, data=payload, headers=headers)

        # Check the response status code for the current user
        if response.status_code != 201:
            print('Error sending data for user:', user, response.text)
    
    # Get ids of managers
    manager_ids = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for user in data:
            if user['username'] in manager_usernames:
                manager_ids.append(user['id'])
    
    print("Number of managers: ", len(manager_ids))
    return manager_ids

def generate_price_configs(headers, num_configs=15):
    configs = []

    for i in range(num_configs):
        deposit_percentage = round(random.uniform(0.0, 1.0), 2)
        cancellation_refund_percentage = round(random.uniform(0.0, 1.0), 2)
        free_cancellation_days = random.randint(0, 30)
        discount = round(random.uniform(0.0, 1.0), 2)

        config = {
            "deposit_percentage": deposit_percentage,
            "cancellation_refund_percentage": cancellation_refund_percentage,
            "free_cancellation_days": free_cancellation_days,
            "discount": discount
        }

        configs.append(config)

    # Send configs to server
    print('Generating pricing configs...')
    url = 'http://127.0.0.1:8000/api/pricing_configs/'
    num_rows = len(configs)
    for config in tqdm(configs, total=num_rows):
        # Convert the user data to a JSON payload
        payload = json.dumps(config)

        # Send the POST request with the JSON payload for the current user
        response = requests.post(url, data=payload, headers=headers)

        # Check the response status code for the current user
        if response.status_code != 201:
            print('Error sending data for config:', config, response.text)
    
    # Get ids of configs
    config_ids = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for config in data:
            config_ids.append(config['id'])

    return config_ids

def generate_homestay_name():
    # Define a list of possible adjectives and nouns for the name
    adjectives = [
        "Cozy",
        "Charming",
        "Quaint",
        "Rustic",
        "Serene",
        "Tranquil",
        "Idyllic",
        "Enchanting",
        "Elegant",
        "Gorgeous",
        "Stylish",
        "Vintage",
        "Luxurious",
        "Modern",
        "Sleek"
    ]
    nouns = [
        "Retreat",
        "Hideaway",
        "Oasis",
        "Sanctuary",
        "Haven",
        "Escape",
        "Lodge",
        "Cottage",
        "Villa",
        "Mansion",
        "Palace",
        "Manor",
        "Estate",
        "Chateau",
        "Maison"
    ]

    # Randomly select an adjective and a noun from the lists
    selected_adjective = random.choice(adjectives)
    selected_noun = random.choice(nouns)

    # Combine the adjective and noun into a single name and return it
    name = f"{selected_adjective} {selected_noun}"
    return name

def generate_homestays(cities, streets, manager_ids, config_ids, headers, num_homestays=100):
    # List of homestay descriptions
    with open('data_generation/utils_data/homestay_descriptions.txt', 'r') as f:
        descriptions = f.readlines()
    
    # fetch images and prices from json file
    with open("data_generation/utils_data/homestay_img_price.json", "r") as output_file:
        img_price_list = json.load(output_file)

    homestays = []
    for i in range(num_homestays):
        name = generate_homestay_name()
        price = img_price_list[i]['price']
        description = random.choice(descriptions)
        max_num_adults = random.randint(1, 10)
        max_num_children = random.randint(1, 10)
        allow_pet = random.choice([True, False])
        availability = random.choice([True, False])
        city = list(cities.keys())[i % len(cities)]
        district = cities[city][i % len(cities[city])]
        street_name = random.choice(streets)
        street_number = random.randint(1, 999)
        manager_id = random.choice(manager_ids)
        pricing_config_id = random.choice(config_ids)
        image = img_price_list[i]['img'][0]

        homestay = {
            "name": name,
            "price": price,
            "description": description,
            "max_num_adults": max_num_adults,
            "max_num_children": max_num_children,
            "allow_pet": allow_pet,
            "availability": availability,
            "street_number": street_number,
            "street_name": street_name,
            "city": city,
            "district": district,
            "manager_id": manager_id,
            "pricing_config_id": pricing_config_id,
            "image": image
        }

        homestays.append(homestay)
    
    # send data to server
    print('Generating homestays...')
    url = 'http://127.0.0.1:8000/api/homestays/'
    num_rows = len(homestays)
    for homestay in tqdm(homestays, total=num_rows):
        # Convert the user data to a JSON payload
        payload = json.dumps(homestay)

        # Send the POST request with the JSON payload for the current user
        response = requests.post(url, data=payload, headers=headers)

        # Check the response status code for the current user
        if response.status_code != 201:
            print('Error sending data for homestay:', homestay, response.text)

    # Get ids of homestays
    homestay_ids = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for homestay in data:
            homestay_ids.append(homestay['id'])

    return homestay_ids

def generate_service_types(headers):
    service_types = [
        "Swimming pool",
        "Gym",
        "Spa",
        "Restaurant",
        "Bar",
        "Cafe",
        "Parking",
        "Laundry",
        "Airport shuttle",
        "Breakfast"
    ]

    # Send service_types to server
    print('Generating service types...')
    url = 'http://127.0.0.1:8000/api/service_types/'
    num_rows = len(service_types)
    for service in tqdm(service_types, total=num_rows):
        # Convert the user data to a JSON payload
        payload = json.dumps({"name": service})

        # Send the POST request with the JSON payload for the current user
        response = requests.post(url, data=payload, headers=headers)

        # Check the response status code for the current user
        if response.status_code != 201:
            print('Error sending data for service type:', service, response.text)
    
    # Get ids of service types
    service_types = {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for service in data:
            service_types[service['name']] = service['id']

    return service_types

def define_service_descriptions():
    service_types_description = {
        "Swimming pool": [
            "Experience the ultimate relaxation with our swimming pool service. Our expert staff will ensure that you have a memorable experience.",
            "Take a dip in our luxurious swimming pool and enjoy the beautiful surroundings.",
            "Our swimming pool is the perfect place to unwind after a long day of sightseeing."
        ],
        "Gym": [
            "Get fit and stay healthy with our state-of-the-art gym equipment.",
            "Our gym is equipped with everything you need for a great workout.",
            "Our expert trainers will help you achieve your fitness goals."
        ],
        "Spa": [
            "Indulge in a luxurious spa treatment and feel your stress melt away.",
            "Our spa offers a wide range of treatments to help you relax and rejuvenate.",
            "Experience the ultimate in pampering with our spa services."
        ],
        "Restaurant": [
            "Savor the flavors of our delicious cuisine in our elegant restaurant.",
            "Our restaurant offers a wide range of dishes to suit every taste.",
            "Enjoy a romantic dinner for two in our intimate restaurant setting."
        ],
        "Bar": [
            "Relax with a drink in our cozy bar and enjoy the company of friends.",
            "Our bar offers a wide selection of cocktails, beers, and wines.",
            "Unwind after a long day with a refreshing drink from our bar."
        ],
        "Cafe": [
            "Start your day off right with a delicious coffee from our cafe.",
            "Our cafe offers a wide range of pastries, sandwiches, and snacks.",
            "Take a break from sightseeing and enjoy a relaxing cup of tea or coffee in our cozy cafe."
        ],
        "Parking": [
            "Convenient parking is available for all guests at our homestay.",
            "Leave your car with us and enjoy peace of mind during your stay.",
            "Our secure parking lot ensures that your vehicle is safe and sound."
        ],
        "Laundry": [
            "Stay fresh and clean during your stay with our laundry services.",
            "Our expert staff will take care of all your laundry needs.",
            "Enjoy clean clothes every day with our convenient laundry services."
        ],
        "Airport shuttle": [
            "Arrive at your destination in style with our airport shuttle service.",
            "Our comfortable shuttle will take you directly to your homestay.",
            "Skip the hassle of public transportation and let us take care of your airport transfer."
        ],
        "Breakfast": [
            "Start your day off right with a delicious breakfast from our homestay.",
            "Our breakfast menu offers something for everyone, from sweet to savory dishes.",
            "Enjoy breakfast in bed or in our cozy dining area."
        ]
    }


    return service_types_description

def generate_homestay_services(homestay_ids, service_types, headers):
    descriptions = define_service_descriptions()
    homestay_services = {}

    for homestay_id in homestay_ids:
        num_services = random.randint(1, len(service_types))
        selected_services = random.sample(list(service_types.keys()), num_services)
        homestay_services[homestay_id] = []
        for service in selected_services:
            description = random.choice(descriptions[service])
            homestay_service = {
                "service_type_id": service_types[service],
                "description": description,
                'price': random.randint(5, 50),
                'availability': False if random.randrange(5) == 1 else True
            }
            homestay_services[homestay_id].append(homestay_service)

    # Send homestay_services to server
    print('Generating homestay services...')
    # url = homestays/<str:homestay_id>/services/
    url_1 = 'http://127.0.0.1:8000/api/homestays/'
    url_2 = '/services/'

    num_rows = len(homestay_services)
    for homestay_id, services in tqdm(homestay_services.items(), total=num_rows):
        # Convert the user data to a JSON payload
        payload = json.dumps(homestay_service)

        # Send the POST request with the JSON payload for the current user
        url = url_1 + str(homestay_id) + url_2
        for service in services:
            payload = json.dumps(service)
            response = requests.post(url, data=payload, headers=headers)

            # Check the response status code for the current user
            if response.status_code != 201:
                print('Error sending data for homestay service:', service, response.text)


# -----------------------------

cities, streets = prepare()
manager_ids = generate_users(cities, streets, login_admin(), 1, 2)
config_ids = generate_price_configs(login_admin(), 15)
homestay_ids = generate_homestays(cities, streets, manager_ids, config_ids, login_admin(), 5)
service_types = generate_service_types(login_admin())
generate_homestay_services(homestay_ids, service_types, login_admin())

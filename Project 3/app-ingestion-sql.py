import psycopg2
from faker import Faker
import random
from dotenv import load_dotenv
import os

def createTables(cur):
    try:
        # Create table Customers
        cur.execute("""
        CREATE TABLE Customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
        """)

        # Create table Products
        cur.execute("""
        CREATE TABLE Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10,2)
        )
        """)

        # Create table Orders
        cur.execute("""
        CREATE TABLE Orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(id),
            product_id INTEGER REFERENCES Products(id),
            quantity INTEGER,
            total DECIMAL(10,2),
            status VARCHAR(20)
        )
        """)
        print ("Success creating tables in the db")
    except Exception as e:
        print (f"Error creating tables in the db:{e}")
    return 0

def randomData(cur, conn, numClients):
    try:
        # Inserting data in the table Customers
        customers = []
        for i in range(numClients):
            name = fake.name()
            email = fake.email()
            cur.execute("INSERT INTO Customers (name, email) VALUES (%s, %s)", (name, email))
            customers.append(name)

        conn.commit()
        print ("Success generating users' data")
    except Exception as e:
        print (f"Error trying to generate users' data: {e}")

    try:
        # Inserting data in the table Products
        products = ['Laptop Acer Aspire 5', 'Smartphone Samsung Galaxy S20', 'Smart TV LG 50 inches', 'Mouse Logitech MX Master', 'Earphone Sony WH-1000XM4', 'Keyboard Corsair K95', 'Camera Canon EOS Rebel T7', 'Headset HyperX Cloud II', 'Gaming Monitor Alienware 34"', 'Tablet Samsung Galaxy Tab S7', 'Speakers Bluetooth JBL Flip 5', 'Printer HP Deskjet 3755', 'Smartwatch Apple Watch Series 6', 'Drone DJI Mavic Air 2', 'Grass Trimmer Tramontina', 'Laptop Dell Inspiron 15', 'Smartphone Motorola Moto G Power', 'Smart TV Sony 55 inches', 'Mouse Pad Gamer Corsair MM300', 'Earphone JBL Tune 750BTNC', 'Keyboard Logitech K780', 'Security Camera Nest Cam IQ', 'Headset Razer Kraken Tournament', 'Monitor LG UltraWide 29"', 'Tablet Amazon Fire HD 10', 'Speakers Sony SRS-XB43', 'Printer Epson EcoTank L3150', 'Smartwatch Samsung Galaxy Watch 3', 'Drone DJI Mini 2', 'Trimmer Tramontina', 'Laptop HP Pavilion 15', 'Smartphone Apple iPhone SE', 'Smart TV TCL 50 inches', 'Mouse Logitech G502 HERO', 'Earphone Bose QuietComfort 35 II', 'Keyboard Razer BlackWidow Elite', 'Camera GoPro HERO9 Black', 'Headset SteelSeries Arctis 7', 'Monitor Dell UltraSharp 27"', 'Tablet Apple iPad Air', 'Speakers JBL Xtreme 3', 'Printer Brother MFC-L2750DW', 'Smartwatch Fitbit Versa 3', 'Drone DJI Mavic Mini', 'Robot Vacuum iRobot Roomba i3+', 'Laptop Asus Zenbook UX425', 'Smartphone OnePlus 8T', 'Smart TV Samsung 55 inches', 'Mouse Pad Gamer Razer Goliathus', 'Earphone Sennheiser Momentum True Wireless 2', 'Keyboard Logitech K810', 'Camera Mirrorless Sony Alpha a7 III', 'Headset Astro A50 Wireless', 'Monitor Asus TUF Gaming 24,5"', 'Tablet Microsoft Surface Pro 7', 'Speakers Ultimate Ears BOOM 3', 'Printer Canon PIXMA TS9120', 'Smartwatch Garmin Venu', 'Drone DJI Phantom 4', 'Washer Karcher K4', 'Laptop Lenovo IdeaPad 5', 'Smartphone Xiaomi Redmi Note 9 Pro', 'Smart TV LG OLED 55 inches', 'Mouse Logitech MX Anywhere 2S', 'Earphone Jabra Elite 85h', 'Keyboard HyperX Alloy FPS Pro', 'Security Camera Arlo Pro 3', 'Headset Turtle Beach Stealth 700', 'Monitor Acer Nitro XV272U']
        categories = ['Eletronics', 'Technology', 'Phones', 'Accessories']
        for i in range(len(products)):
            name = products[i]
            category = categories[i % len(categories)]
            price = round(random.uniform(50, 1000), 2)
            cur.execute("INSERT INTO Products (name, category, price) VALUES (%s, %s, %s)", (name, category, price))
        conn.commit()
    except Exception as e:
        print (f"Error trying to generate products' data: {e}")

    try:
        # Inserting data in the table Orders
        for i in range(len(products)):
            customer_id = random.randint(1, len(customers))
            product_id = random.randint(1, len(products))
            quantity = random.randint(1, 5)
            cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cur.fetchone()[0]
            total = round(price * quantity, 2)
            status = random.choice(['Pending', 'Processing', 'Ready'])
            cur.execute("INSERT INTO Orders (customer_id, product_id, quantity, total, status) VALUES (%s, %s, %s, %s, %s)", (customer_id, product_id, quantity, total, status))
        conn.commit()
    except Exception as e:
        print (f"Error trying to generate orders' data: {e}")
        
    # Closing the db connection
    cur.close()
    conn.close()

# Creating Faker lib's instance
fake = Faker(locale='en_GB')

# Loading environment variables from .env file
load_dotenv()

# Connecting to PostgreSQL db
conn = psycopg2.connect(
    host = os.environ.get('DB_HOST'),
    port = os.environ.get('DB_PORT'),
    database = os.environ.get('DB_NAME'),
    user = os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

numClients = int(os.environ.get('numClients'))

# Creating a cursor to run SQL code
cur = conn.cursor()
createTables(cur)
randomData(cur, conn, numClients)
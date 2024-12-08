<img width="1502" alt="image" src="https://github.com/user-attachments/assets/b2e57a34-a140-4a05-94b3-bc9fd448a59e"># E-commerce Web Application with Cloud and Distributed Computing Integration

## Project Overview
This project demonstrates our understanding of web application development and the integration of cloud 
services. Our team built a fully functional e-commerce application using Django as the backend framework,
with HTML, CSS, and AJAX for the frontend. The application is enhanced with cloud services, distributed computing, and real-time message processing.

## Objective
### The primary goal of this project was to solve a real-world case study using a web application while showcasing our skills in:

1. Web development (Django, HTML, CSS, AJAX).
2. Cloud service integration (AWS RDS, Hadoop).
3. Real-time data streaming using Apache Kafka.
4. Big data analytics with MapReduce.

## Features Implemented
### Web Application Development
Framework: Django
Frontend: HTML, CSS, and AJAX

## Features:
1. Authentication system: Secure login/signup.
2. CRUD functionality for products and orders.
3. A displaying order analytics using MapReduce results.

## Cloud and Distributed Computing Integration
1. Database: MySQL hosted on AWS RDS.
2. Configured and connected the Django application to an AWS MySQL database.
3. Ensured proper database transactions and queries.

## Hadoop:
Implemented MapReduce on order data for analytics.

## Apache Kafka:
Real-time message streaming for adding products to the cart.
Consumed and displayed these messages in real-time within the application

Case Study
E-commerce Inventory and Order Management
The application allows users to browse products, add them to their cart, and place orders. 
Real-time notifications, analytics, and data processing were incorporated for a comprehensive shopping experience

## Technical Implementation
### Technologies Used
Backend: Django
Frontend: HTML, CSS, AJAX
Database:Sqlite3 for local and  MySQL (AWS RDS)
Messaging: Apache Kafka
Big Data Analytics: Hadoop (MapReduce)

## Cloud Configuration
### AWS RDS:
Hosted the MySQL database on Amazon RDS.
Used secure credentials to connect the Django app to the cloud database.

### Hadoop:
Set up locally for processing data with MapReduce.

### Apache Kafka:
Installed and configured locally to handle message brokering.


# How to Run the Project
## Clone the Repository

git clone <https://github.com/phasetumurere/class_assignment_group_8>
cd <repository-folder> 

# Setup Environment
pip install -r requirements.txt
Configure database settings in settings.py to match your AWS RDS credentials.
Start Kafka server and ensure the producer and consumer scripts are running.

## Challenges Faced
### Database Configuration:

Ensuring secure connections between Django and AWS RDS required extra configuration and debugging.

### Hadoop Setup:

Setting up HDFS and running MapReduce jobs locally required us energy and in the end we've decided 
to just export the .csv file of the orders and run MapReduce then just dispay it's template.

### Kafka Real-time Integration:

Synchronizing real-time events and ensuring efficient consumption of messages posed initial challenges.

## Results
### Functional Features:
1. Real-time cart updates using Kafka.
2. Accurate order analytics through MapReduce jobs.
   
### Cloud Integration:
1. Successfully configured MySQL on AWS RDS.
### User Experience:
A responsive and interactive UI built with Javascript, bootstrap and Jax.

## Group Members
Phase TUMURERE: Role (Backend development and Kafka Integration)
Eric Tunzi: Role (Hadoop setup and Frontend development)
Solange UMUGWANEZA: (Cloud Database Integration, Documentation)

Home page
<img width="1498" alt="image" src="https://github.com/user-attachments/assets/4bdffa48-ee78-4936-be55-c2430fc5dd66">

Adding a Product in cart
<img width="1503" alt="image" src="https://github.com/user-attachments/assets/63ddd56a-437f-4f6d-ba77-d42ead3dfea1">

Checkout the cart for making the order or back in cart to remove or add other products
<img width="1509" alt="image" src="https://github.com/user-attachments/assets/2283cf30-fe7e-4b55-a16a-8cb71499cf49">

Filling the Billing address for the future delivery incase of it
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/fe19568e-ea96-45d0-ad1a-afe06453248c">

Checkout the order for the confirmation then continue with payment process
<img width="1512" alt="image" src="https://github.com/user-attachments/assets/8ea9bf5e-8292-4948-ba42-f28c54faef54">

Admin Dashboard
<img width="1511" alt="image" src="https://github.com/user-attachments/assets/bb1a1f7c-ef28-435b-911c-93dd1c5e15cb">

AWS_MySqlDb
<img width="1512" alt="image" src="https://github.com/user-attachments/assets/f85a0bff-7161-491c-9f6e-4fe574bf5f41">

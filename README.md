Python Test Task
============

Overview
-------

This application is designed to fetch user data at regular intervals and enhance it by retrieving additional information. It leverages Celery for task scheduling and execution, ensuring efficient storage of user, address, and credit card data.

Accomplishments
-------

- Developed an application utilizing Celery for effective task scheduling.
- Implemented a periodic task to extract user data from the [Random Data API](https://random-data-api.com/) and store it in the database.
- Created separate periodic tasks for extracting address and credit card information from the [Random Data API](https://random-data-api.com/), with the data stored in distinct tables linked to the corresponding user.
- Wrote tests using `pytest` to ensure application reliability and correctness.
- Containerized the application with Docker for simplified deployment and management.
- Provided comprehensive setup and usage instructions in this README.
- Implemented an optional feature to view saved data.
- Utilized a linter to maintain code quality and adhere to best practices.

Stack
-------

- **Programming Language:** `Python`
- **Task Queue:** `Celery`
- **Testing Framework:** `Pytest`
- **Web Framework:** `Django`
- **Database:** `PostgreSQL`
- **Message Broker:** `RabbitMQ`
- **Linter:** `Flake8`


Important Information
-------
After starting the application, a default superuser will be created with the following credentials:

 - **Username**: `admin`
 - **Password**: `password`
 - **Email**: `admin@example.com`  

**Warning**: This password is weak. 
If you prefer not to have a superuser with these credentials, 
please remove the following lines from the `script.sh` file:  
   ```
   echo "Create default superuser"
   python manage.py create_default_superuser
   ```

How to run this app?
-------
### Steps

1. **Clone the repository files to your computer:** 
  
   ```bash
   git clone <repository-url>
   ```
   
2. **Enter the folder of the repository:**

   ```bash
   cd Python_test_task
   ```

3. **Create and Fill in the `.env` File:**
   
   Create a file named `.env` in the root of your project and include the following environment variables:

   ```plaintext
   # Development settings
   DEV=true

   # Allowed hosts for the application
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Django secret key for cryptographic signing
   SECRET_KEY=192jr1092jf193ngj9428n9o4j29f3j4

   # Database configuration
   DB_NAME=user_db
   DB_USER=postgres_user
   DB_PASS=password123
   ```

4. **Build and run docker compose:**

   ```bash
   docker-compose up -d --build
   ```
   
5. **Run Tests (Optional):**

   **Important!** Ensure that the `DEV` variable in `.env` file is set to `TRUE`.

   Once your Docker containers are up and running, execute the following command to run the tests:

   ```bash
   docker exec -it app pytest --import-mode=importlib
   ```
   
6. **Run linter (Optional):**

   **Important!** Ensure that the `DEV` variable in `.env` file is set to `TRUE`.

   Once your Docker containers are up and running, execute the following command to run the linter:

   ```bash
   docker exec -it app flake8
   ```
   
   
Docker containers
-------
After building the application, you will have five Docker containers:

* **Django Application**: Accessible for viewing data on the admin page and creating periodic tasks.  
* **Celery Beat**: Responsible for queuing tasks at specified intervals.  
* **Celery Worker**: Executes tasks taken from the queues.  
* **RabbitMQ**: Manages the queues for tasks.  
* **PostgreSQL Database**: Stores the data.  


How to view fetched data?
-------
### Steps
1. **Create Superuser (Optional)**  
   If you have deleted the default superuser, you can create a new superuser account by running the following command and following the prompts:

   ```bash
   docker exec -it app python manage.py createsuperuser
   ```
   
2. **Login to admin page:**  
Navigate to http://127.0.0.1:8001/admin/ and 
enter your username and password. For the 
default superuser, use the following credentials:

   - **Username**: `admin`
   - **Password**: `password`

3. **View your data**  
After logging in, you'll have 
access to view user, address, 
and credit card data. The admin panel also 
allows you to perform many other actions.


Important
-------

Since random-data-api.com always returns random 
values, regardless of the specified URL 
parameters, I created a user task that not 
only fetches and saves user data but also 
verifies whether the user's address exists 
in the database. If the address is already 
present, I update the foreign key (FK) in 
the address record to associate it with the 
specific user.

I applied the same approach for credit card 
data. When fetching address or credit card 
information, a unique identifier (uid) is 
returned. I check if a user with that uid 
exists in the database, and if they do, I 
link the user to the corresponding address.

As a result, some addresses and credit cards 
may remain unassigned to any user.

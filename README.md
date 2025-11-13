# EGASP Project
This project is the EGASP Database. Below is the guide to set up the project on your local machine.


# Getting Started


1. Open terminal and Clone the Repository

Start by cloning the repository from GitHub:
git clone https://github.com/squarfie/EGASP_project.git

2. Create a Virtual Environment
Once the repository is cloned, navigate to the project directory and create a Python virtual environment. This will isolate the dependencies for the project.


cd egasp_project
python -m venv egasp  # or customize the name of your virtual environment

3. Activate the Virtual Environment
Activate the virtual environment. The activation command depends on your operating system:

Windows:

egasp\Scripts\activate

Mac/Linux:

source egasp/bin/activate

You should now see (egasp) before your command prompt, indicating that the virtual environment is active.

4. Install the Required Modules 
Install all the necessary dependencies:

pip install Django
pip install -r requirements.txt
pip install pandas
pip install psycopg2
pip install python-decouple
pip install Unipath
pip install django-widget-tweaks
pip install django-phonenumber-field[phonenumbers]
pip install xhtml2pdf
pip install whitenoise
pip install openpyxl
pip install SQLAlchemy


This will install all the Python modules required for the project.

5. Set Up the Database

If the project uses an SQLite or PostgreSQL database, follow these steps to set it up:


# Create a new PostgreSQL database.

download PostgreSQL and follow the instructions to install.

Open pgadmin

Create a new database and use the indicated DB_NAME from the .env file

Database names:

Default (for testing): test_db

For deployment: Egasp_db

⚡ You may need to update the DB_NAME in the .env file.
⚡ Uncomment DB_NAME=Egasp_db for deployment, and comment out DB_NAME=test_db.


# Run migrations:

python manage.py makemigrations
python manage.py migrate

6. Start the Application (Development Mode)
To start the server:

Running the Django Development Server:
To start the server on the default port (8000), run:

python manage.py runserver

To allow access from other devices on your local network (LAN), use:
python manage.py runserver 0.0.0.0:(your preferred port number)

example:
python manage.py runserver 0.0.0.0:8090

then access the database using any browser by typing:
http://127.0.0.1:8090


Or, to bind the server to your machine’s local IP address with a custom port:
python manage.py runserver 192.168.1.243:8090

🔹 Replace 192.168.1.243 with your actual local IP address in settings.py "ALLOWED HOSTS"

🔹 Use only for development/testing. Avoid exposing this in production environments.


🔔 You can change the port number if desired.
🔔 Important: If deploying with Gunicorn, ensure the port is also updated in the gunicorn-cfg.py configuration file.

# Application Setup:

7. Register Your Account
Register your name and password, then log in to the system.

8. Configure System Settings
Configure your codes, breakpoints, antibiotics, and locations using the options under the "Utilities" menu.

9. Upload Breakpoints and Antibiotics
Use the "Breakpoints_egasp.xlsx" template.

First, add the antibiotics and breakpoints into the Excel file.

Upload it through the "Breakpoints" option under the "Utilities" menu on the dashboard.

You can find the template files inside the template_docs folder located in the main app directory.

⚡ You can also add more antibiotics and breakpoints directly through the database.
⚡ However, if you're setting up the database for the first time, the most convenient approach is to upload the Excel file. Before doing so, 
ensure that all required antibiotics are included in the file.

10. Upload Cities List
Click on "Add Cities" under the Utilities menu, and upload the file named "Citieslist.xlsx" to add the complete list of cities in the Philippines.

✨ If you need to add more cities later, you do not need to modify the Excel file.
✨ The database provides a feature to add and delete the list of cities and barangays directly.

# Done! 🎉
You now have the EGASP Database running on your local machine!


# Useful TIPS:
This includes instructions when running in production mode

# Prerequisites
Before proceeding, ensure that you have the following:

Docker and Docker Compose installed on your machine or server.

A .env file containing the necessary PostgreSQL credentials.

Your project files, including configurations for Gunicorn, Nginx, and Docker.

# Setup Instructions

1. Create the .env file

In the root of your project, make sure you have created a .env file containing the following environment variables for PostgreSQL:

DB_NAME=your_db_name

DB_USER=your_db_user

DB_PASSWORD=your_db_password

Replace your_db_name, your_db_user, and your_db_password with your actual PostgreSQL database credentials.


# if .env file is already created:
--> Update the .env File

Open your .env file and update the paths for your STATIC_DIR and STATICFILES_DIR:

Example static directory:
D:/EGASP_PRO_050525/EGASP_DATA/apps/static

Example staticfiles directory:
D:/EGASP_PRO_050525/EGASP_DATA/staticfiles

--> If necessary, update the port number to 5432, which is the default for PostgreSQL used by Django.

--> Important: If you change the port number, make sure to also update it in the utils.py file to match. Locate the line that defines the database engine and ensure the port is correct:

ex: (if using POSTGRESQL)

engine = create_engine('postgresql+psycopg2://postgres:admin123@localhost:5432/test_db')


2. Build the Docker Images

Use the following command to build the Docker images based on the Dockerfiles and configurations you have set up:

docker-compose build
Start the Services

3. Start the services (Django app, PostgreSQL database, and Nginx) in detached mode by running:

docker-compose up -d

This will launch the containers in the background.

4. Run Migrations

Apply the Django database migrations to set up the schema by running:

docker-compose exec web python manage.py migrate

5. Collect Static Files

Collect static files to be served by Nginx:

docker-compose exec web python manage.py collectstatic --noinput

6. Start the Development Server

Localhost (Default)
python manage.py runserver

•	Accessible at: http://127.0.0.1:8000


LAN / Custom Port
To make it accessible across the local network:
python manage.py runserver 0.0.0.0:8090

•	Accessible from: http://127.0.0.1:8090
or specify your IP:

python manage.py runserver 10.10.103.54:8090

•	Accessible from other devices: http://10.10.103.54:8090

🔒 Note: This setup is for development only, not for production use.


Make sure have added the local IP address (if running in a different IP) at settings.py 
In this case:
ALLOWED_HOSTS = [
    config('SERVER', default=''),  # Use SERVER from .env if exists
    'localhost',
    '127.0.0.1',
    '10.10.103.54',
    'mariseru.pythonanywhere.com',  # Your PythonAnywhere domain
]



7. Accessing the Application

After running the above commands and confirming that the services are running, you can access the application on the following URLs:

Local Machine: http://127.0.0.1:8000/

Remote Server: http://<your_server_ip_or_domain>
            e.g. http://10.10.103.54:8090/



8. Optional Steps
Monitoring Logs

You can monitor the logs for any of the containers (web, nginx, db) by running:

docker-compose logs -f

9. Stopping the Services

To stop all services, use the following command:

docker-compose down

10. Restarting the Services

If you need to restart all services, use:

docker-compose restart

# Notes for Production

Security: Make sure your PostgreSQL credentials and any other sensitive information are securely stored in the .env file and not exposed in public repositories.

Scaling: If your application grows, you might want to adjust the number of Gunicorn workers or scale your database and web containers.

Backups: Set up regular backups for the PostgreSQL database to ensure data is protected.

# Troubleshooting
PostgreSQL Connection Errors:

Ensure the credentials in your .env file are correct.

Verify that PostgreSQL is running using docker-compose ps.

Static Files Not Loading:

Run python manage.py collectstatic to ensure static files are collected properly.

Make sure Nginx is correctly configured to serve the static files from the correct location.

# Gunicorn Issues:

If Gunicorn isn’t starting, check the logs with docker-compose logs web for any errors related to Gunicorn or Django.

Ensure the correct Gunicorn command is being executed by reviewing the docker-compose.yml configuration.

By following this guide, you should be able to successfully deploy your EGASP application in a production environment.


# Missing antiboitic entries when download button is used
Relinking of entries (this is useful during downloading of entries)
--- > Even if the ForeignKey exists, some AntibioticEntry records might not have ab_idNumber_egasp set, especially if they were created before the foreign key was enforced, or imported without linking. to ensure linking of entries works before download of data, run this:

1. OPEN DJANGO SHELL

Run:
python manage.py shell


2. Fix Existing Unlinked Data (One-Time Fix):

Run:
from apps.home.models import AntibioticEntry, Egasp_Data

for entry in AntibioticEntry.objects.filter(ab_idNumber_egasp__isnull=True):
    try:
        match = Egasp_Data.objects.get(ID_Number=entry.ab_EgaspId)
        entry.ab_idNumber_egasp = match
        entry.save()
        print(f"Linked {entry.ab_EgaspId} to {match.id}")
    except Egasp_Data.DoesNotExist:
        print(f"No match found for {entry.ab_EgaspId}")
        continue


3. Confirm the links were fixed:

Run:
from apps.home.models import AntibioticEntry

# Check how many are still unlinked (should be 0 ideally)

Run:
AntibioticEntry.objects.filter(ab_idNumber_egasp__isnull=True).count()

4. Re-test your download feature
Now go back to your app and trigger the Download Combined Table function.

Since the AntibioticEntry records are now properly connected to Egasp_Data, the antibiotic fields should now appear in the CSV output as expected.


# Recommended Browser

For optimal performance, it is recommended to use any modern, up-to-date version of Chrome, Firefox, Brave, or other equivalent browsers when accessing the system.

Note: The system uses AJAX and JavaScript features that may not function properly on certain browsers.
Please refer to the “List of Browsers with Possible Issues” for more details.


# List of Browsers with Possible Issues

(Feel free to add your browser here if the system behaves unexpectedly while using it.)

1. Microsoft Edge

Some AJAX requests or JavaScript functions may not behave as expected due to Edge-specific behaviors or security settings.

<details> <summary><strong>Microsoft Edge – Troubleshooting Guide</strong></summary> <br>
1. Clear Browser Cache

Edge may load outdated JavaScript files.

Press Ctrl + Shift + Delete

Clear Cached images and files and Cookies and site data

Refresh the page

2. Disable Browser Extensions

Extensions (ad blockers, privacy tools, script blockers) can interfere with AJAX requests.

Go to Settings → Extensions

Temporarily disable all extensions

Test the system again

3. Check the Developer Console for Errors

Use the console to identify what’s failing.

Press F12 → open Console

Trigger your search or function

Look for:

JavaScript errors

CORS/CSRF errors

Blocked scripts

Mixed-content warnings

Failed AJAX requests

4. Review the Network Tab

Confirm whether the AJAX request is being blocked.

Press F12 → open Network

Trigger the search

Check for:

Requests marked (blocked)

Status codes 403, 404, 500

CORS or security warnings

5. Ensure JavaScript Is Enabled

Go to Settings → Cookies and site permissions → JavaScript

Set JavaScript to Allowed

6. Adjust Tracking Prevention

Edge’s tracking prevention may block certain requests.

Go to Settings → Privacy, search, and services

Set Tracking prevention to Balanced (or temporarily Off)

7. Use HTTPS

Edge may block AJAX calls if the site uses mixed content (HTTPS page with HTTP requests).

Access the system via https://

Ensure all AJAX endpoints also use https://

8. Try InPrivate Mode

This disables extensions and uses a clean cache environment.

Press Ctrl + Shift + N

Open the system and test again

</details>
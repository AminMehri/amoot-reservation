# Amoot Project

A Simple Reservation System For Doctors And Patients.

## Technologies used in this project:

- Django
- Djangorestframework
- JWT
- Mysql
- Docker

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AminMehri/amoot-reservation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd amoot-reservation
    ```
3. Now run django and postgresql with docker-compose:
    ```bash
    docker-compose up -d --build
    ```
4. Go to the backend container:
  ```bash
  docker exec -it backend-web-1
  ```
5. Migrations and create super user:
   ```bash
   python manage.py makemigrations
   ```

   ```bash
   python manage.py migrate
   ```
   
   ```bash
   python manage.py createsuperuser
   ```
## Usage

Go to http://127.0.0.1:8000/admin/ in your browser


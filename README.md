# Mailing Service

## Description
Mailing Service is a Django-based application that allows users to manage and send email campaigns. It includes features for creating messages, managing recipients, scheduling mailings, and tracking mailing attempts.

## Features
- Create and manage email messages
- Manage email recipients
- Schedule mailings
- Track mailing attempts
- User authentication and authorization

## Installation

### Prerequisites
- Python 3.12
- PostgreSQL
- Redis

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mailing-service.git
    cd mailing-service
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=your_database_host
    DATABASE_PORT=your_database_port
    EMAIL_HOST=your_email_host
    EMAIL_USE_TLS=True
    EMAIL_PORT=your_email_port
    EMAIL_HOST_USER=your_email_user
    EMAIL_HOST_PASSWORD=your_email_password
    ```

4. Apply database migrations:
    ```sh
    poetry run python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    poetry run python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    poetry run python manage.py runserver
    ```

## Usage
1. Access the admin panel at `http://127.0.0.1:8000/admin` and log in with your superuser credentials.
2. Create messages and manage recipients.
3. Schedule mailings and track their status.

## Running Tests
To run tests, use the following command:
```sh
poetry run python manage.py test
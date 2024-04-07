# Task Manager

The task manager project aims to provide a comprehensive solution for managing tasks, epics, sprints, users, and comments within a project environment.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The task manager project facilitates efficient task management by providing a structured framework for organizing tasks, tracking progress, and facilitating communication among team members.

## Features

Key features of the task manager project include:

- Task management: Create, update, and track tasks with details such as title, description, status, due date, and assigned users.
- Epic management: Define epics, which represent larger tasks that can be broken down into smaller sub-tasks.
- Sprint management: Organize tasks into sprints, which are defined time periods for completing specific tasks for deployment review.
- User management: Manage users with roles and permissions, allowing for secure access and collaboration within the system.
- Comment functionality: Add comments to tasks to facilitate communication and collaboration among team members.

## Prerequisites

To set up and run the task manager project, ensure you have the following prerequisites installed:

- Python >= 3.8
- Django >= 4.2.2
- PostgreSQL >= 12.0
- Other dependencies as specified in the project requirements



## Installation

Follow these steps to install and set up the task manager project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/HackersAccount/task_manager.git
   ```

2. Navigate to the project directory:
   ```bash
   cd project_name
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv env
   ```

4. Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source env/bin/activate
     ```
   - On Windows (cmd):
     ```bash
     env\Scripts\activate
     ```

5. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

6. Navigate to the `taskmanager` directory where `manage.py` is located:
   ```bash
   cd taskmanager
   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```

8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Run the development server:
   ```bash
   python manage.py runserver
   ```

10. Access the admin interface:
    ```
    http://127.0.0.1:8000/admin/
    ```


This Markdown format maintains the structure and formatting of the original text while making it suitable for use in Markdown documents or README files.

## Configuration

Configure the task manager project by setting up environment variables and database configuration:

### Environment Variables

Create a `.env` file in the root directory and add the following variables:

```plaintext
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
SECRET_KEY=your_secret_key
DEBUG=True
```

### Database Configuration

Update `settings.py` with the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

## Usage

To use the task manager project, follow these steps:

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

4. Access the admin interface:
   ```
   http://127.0.0.1:8000/admin/
   ```

## Contributing

Contributions to the task manager project are welcome! Follow the guidelines outlined in the CONTRIBUTING.md file to contribute code, report bugs, or suggest features.

## License

The task manager project is licensed under the [MIT License](LICENSE), which allows for free use, modification, and distribution of the software. See the LICENSE file for additional terms and conditions.

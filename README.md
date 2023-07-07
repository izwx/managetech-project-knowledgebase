Software Developmenet Project Knowledge Base Builder
======

The Project Knowledge Base collects and analyzes project-related information from various tools used in software development and builds a database.

If you prefer to view the Project Knowledge Base as a dashboard, use the following repository.

[Managetech Dashboard](https://github.com/izwx/managetech-dashboard). 

# Table of Contents
* [Supported Development Tools](#supported-development-tools)
* [Install](#install)
* [Configuration](#configuration)
* [Usage](#usage)
* [Author](#author)
* [Licenese](#license)

# Supported Development Tools

- Task Management
    - Jira
    - Redmine
    - AzureBoards
    - Backlog
    - Trello
- Document
    - Confluence
- Source Code Control
    - Github
    - Gitlab
- Communication
    - Slack
    - ChatWork


# Install

If you've never used git before, please take a moment to familiarize yourself with [what it is and how it works](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics). To install this project, you'll [need to have git installed and set up](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your local dev environment.

### 1. Install a repo by running the following command.
```sh
$ git clone <link>
``` 
This will create a directory and download the contents of this repo to it.

### 2. Install `Python 3.10.x` and create a virtual environment for the repo. 

### 3. Activate the virtual enviroment and install requirements.
```sh
$ (venv) pip install -r requirements.txt
```


# Configuration

### 1. Clone `.env.example` and rename it to `.env`.

### 2. Input actual values in `.env` to configurate the database settings and install a python package for your DB in the virtual environment. 


# Usage

### 1. Migrate the database.
```sh
$ (venv) python manage.py migrate
```
### 2. Create your first super user.
```sh
$ (venv) python manage.py createsuperuser
```
### 3. Run a Django development server.
```sh
$ (venv) python manage.py runserver
```
### 4. Run Celery worker and beat in other 2 processes. (the virtual environment should be activated in both processes)
```sh
$ (venv) celery -A project worker -l info -P gevent
$ (venv) celery -A project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
### 5. If you do not have experience Django and Django Restframework, visit [here](https://docs.djangoproject.com/en/3.2/) and [here](https://www.django-rest-framework.org/) to check tutorials. 


# Author
 
* Managetech Inc.
* [https://www.managetech.io/](https://www.managetech.io/)
* <info@managetech.io>
 

# License
 
`Project Knowledge Base` is under the terms of the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html).
Please refer to [LICENSE](/LICENSE.md) for the full terms.
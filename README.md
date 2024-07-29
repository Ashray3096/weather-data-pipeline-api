# Weather Data Pipeline API

This project is a weather data pipeline API built with Flask and Flask-RESTx. It provides endpoints for managing and querying weather data and statistics.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Configuration](#configuration)
- [Database Initialization](#database-initialization)
- [Data Ingestion](#data-ingestion)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
```bash
/weather-data-pipeline-api
│
├── /src
│   ├── app.py # Main Flask application file containing API endpoints.
│   ├── init_db.py # Module for establishing connection to the database.
│   ├── models.py # Defines the database schema and ORM models.
│   ├── ingest_data.py # Script for ingesting weather data into the database.
│   ├── weather_statistics.py # Script for calculating weather statistics and storing them in database.
│   └── tests.py # Unit tests for testing the functionality of the application.
|   └── extensions.py
│
├── /wx_data # Directory containing raw weather data files.
│
├── README.md # This file provides an overview of the project, its structure, setup and implementation.
│
└── requirements.txt # List of Python dependencies required for the project.
```

## Features
- Ingest weather data from files.
- Calculate and store weather statistics.
- Provide API endpoints for querying weather data and statistics.
- Swagger documentation for API endpoints.

## Setup

### Prerequisites
- Python 3.7+
- PostgreSQL

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/weather-data-pipeline-api.git
    cd weather-data-pipeline-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
#### Run the init_db.py file:

	python src/init_db.py

#### Run the ingest_data.py file:

	python src/ingest_data.py

#### Run the calculate_statistics.py file:

	python src/calculate_statistics.py

## Configuration
Configuration settings are located in the `config.py` file. Ensure that the `SQLALCHEMY_DATABASE_URI` is correctly set to your PostgreSQL database URL.

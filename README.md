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

## Configuration
Configuration settings are located in the `config.py` file. Ensure that the `SQLALCHEMY_DATABASE_URI` is correctly set to your PostgreSQL database URL.

## Database Initialization
To create the database tables, run the following script:
```bash
python init_db.py

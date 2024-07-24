
## Overview

This is a Flask-based web application designed to manage and evaluate student questions, marks, and records. The application includes functionalities for administrators to log in, manage questions, evaluate students, and view an honor board.


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Pranay75/flask_app.git 
    cd flask_app
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv 
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Rename the `.env.example` to `.env` and update File to your credentials:**
    ```.env
    ADMIN_USERNAME=admin_username
    ADMIN_PASSWORD=admin_password
    SECRET_KEY=your_secret_key
    ```


## Running the application

1. **Run the application:**
    ```bash
    python app.py #before running the app.py make sure you are in virtual environment.
    ```
    Refer [Link](https://code.visualstudio.com/docs/python/environments) to create and use virtual env.


2. **Access the application:** 
   Open your browser and go to `http://127.0.0.1:5000`.

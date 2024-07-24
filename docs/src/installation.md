# Installation

To get started with the Flask Web Application, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/rise-research-labs/honor-board-website
    cd flask_app
    ```

2. **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Rename the `.env.example` to `.env` and update File to your credentials:**
    ```plaintext
    SECRET_KEY=your_secret_key
    ADMIN_USERNAME=admin_username
    ADMIN_PASSWORD=admin_password
    ```
5. **Run the Application:**
    ```bash
    python app.py
    ```

You are now ready to start using the Flask Web Application.

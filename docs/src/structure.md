# Application Structure

The Flask web application is organized into the following structure:

    .
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── .env
    ├── templates/
    │ ├── index.html
    │ ├── login.html
    │ ├── admin_dashboard.html
    │ ├── about.html
    │ ├── edit_questions.html
    │ ├── evaluate_students.html
    │ ├── view_solved.html
    │ ├── view_all_questions.html
    │ └── honor_board.html
    ├── static/
    └──docs

## Description of Each Component

- **`app.py`**: The main application script that contains the Flask app and route definitions.
- **`README.md`**: The file containing project overview and instructions.
- **`requirements.txt`**: Lists the dependencies required to run the application.
- **`.env`**: Environment configuration file that contains sensitive information such as `SECRET_KEY` and admin credentials.
- **`templates/`**: Directory containing HTML templates used by Flask to render views.
  - **`index.html`**: Template for the home page displaying active questions.
  - **`login.html`**: Template for the admin login page.
  - **`admin_dashboard.html`**: Template for the admin dashboard.
  - **`about.html`**: Template for the about page.
  - **`edit_questions.html`**: Template for managing questions.
  - **`evaluate_students.html`**: Template for evaluating student submissions.
  - **`view_solved.html`**: Template for viewing solved questions.
  - **`view_all_questions.html`**: Template for viewing all questions.
  - **`honor_board.html`**: Template for displaying the honor board.
- **`static/`**: Directory for static files such as CSS, JavaScript, and images.
- **`docs/`**: Directory for documentation files in Markdown format, used by `mdBook`.

For more information on how to get started and configure the application, refer to the [Installation](./installation.md) and [Configuration](./configuration.md) sections.

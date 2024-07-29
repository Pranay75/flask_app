## Server set-up

To set-up the server running this web application

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/rise-research-labs/honor-board-website
    cd flask_app
    ```
2. **Run the install.sh:**
    ```bash
    ./install.sh
    ```
    In the installation process you should create admin credentials and use them to login as admin.

3. **Run the run.sh:**
    ```bash
    ./run.sh
    ```
The server get started running on your current IP address.

## Stop the server

1. **Run these commands:**
    ```bash
    sudo systemctl stop nginx
    sudo systemctl stop question-panel-app
    ```
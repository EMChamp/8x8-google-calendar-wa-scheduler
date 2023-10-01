# WhatsApp Calendar Invites Project

This project allows you to schedule Google Calendar invites and send them through WhatsApp as a communication channel.

## Prerequisites

Before you can run this project, make sure you have the following prerequisites installed on your system:

1. **Python**: This project is built using Python. You'll need Python installed on your machine. You can download Python from the [official Python website](https://www.python.org/downloads/).

2. **Python Packages**: Install the necessary Python packages using pip. Open your terminal or command prompt and run the following command:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the required packages listed in the `requirements.txt` file.

3. **Google Calendar API Credentials**: To interact with Google Calendar, you'll need to set up Google API credentials. Follow the instructions in the [Google Calendar Python Quickstart](https://developers.google.com/calendar/quickstart/python) to create and download your API credentials. Save the `credentials.json` file in the project directory.

4. **WhatsApp API Credentials**: You'll need API credentials or tokens for sending messages via WhatsApp. Please refer to the documentation of your chosen WhatsApp API provider to obtain the required credentials.

## Running the Flask Server

To run the Flask server, follow these steps:

1. Make sure you have completed the prerequisite steps, including installing Python packages and setting up API credentials.

2. Open your terminal or command prompt and navigate to the project directory.

3. Run the Flask server with the following command:

   ```bash
   python app.py
   ```

   This will start the Flask server, and you'll see output indicating that the server is running.

4. Open a web browser and access the server at `http://localhost:5000`. You can now use the web interface to schedule Google Calendar invites and send them via WhatsApp.

## Usage

1. Access the web interface by navigating to `http://localhost:5000` in your browser.

2. Follow the on-screen instructions to authenticate with your Google Calendar account.

3. Schedule calendar invites by providing the necessary details, such as event title, date, and time.

4. Select the recipients and configure WhatsApp messaging options.

5. Click the "Schedule Invite" button to create and send the Google Calendar invite via WhatsApp.

## Contributing

Contributions to this project are welcome. If you encounter issues or have suggestions for improvements, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
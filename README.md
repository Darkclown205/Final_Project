# Age Calculator
#### Video Demo:
https://github.com/user-attachments/assets/e37d437e-a299-4e6b-8bad-8b4677568004

## Project Overview
The Age Calculator is a comprehensive web application that offers users a simple yet powerful way to calculate various details based on their birthdate. Developed using Flask for the backend and a combination of Python, HTML, and CSS for the frontend, the application provides a seamless user experience with a clean and intuitive interface. This project goes beyond simple age calculation, offering users a personalized experience with multiple key features.

Upon entering their birthdate, users are instantly provided with:

Exact Age: The app calculates the user's age down to the exact number of years, months, and days, providing a precise and detailed result.
Next Birthday: It shows the time remaining until the user's next birthday, allowing users to anticipate their upcoming special day.
Zodiac Sign: The app automatically determines the user's zodiac sign based on their birthdate, adding a fun and personalized touch.
Special Traits: The app offers insights into the personality traits typically associated with the user's zodiac sign, giving them something unique to learn about themselves.
Birthday Wishes via Email: One of the standout features of this application is the ability to schedule birthday wishes to be sent via email on the user's next birthday. Users can input a message, and the system will automatically send the email to them when the time comes.

## Key Features
- **Age Calculation: The application accurately calculates the user's age based on their birthdate, down to the specific number of days.
- **Next Birthday Countdown: Displays how many days remain until the user's next birthday.
- **Zodiac Sign & Traits: Offers users their zodiac sign along with a brief description of associated personality traits.
- **Email Scheduling: Allows users to schedule a birthday wish to be emailed to themselves on their birthday.
- **User-Friendly Interface**: Provides a simple and intuitive interface for users to interact with the application.

This project was built with simplicity and user experience in mind. Users are greeted with a minimalist interface, allowing them to enter their birthdate and receive all the relevant information in one click. The feature to schedule an email birthday wish adds a unique, personal touch that users will appreciate, particularly as a fun reminder on their birthday.


## Technology Stack
- **Frontend**: HTML, CSS
- **Backend**: Flask (Python)
- **Database: None (Data is managed in-session, but future improvements could include user login and data persistence)
- **Email: The app uses Flask-Mail to handle email scheduling and delivery.


## Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/Darkclown205/Final_Project
2. Navigate to the project directory:
   ```bash
   cd Final_Project
3. Install the required packages:
   ```bash
   pip install -r requirement.txt
4. Run the Flask application:
   ```bash
   flask run
5.Open your browser and navigate to http://127.0.0.1:5000 to use the application.

## Future Improvements
User Accounts: Introduce user registration and login to allow users to save their details and scheduled emails.
Database Integration: Implement a database to store user information, including birthdates and scheduled emails, for persistence.
Improved Email Customization: Allow users to fully customize the email message, design, and schedule.
Expanded Horoscope & Traits: Offer users more detailed zodiac sign readings and daily horoscopes.

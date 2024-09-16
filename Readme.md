# SQLite Flask Template

## Project Description

Form Menia is a web template designed for creating user authentication and profile management systems. It provides a solid foundation built with HTML, CSS, Flask, and SQLite technologies.

## Features

- User Registration
- Login System
- Profile Management
- Secure Authentication
- Responsive Design

## Technologies Used

- HTML: Frontend Templating
- CSS: Styling
- Flask: Python Web Framework
- SQLite: Database Management

## Setup Instructions

1. Clone the repository:
git clone https://github.com/yourusername/form-menia-template.git


2. Install required dependencies:
pip install flask


3. Create a database file named `users.db` in the project root directory.

4. Update the `app.py` file with your database connection details:
python conn = sqlite3.connect('users.db') cursor = conn.cursor()

Rest of your database setup code

5. Customize the HTML templates (`templates/`) to fit your specific needs.

6. Modify the `app.py` file to add routes and functionality as needed.

7. Run the application:
python app.py


   Access the application at `http://127.0.0.1:5000`.

## Usage

- Navigate to `/login` to access the login page.
- Register new users at `/register`.
- View and manage profiles at `/profile`.
- Logout at `/logout`.

## Customization Guide

1. Edit HTML templates in the `templates/` folder to modify layout and content.
2. Update CSS styles in the `static/style.css` file to change appearance.
3. Modify routes and functionality in `app.py`.
4. Adjust database operations in `app.py` to match your specific requirements.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or issues.


# Registration Page with Flask and MongoDB

This is a web application built using Flask and MongoDB. It allows users to register, log in, manage contact details, and search for contacts using a registration number. The application also includes a "Forgot Password" feature that sends a password reset link to the user's email.

## Features

- **User Registration**: Users can create an account by providing a username, email, and password.
- **User Login**: Registered users can log in using their credentials.
- **Forgot Password**: Users can request a password reset link via email.
- **Contact Management**: Users can add and manage contact details (mobile, email, address, and registration number).
- **Search Contacts**: Users can search for contacts using their registration number.

## Technologies Used

- **Flask**: A lightweight Python web framework.
- **MongoDB**: A NoSQL database used to store user and contact data.
- **Flask-Mail**: Used to send password reset emails.
- **Bootstrap**: Used for styling the frontend.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- MongoDB
- Flask (`pip install flask`)
- PyMongo (`pip install pymongo`)
- Flask-Mail (`pip install flask-mail`)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Elelei/Registration-page.git
   cd Registration-page

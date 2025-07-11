## Event Management System

This is a Django-based Event Management System that allows users to create, manage, and RSVP to events. The system includes features for both organizers and participants, with different permissions and views for each user type.

live link: [Event Management System](https://event-management-django-2.onrender.com/)

Admin credentials:

- Username: admin
- Password: 12345

Organizer credentials:

- Username: majharul
- Password: 12345

Participant credentials:

- Username: mi
- Password: 12345

### Features

- User authentication and authorization
- Event creation, updating, and deletion
- RSVP functionality for participants
- Dashboard for organizers to manage events
- Email notifications for important actions

### Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd event-management-django
   ```

3. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```
   python manage.py migrate
   ```

6. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`

### Usage

- Organizers can create and manage events through the dashboard.
- Participants can RSVP to events they are interested in.
- Email notifications are sent for important actions (e.g., RSVP confirmation).

### Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or bug fixes.

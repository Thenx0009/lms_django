# Setup Instructions

1. Clone the Repository
```bash
 git clone https://github.com/Thenx0009/lms_django.git
 cd library_system
 ```

2. Create & Activate Virtual Environment
```bash
python -m venv env
env\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a Superuser
```bash
python manage.py createsuperuser
```
6. Run the Server
```bash
python manage.py runserver
```
7. Access the Admin Panel
```bash
URL: http://127.0.0.1:8000/admin/
```
# LIBRARY MANAGEMENT
`Python 3.12.1` `Django 4.2.6` </br>
A library management system Uuer can login, signup, borrow, search books and returns books in time. Implemented payment gateway system for pay fine.

## Features
- **User Authentication:** User can login, Signup, update user information, recover user account.
- **Book Management:** User can borrow books for 15 days and it's free. 
- **Wish List:** User can add his/her favourite books in his/her wishlist.
- **Fine System:** If book return date is over user must have to paid fine for return book. Per day 5 taka.

## Technologies Used
<a href="https://www.python.org/" title="Python"><img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" width="40px" height="40px"></a>
<a href="https://www.djangoproject.com/" title="Django"><img src="https://github.com/get-icon/geticon/raw/master/icons/django.svg" alt="Django" width="40px" height="40px"></a>
<a href="https://www.w3.org/TR/html5/" title="HTML5"><img src="https://github.com/get-icon/geticon/raw/master/icons/html-5.svg" alt="HTML5" width="40px" height="40px"></a>
<a href="https://getbootstrap.com/" title="Bootstrap"><img src="https://github.com/get-icon/geticon/raw/master/icons/bootstrap.svg" alt="Bootstrap" width="40px" height="40px"></a>

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/AlSaimun/LIBRARY-MANAGEMENT.git
    ```
2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```
3. **Activate the virtual environment:**

    - On Windows:

    ```bash
    .\venv\Scripts\activate
    ```

    - On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```
4. **Install requirements.txt:**

    ```bash
    pip install -r requirements.txt
    ```
5. **Create and Set Up `.env` file:**
    ```
    EMAIL_HOST_USER =  'example@gmail.com'
    EMAIL_HOST_PASSWORD = 'examplepassword'
    ```
    NB: It's for send email to user.
6. **Create account in SSLCOMMERZ Developer site:**
  <a href="https://developer.sslcommerz.com/" target="_blank">`Click here to create an account`</a> </br>
  Now keep store id and password in `.env` as `STORE_ID`, `STORE_PASSWORD` and set up in `transection/ssl.py`.

    ```python
    settings = {'store_id':os.environ.get('STORE_ID'),
    'store_pass': os.environ.get('STORE_PASSWORD'), 'issandbox': True}
    ```
5. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```
    
7. **Open your web browser and go to <a href="http://localhost:8000/" target="_blank">`http://localhost:8000/`</a> to access the application.**

8. **Create a superuser account to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```
Contributions are welcome! If you'd like to contribute to the project :).

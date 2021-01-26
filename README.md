# Django-Plaid-API-Integration
Integrating Plaid

### Description
```bash
Create User -> Make a POST request at /register-user/ with email and password to create new user.

Login -> Make a POST request at /login/ with email and password.Returns a token if login is successful and is_logged_in is set to true.

Logout -> Make a POST request at /logout/ with the token generated at login. is_logged_in is set to false.

Token Exchange -> Make a GET request at /token-exchange/ with email and public_token.Returns access_token if not generated already.

Get Transaction -> Make a GET request a /get-transactions/ with email, start_date and end_date. Returns transactions within given timeperiod.

Get Accounts -> Make a GET request at /get-accounts/ with email.Return user accounts.

Update Transaction (hook) -> Make a POST request at /update-transactions/ with user email and transaction id.Fetches the transaction. Updates user by sending email.
```

## Instructions

### Install Dependencies
```bash
--- pip install -r requirements.txt 
```
(Some dependencies might not be included.Please install it manually.)

### Install RabbitMQ
```bash
--- sudo apt-get install rabbitmq-server (Ubuntu)
```

### Enable and Start RabbitMQ service
```bash
--- systemctl enable rabbitmq-server
--- systemctl start rabbitmq-server
```

### Create and Apply Migrations
```bash
--- python manage.py makemigrations
--- python manage.py migrate
```

### Start Worker Process
```bash
--- celery -A IntegratingPlaid  worker -l info
```

### Run Server
```bash
--- python manage.py runserver
```

### API Endpoints
```bash
--- /register-user/ -> Creating New User
--- /login/  -> Login
--- /logout/ -> Logout
--- /token-exchange/ -> Generating access token
--- /get-transactions/ -> Getting user transactions
--- /get-accounts/ -> Getting user accounts
--- /update-transaction/ -> Updates user by sending email when a POST request is made.(hook)
```

```bash
Celery Broker -> RabbitMQ
Celery Backend -> SQLite
```





# Django-Plaid-API-Integration
Integrating Plaid

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
--- /update-transaction/ -> Return transactions when a POST request is made.(hook)
```

```bash
Celery Broker -> RabbitMQ
Celery Backend -> SQLite
```





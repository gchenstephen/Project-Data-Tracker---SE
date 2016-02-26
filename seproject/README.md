# Project Data Tracker
## Run the development server
First run `python manage.py migrate`, then run
```
python manage.py makemigrations pdt && python manage.py migrate pdt --fake
```
To start the development server, run `python manage.py runserver`, it should be able to reach from `http://127.0.0.1:8000`.

## Create superuser
Run `python manage.py createsuperuser`, admin page is available at `http://127.0.0.1:8000/admin`.

## Acknowledgment
The web UI is based on [Kube](https://imperavi.com/kube/) CSS framework.

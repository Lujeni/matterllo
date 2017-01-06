FROM python:2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements_base.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements_base.txt

COPY . /usr/src/app

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata admin

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

#COPY diploma-frontend diploma-frontend
#COPY diploma-frontend-0.6.tar.gz diploma-frontend-0.6.tar.gz

COPY shop_megano/diploma-frontend/dist/diploma_frontend-0.6.tar.gz diploma_frontend-0.6.tar.gz
RUN pip install diploma-frontend-0.6.tar.gz

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY shop_megano .

CMD ["python", "manage.py", "runserver"]

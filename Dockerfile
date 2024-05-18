FROM python:3.8

# USER app
ENV PYTHONUNBUFFERED 1
# RUN mkdir /db
#RUN chown app:app -R /db

#RUN mkdir /code
#WORKDIR /code
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt
#ADD . /code/
#EXPOSE 8000
#CMD ["python3", "jcvidb/manage.py","runserver"]





#WORKDIR /code
#COPY . .
#RUN pip install -r requirements.txt
#EXPOSE 8000
#CMD ["python3", "jcvidb/manage.py","runserver"]



WORKDIR /app
COPY . /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 8000
#CMD ["python3", "jcvidb/manage.py","makemigrations"]
#CMD ["python3", "jcvidb/manage.py","migrate"]
#CMD ["python3", "jcvidb/manage.py","runserver","0.0.0.0:8000"]


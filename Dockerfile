FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app/
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY main.py  /app/
CMD ["python", "main.py"]

# FROM python:3.7
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 2000
# ENTRYPOINT [ "python" ]
# CMD [ "main.py" ]

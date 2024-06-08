FROM python:3.9-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY templates /usr/local/bin/templates
COPY app_test.py /usr/local/bin/app.py
COPY models.py /usr/local/bin/models.py
COPY forms.py /usr/local/bin/forms.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY migrations /usr/local/bin/migrations
WORKDIR /usr/local/bin
RUN chmod +x entrypoint.sh
# CMD ["python3", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
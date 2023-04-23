FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENTRYPOINT ["python","src/main.py"]
FROM python:3.12

WORKDIR /app
ENV TZ=America/New_York

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY main.py /app/main.py
COPY core/ /app/core/

CMD ["python", "main.py"]
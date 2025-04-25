FROM python:3.13-slim

COPY . /code/

RUN pip install flake8
RUN pip install -r /code/requirements.txt

WORKDIR /code/

CMD ["python3", "-u", "/code/src/component.py"]

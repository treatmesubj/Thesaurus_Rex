FROM python:bullseye

# Install python/pip
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install thesr

RUN mkdir /app

COPY ./flask/ /app

RUN pip install /app/dist/thesr_flask_app-0.0.0-py3-none-any.whl
RUN pip install waitress

EXPOSE 8000

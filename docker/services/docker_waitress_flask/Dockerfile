FROM python:bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y python3 python3-venv && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install thesr

RUN mkdir /app

COPY ./flask/ /app

RUN pip install /app/dist/thesr_flask_app-0.0.0-py3-none-any.whl
RUN pip install waitress

CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8000", "--url-scheme", "https", "thesr_flask_app:app"]

EXPOSE 8000

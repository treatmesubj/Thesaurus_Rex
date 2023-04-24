FROM python:bullseye

COPY ./src/* 

# Install python/pip
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install thesr

EXPOSE 80

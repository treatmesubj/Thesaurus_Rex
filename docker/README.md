# [flask package setup](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
I had to create a new Python venv just for flask because I had wack dependency issues

## Dev
- $ `cd ./flask`
- $ `pip install -e .`
- $ `flask --app thesr_flask_app run -p 8000`

## [Deploy to Prod](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/)
- $ `cd ./flask`
- $ `python setup.py bdist_wheel`
- $ `pip install flaskr-1.0.0-py3-none-any.whl`
- $ `cd ./dist`
- create a fresh new Python venv to `pip install` wheel
    - $ `python -m venv ~/.tmp_flask_venv`
    - $ `source ~/.tmp_flask_venv/bin/activate`
    - $ `pip install flaskr-1.0.0-py3-none-any.whl`

# Docker stuff
1. [Dockerfile](Dockerfile)
2. $ `docker build -t webserv_img .`
3. $ `docker run -itd -p 8000:80 --name webserv webserv_img`


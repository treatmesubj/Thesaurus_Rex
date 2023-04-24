# [flask package setup](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
I had to create a new Python venv just for flask because I had wack dependency issues

## Dev
- $ `cd ./flask`
- $ `pip install -e .`
- $ `flask --app thesr_flask_app run -p 8000`

## [Deploy to Prod](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/)
- create a wheel to distribute because it's the cool way
    - $ `cd ./flask`
    - $ `python setup.py bdist_wheel`
    - $ `cd ./dist`
- create a fresh new Python venv to `pip install` wheel
    - $ `python -m venv ~/.tmp_flask_venv`
    - $ `source ~/.tmp_flask_venv/bin/activate`
    - $ `pip install thesr_flask_app-0.0.0-py3-none-any.whl`
- Deploy on locally [Waitress WSGI server](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)
    - $ `pip install waitress`
    - $ `waitress-serve --host 127.0.0.1 --port 8000 thesr_flask_app:app`

# Docker stuff
- [Dockerfile](Dockerfile)
- clear up stuff
    - $ `docker ps`
    - $ `docker stop <container>`
    - $ `docker system prune --all`
- $ `docker build -t thesr_flask_img .`
- $ `docker run -itd -p 80:8000 --name thesr_flask_app thesr_flask_img`
- check stuff
    - $ `docker exec -it thesr_flask_app bash`


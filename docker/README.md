1. [Dockerfile](Dockerfile)
2. $ `docker build -t webserv_img .`
3. $ `docker run -itd -p 8000:80 --name webserv webserv_img`

# [flask package setup](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
- $ `cd ./flask`
- $ `pip install -e .`
- $ `flask --app thesr_flask_app run -p 8000`

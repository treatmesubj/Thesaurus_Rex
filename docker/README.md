# [flask package setup](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
I had to create a new Python venv just for flask because I had wack dependency issues
- $ `cd ./flask`
- $ `pip install -e .`
- $ `flask --app thesr_flask_app run -p 8000`

# Docker stuff
1. [Dockerfile](Dockerfile)
2. $ `docker build -t webserv_img .`
3. $ `docker run -itd -p 8000:80 --name webserv webserv_img`


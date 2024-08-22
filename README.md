# stocks-visualizer

This is a basic project repository set up by me for my Ambassador AI project.

## Setup Pre-requirements

Three processes are essential for this project to run. Make sure you have them installed already in your system.

1. GNU Make. This comes pre-installed in the standard GNU environment. If not, then the download setup can be found on https://www.gnu.org/software/make/.
2. Docker Engine. This is the container environment, essential for running the application. Can be downloaded at https://www.docker.com/products/docker-desktop/.
3. PostgreSQL database server. This can be downloaded at https://www.postgresql.org/download/.

## Tech Stack

| Backend Framework | Django v5.3         |
| :---------------: | :------------------ |
|   Task-runners    | Celery, Celery-beat |
|     Database      | PostgreSQL v16.3    |
|    Task Broker    | Redis v6.0          |



## Setup Instructions

1. Navigate to the location of your choice on your PC and download the Git repository by following command:

``````bash
https://github.com/buttafraz22/stocks-visualizer
``````

​	This will install the git repository in your current working directory.

2. Change the directory to one level in by the command `cd ./stocksbackend`.

​	At this stage, your directory should look like:

``````bash
---| stocksbackend
------| migrations
------| asgi.py
------| celery.py
------| models.py
------| settings.py
------| urls.py
------| views.py
------| wsgi.py
---| tests
---| worker
------| migrations
------| admin.py
------| apps.py
------| models.py
------| pagination.py
------| serializers.py
------| tasks.py
------| tests.py
------| urls.py
------| views.py
---| compose.yaml
---| Dockerfile
---| manage.py
---| pytest.ini
---| Makefile
---| requirements.txt
``````

3. At the manage.py level, create a `.env` file and populate it with these variables:	*(read this article by me to get a more clear explanation of how this works: https://t.ly/ZchoX)*

``````ini
POSTGRES_USER=<your values>
POSTGRES_PWD=<your values>
POSTGRES_HOST=db	# This is the name of the service in the docker
POSTGRES_PORT=<your values, usually 5432>
POSTGRES_DB=<your values>
BROKER=cache
BROKER_USER=default
BROKER_PWD=password
``````

4. When this is done, in the same terminal window, hit up 

``````cmd
docker-compose up
``````

​	and the services should be up and running.

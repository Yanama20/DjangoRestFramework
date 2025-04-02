FROM python:3.12.2
#don't create pyc files
ENV PYTHONDONTWRITEBYTECODE 1
#do/don't synchronize code with container
ENV PYTHONUNBUFFERED 1

#create container "app" for project
WORKDIR / app

#copy file "requirements.txt" to container "app"
COPY requirements.txt /app/requirements.txt

#install requirements
RUN pip install -r /app/requirements.txt

#copy full project to container "app" (COPY . /app)
COPY . .

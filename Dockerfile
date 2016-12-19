# Using official python runtime base image
FROM python:2.7
MAINTAINER baiyunhui <baiyunhui@juxinli.com>

# Add files to the image
RUN mkdir -p /apps
ADD . /apps
RUN pip install -r /apps/requirements.txt

# Make port 5000 available for links and/or publish
EXPOSE 6752

# Set the application directory
WORKDIR /apps

CMD ["python /apps/todos/main.py"]
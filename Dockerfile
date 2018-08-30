FROM python:3.6
LABEL description="Image with QA app" \
      maintainer="Aleksey Pauls" \
      source="https://github.com/AlekseyPauls/JBInternship/"
RUN apt-get -y update
RUN apt-get install -y python3 python3-pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
CMD ["python", "main.py"]
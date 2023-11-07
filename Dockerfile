# start by pulling the python image
FROM python:3.10-slim

WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt /requirements.txt

# switch working directory
WORKDIR /

ENV RUNPOD_KEY=""

EXPOSE 8501

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY ./ /

# configure the container to run in an executed manner
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "ui.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]
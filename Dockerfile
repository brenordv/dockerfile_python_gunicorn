# Base for this image
FROM python:3.7-slim

# A few labels...
LABEL description="my flask application"
LABEL maintainer="Breno RdV <breno@raccoon.ninja>"

# Enviroment variables...
# docker build --build-arg <arg_name>=<arg_value>

# Source folder
ARG source_folder_app=/app
ENV source_folder=${source_folder_app}

# Target folder (where it the code will be copied.)
ARG target_folder_app=/app
ENV target_folder=${target_folder_app}

# Host
ARG host_addr="0.0.0.0"
ENV host=${host_addr}

# Port
ARG port_num=20042
ENV port=${port_num}

# Number of workers
ARG qty_workers=3
ENV workers=${qty_workers}

# App file
ARG app_file_name="web_isn_batch_add_processo"
ENV app_file=${app_file_name}

# Variable name
ARG app_var_name="app"
ENV app_var=${app_var_name}

# Copies source files
COPY .${source_folder} ${target_folder}

# Copies gunicorn config file. (sample file, slightly modified.)
COPY ./gunicorn_conf.py /gunicorn.conf.py

# Installs stuff...
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install wheel \
    && pip install gunicorn \
    && pip install -r ${target_folder}/requirements.txt 
    
# Finishing up...
WORKDIR ${target_folder}/
ENV PYTHONPATH=${target_folder}
EXPOSE ${port}

# Starts gunicorn
CMD gunicorn --config /gunicorn.conf.py "${app_file}:${app_var}"
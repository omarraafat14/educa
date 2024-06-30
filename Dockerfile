# Pull official base Python Docker image
FROM python:3.12.3

# Set environment variables
# Prevents Python from writing out pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures that the Python stdout and stderr streams are sent straight
# to the terminal without first being buffered.
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /code/
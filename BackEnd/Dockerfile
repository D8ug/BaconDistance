FROM python:3.13.5-slim

# Set workdir
WORKDIR /backend

# Install dependencies
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

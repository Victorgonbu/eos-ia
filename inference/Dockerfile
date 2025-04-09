FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    poppler-utils \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libblas-dev \
    liblapack-dev \
    gfortran \
    git \
    libgl1

COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install fastapi uvicorn httpx

WORKDIR /app
COPY /app /app

# Expose the port for FastAPI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

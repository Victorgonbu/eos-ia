# VLLM and Eos-ia Project

This project is a containerized application that serves a VLLM (Very Large Language Model) and includes a FastAPI application that consumes the VLLM service. 

## Project Structure

```
eos-ia
├── inference
│   ├── app
│   │   ├── main.py          # Entry point for the FastAPI application
│   │   └── __init__.py      # Marks the directory as a Python package
│   ├── Dockerfile            # Dockerfile for building the FastAPI application
│   └── requirements.txt      # Python dependencies for the FastAPI application
├── vllm_server
│   ├── Dockerfile            # Dockerfile for building the VLLM server
│   └── config.json          # Configuration settings for the VLLM server
├── docker-compose.yml        # Docker Compose configuration for the services
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/Victorgonbu/eos-ia.git
   cd eos-ia
   ```

2. **Build the Docker images:**
   ```
   docker-compose build
   ```

3. **Run the services:**
   ```
   docker-compose up
   ```

4. **Access the FastAPI application:**
   Open your browser and navigate to `http://localhost:8000` to access the FastAPI application.

## Usage

- The FastAPI application provides endpoints to interact with the VLLM service. You can find the API documentation at `http://localhost:8000/docs`.

## Notes

- Ensure that Docker and Docker Compose are installed on your machine before running the project.
- Modify the `config.json` file in the `vllm_server` directory to adjust the VLLM server settings as needed.
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    gfortran \
    libgomp1 \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install qiskit qiskit-aer tqdm pyjwt

COPY qwt.py .

EXPOSE 5001

CMD ["python", "qwt.py"]
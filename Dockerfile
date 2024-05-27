
FROM python:3.10.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    llvm \
    clang \
    gcc 


# Run compiler.py when the container launches
ENTRYPOINT ["python3", "compiler.py"] 

FROM python:3.10.12-slim

WORKDIR /app

COPY . /app
RUN mv *.pl /app/src

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    llvm \
    clang \
    gcc 

WORKDIR /app/src
ENV PYTHONPATH /app
# Run compiler.py when the container launches
ENTRYPOINT ["python3", "compiler/compiler.py"]
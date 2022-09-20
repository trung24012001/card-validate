FROM ubuntu

WORKDIR /app/card-validate
COPY . .
RUN apt update && \
  apt -y upgrade && \
  apt install -y python3 python3-pip python3-pyqt5 && \
  pip install -r requirements.txt

VOLUME "~/card-valicate"  "/app/card-valicate" 
EXPOSE 8080
CMD python3 app.py
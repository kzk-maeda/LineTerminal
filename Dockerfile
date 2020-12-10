FROM python:3.8

# ENV LINE_ACCESS_TOKEN=XXX
# ENV LINE_SECRET=XXX

RUN mkdir /app
WORKDIR /app

ADD entrypoint.sh /app/entrypoint.sh
ADD src/ /app
RUN chmod 755 /app/entrypoint.sh 

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
CMD ["/app/entrypoint.sh"]
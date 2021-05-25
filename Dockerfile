FROM python:alpine

RUN python -m pip install requests

COPY tethys_app_status.py /tethys_app_status.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]

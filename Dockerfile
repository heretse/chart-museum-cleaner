FROM python:3.8-slim-buster

ENV USER chart-museum-cleaner
RUN adduser --system --home /chartmuseum-cleaner --disabled-password --group ${USER}

WORKDIR /chart-museum-cleaner

COPY ./requirements.txt /chart-museum-cleaner/requirements.txt
RUN pip3 install -r requirements.txt

COPY chart_museum_cleaner /chart-museum-cleaner/chart_museum_cleaner

USER ${USER}

ENTRYPOINT ["python3" , "-m", "chart_museum_cleaner"]
CMD ["-h"]

FROM python:2.7.14-alpine

LABEL maintainer="Peng Xiao <xiaoquwl@gmail.com>"

RUN apk add --no-cache gcc musl-dev

ADD . /yabgp

WORKDIR /yabgp

RUN pip install -r requirements.txt && python setup.py install

EXPOSE 8801

VOLUME ["~/data"]

ENTRYPOINT ["/usr/local/bin/yabgpd"]

CMD []

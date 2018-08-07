FROM python:3.7-alpine
MAINTAINER Thomas Maschler thomas.maschler@wri.org

ENV NAME area_intersect
ENV USER area_intersect
ENV GEOS http://download.osgeo.org/geos/geos-3.6.2.tar.bz2
ENV PROCESSOR_COUNT grep -c ^processor /proc/cpuinfo


RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev gcc python3-dev musl-dev cython \
    && mkdir -p /usr/src \
    && curl -SL $GEOS \
    | tar -xjC /usr/src

WORKDIR /usr/src/geos-3.6.2


RUN ./configure --enable-python \
    && make \
    && make install
RUN ldconfig /usr/src/geos-3.6.2
RUN geos-config --cflags

RUN addgroup $USER \
    && adduser -s /bin/bash -D -G $USER $USER \
    && easy_install pip \
    && pip install --upgrade pip \
    && pip install virtualenv gunicorn gevent numpy flask-restful \
    && pip install shapely --no-binary shapely \
    && mkdir -p /opt/$NAME \
    && cd /opt/$NAME \
    && virtualenv venv \
    && source venv/bin/activate

COPY requirements.txt /opt/$NAME/requirements.txt
RUN cd /opt/$NAME && pip install -r requirements.txt

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY test.py /opt/$NAME/test.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container
WORKDIR /opt/$NAME

COPY ./$NAME /opt/$NAME/$NAME
COPY ./microservice /opt/$NAME/microservice
RUN chown $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5700
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]





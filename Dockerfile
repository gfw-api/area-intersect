FROM python:3.7-alpine
MAINTAINER Thomas Maschler thomas.maschler@wri.org

ENV NAME area_intersect
ENV USER area_intersect
ENV GEOS http://download.osgeo.org/geos/geos-3.6.3.tar.bz2
ENV PROJ4 http://download.osgeo.org/proj/proj-5.1.0.tar.gz

RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev gcc python3-dev musl-dev \
    && mkdir -p /usr/src \
    && curl -SL $GEOS \
    | tar -xjC /usr/src \
    && curl -SL $PROJ4 \
    | tar -xzC /usr/src

WORKDIR /usr/src/geos-3.6.3
RUN ./configure --enable-python \
    && make \
    && make install
RUN ldconfig /usr/src/geos-3.6.3
RUN geos-config --cflags

WORKDIR /usr/src/proj-5.1.0
RUN ./configure --enable-python \
    && make \
    && make install \
    && export PROJ_DIR=/usr/local/lib/

RUN addgroup $USER \
    && adduser -s /bin/bash -D -G $USER $USER \
    && easy_install pip \
    && pip install --upgrade pip \
    && pip install virtualenv cython gunicorn gevent numpy \
    # pulling pyproj directly from github because of
    # https://github.com/jswhit/pyproj/issues/136
    && pip install git+https://github.com/jswhit/pyproj.git \
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





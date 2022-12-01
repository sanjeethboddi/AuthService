FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN apk update && apk upgrade

RUN apk add --no-cache bash\
                       python3 \
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       python3-dev \
                       gpgme-dev \
                       libc-dev \
                       py3-pip \
    && rm -rf /var/cache/apk/*


RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
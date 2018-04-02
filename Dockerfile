ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache python3
COPY app.py /


# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
CMD [ "python", "./app.py" ]
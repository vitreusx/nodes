openssl req -x509 -newkey rsa:4096 -nodes -out "$1.pem" -keyout "$1_key.pem" -days 365

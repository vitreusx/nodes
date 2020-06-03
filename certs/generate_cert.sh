NAME="$1"
ADDRESS="$2"

CORPORATION=Aurora
GROUP=AururaGroup
CITY=Warsaw
STATE=Warsaw
COUNTRY=PL

# create client private key (used to decrypt the cert we get from the CA)
openssl genrsa -out "$NAME.key"

# create the CSR(Certitificate Signing Request)
openssl \
  req \
  -new \
  -nodes \
  -subj "/CN=$ADDRESS/OU=$GROUP/O=$CORPORATION/L=$CITY/ST=$STATE/C=$COUNTRY" \
  -sha256 \
  -extensions v3_req \
  -reqexts SAN \
  -key "$NAME.key" \
  -out "$NAME.csr" \
  -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=IP:$ADDRESS")) \
  -days 36500

# sign the certificate with the certificate authority
openssl \
  x509 \
  -req \
  -days 36500 \
  -in "$NAME.csr" \
  -signkey "$NAME.key" \
  -out "$NAME.crt" \
  -extfile <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=IP:$ADDRESS")) \
  -extensions SAN \

rm "$NAME.csr"

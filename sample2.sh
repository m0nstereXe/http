# Set your server IP and port
SERVER_IP="127.0.0.1"
SERVER_PORT="8080"

# Variables for storing session cookies
SESSION_COOKIE=""

# Common curl options for HTTP/1.0 and connection close
CURL_OPTIONS="--http1.0 --connect-timeout 5 --max-time 10 --fail --silent"

res=$(curl -i -v -X POST -H "username: Richardd" -H "password: 3TQI8TB39DFIMI6" "http://${SERVER_IP}:${SERVER_PORT}/")
echo "$res"
# CHANNELAPI

ChannelAPI is SocketIO based, secure, server-to-client notification delivery application inspired by microservice architecture. Currently Work In Progress.

## Quickstart

- Generate a token for your client by using an unique identifier that will later use to deliver messages to client.
- Deliver the token to the client that you just created.
- Connect the client with SocketIO v3+ using secure token and create your JS handlers to handle incoming messages.
- Send notification to your client whenever you want and instantly receive them on your client JS end.


## Installation

- Install Python3.6+ and Pip
- Clone the repository
- (Optional) Create virtual environment
- Install requirements from requirements.txt ```pip install -r requirements.txt```
- Run channelapi/main.py with Python ```python channelapi/main.py --debug=true --auth_key=changeme --port=80```
- (Optional) Instead directly running the app, use ```systemd``` or ```supervisord``` to run safer as a service


## Usage
- From your server, get a token from your user with following request ```curl  --request POST 'example.com/channel/c1' --header 'Authorization: s3cur3_t0k3n'```
- You will receive a response like ``` {
    "success": true,
    "token": "Q5NkZvpz7uWptKMvNVUF5qRDSN0Ig7QPBweIH0Q8_Pg"}``` give token to your client
- Connect your client with SocketIO to your domain.
- As soon as you connected, send your token received from server to channel ```join_channel``` with payload like ```{"token":"Q5NkZvpz7uWptKMvNVUF5qRDSN0Ig7QPBweIH0Q8_Pg"}```
- When you get a response ```{"data":"Connected to username"}``` you all set. 
- Create your handlers to listen messages coming from ```message``` channel and handle them.
- Whenever you need, send the necessary notification to your client by invoking a request ```curl --request POST 'example.com/message/username' \
--header 'Authorization: s3cur3_t0k3n' \
--header 'Content-Type: application/json' \
--data-raw '{"message": "hello world"}'```
- You will see this message will be received by client.

## FAQ
##


**Q:** Where is the JavaScript client?

**A:** This is not yet ready. If you need the service simply create your own by following ```Usage``` instructions above.
##

**Q:** How is this secure? Can't anyone just connect any others channel by simply sending their data?

**A:** It's not possible to guess any user's token because it is not tied to their username or any other info. Tokens are randomly generated and unless you leak your token it is not possible(almost) to be guessed or mimicked by an attacker. Rest API end meant to used by server is authentication protected.
##

**Q:** Rest API end authentication protected but how will I get client token without leaking my secure token?

**A:** Rest API end must be invoked by your server. That means from your client you need to send a request to your server, determine users unique name and get token from there without exposing any risk.
##

**Q:** What is the address of this service?

**A:** This application is currently not offered as service. You need to get it running by yourself.
##

**Q:** Why Websocket does not connect?

**A:** This may have different amount of reasons. Be aware that from HTTPS web site you cannot connect to unsecure websocket end(ws). You need to have secure websocket server(wss) which this app does not support even if you have proper SSL certificate. You need to terminate that SSL before reaching out to service with something like Loadbalancer or Nginx.
##


# License
GNU
import json

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
users = []


class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        data = json.loads(self.data)
        print(data)
        # if data["type"]=="login":
        #     msg_to_send = f"{data['username']} has been just joined\n"
        #     # users.append([self, data["msg"]])
        #
        # else:
        #     msg_to_send = f"{data['username']}:{data['msg']}\n"
        msg_to_send = self.__getMessage(data)

        # users.append(
        # print(msg_to_send)
        for client in clients:
            if client != self:
                print('message sent')
                client.sendMessage(msg_to_send)
                print(f"------------{msg_to_send}-----------")

    def handleConnected(self):
        # here we handle when we connect
        print("server is running")
        print(f"{self.address},connected")  # self.address the client address
        clients.append(self)  # reference of the socket that client used
        # to call the address with

    def handleClose(self):
        print(self.address, 'closed')
        clients.remove(self.address)

    def __getMessage(self, data):
        if data["type"] == "login":
            msg_to_send = f"{data['username']} has been just joined\n"
        else:
            msg_to_send = f"{data['username']}:{data['msg']}\n"

        return msg_to_send


    def __generate_id(self):
        users_len= len(users)
        if users_len ==0:
            return 0

        return users[users_len+1]["id"]+1


server = SimpleWebSocketServer('', 8080, ChatServer)
server.serveforever()

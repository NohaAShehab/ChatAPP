import json

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
users = []
onlineusers = []


class ChatServer(WebSocket):

    def handleMessage(self):
        data = json.loads(self.data)
        print(data)
        msg_to_send = self.__getMessage(data)
        for client in clients:
            if client != self:
                print('message sent')
                client.sendMessage(msg_to_send)
                print(f"------------{msg_to_send}-----------")

    def handleConnected(self):
        clients.append(self)  # reference of the socket that client used
        # to call the address with
        print(users)

    def handleClose(self):
        print(self.address, 'closed')
        user_index = self.__getUserIndex()
        users.pop(user_index)
        onlineusers.pop(user_index)
        print(onlineusers)
        print(users)
        clients.remove(self.address)






    def __getMessage(self, data):
        if data["type"] == "login":

            newuser = {
                "id": self.__generate_id(),
                "name": data["username"],
                "client": self
            }
            users.append(newuser)
            onlineusr = {
                "id": self.__generate_id(),
                "name": data["username"],
            }
            onlineusers.append(onlineusr)
            print(users)
            print(onlineusers)
            messages = {
                "body": f"{data['username']} has been just joined\n",
                "online": onlineusers
            }
        elif data["type"] == "left":
            print("heerer")
            messages = {
                "body": f"{data['username']} has been left\n",
                "online": onlineusers
            }
        else:
            messages = {
                "body": f"{data['username']}:{data['msg']}\n",
                "online": onlineusers
            }
        msg_to_send = json.dumps(messages)
        return msg_to_send

    def __generate_id(self):
        users_len = len(users)
        if users_len == 0:
            return 0

        return users[users_len - 1]["id"] + 1


    def __getUserIndex(self):
        for index, user in enumerate(users):
            if user["client"]==self:
                return index

        return None



server = SimpleWebSocketServer('', 7000, ChatServer)
server.serveforever()

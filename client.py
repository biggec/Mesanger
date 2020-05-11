import goto_network
import json
from threading import Thread


ip = '127.0.0.1'
client = goto_network.Client(ip, 9090)
connection = client.connection
name = str(input('Введите Имя: '))
con_things = 0
Commands = []


def send_message():
    while True:
        message = str(input())
        Commands.append({"command": "NEW_MESSAGE",
                         "text": message,
                         "name": name})
        try:
            if message.split(' ')[0] == '/msg':
                Commands.append({"command": "NEW_MESSAGE_TO",
                                 "text": message.split(' ', 2)[2],
                                 "name": name,
                                 "to": message.split(' ')[1]})
                connection.send(json.dumps(Commands[3]))
                Commands.pop(3)
            elif message == 'end':
                connection.send(json.dumps(Commands[0]))
                connection.close()
                break

            else:
                connection.send(json.dumps(Commands[2]))
                Commands.pop(2)
        except:
            pass

    return 0


def recv_message():
    global con_things
    global Commands
    while True:
        try:
            data = connection.receive_string()
            if data != '':
                print(data)
            try:
                if json.loads(data):
                    con_things_ = json.loads(data)[1]
                    Commands.append({"command": "GOODBYE",
                                     "name": name,
                                     "con_things": con_things})
                    Commands.append({"command": "I_AM",
                                     "name": name,
                                     "con_things": con_things_})
                    print(con_things_)
                    connection.send(json.dumps(Commands[1]))
            except:
                pass
        except:
            break
    return 0


Thread(target=send_message).start()
Thread(target=recv_message).start()

import goto_network
import json
from threading import Thread


ip = '194.87.238.112'
client = goto_network.Client(ip, 9090)
connection = client.connection
name = str(input('Введите Имя: '))

Commands = [
    {"command": "I_AM",
     "name": name}]

connection.send(json.dumps(Commands[0]))

con_things = 0

Commands = [
            {"command": "I_AM",
             "name": name}]


def send_message():
    while True:
        message = str(input())
        Commands.append({"command": "NEW_MESSAGE",
                         "text": message,
                         "name": name})

        if message == 'end':
            connection.send(json.dumps(Commands[1]))
            connection.close()
            break

        else:
            connection.send(json.dumps(Commands[2]))
        Commands.pop(2)
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
                    con_things = json.loads(data)[1]
                    print(con_things)
                    Commands.append({"command": "GOODBYE",
                                     "name": name,
                                     "con_things": con_things})
            except:
                pass
        except:
            break
    return 0


Thread(target=send_message).start()
Thread(target=recv_message).start()

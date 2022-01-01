from credentials import *
from TS3Query import TS3Query


def main():
    connection = TS3Query(SERVER_IP, TELNET_PORT)
    print(connection.send('whoami'))

    print('login')
    print(connection.login(TELNET_LOGIN, TELNET_PW))

    print(connection.send('whoami'))
    print(connection.send(f'use port={SERVER_PORT}'))
    print(connection.send('whoami'))

    print('logout')
    print(connection.logout())


if __name__ == '__main__':
    main()

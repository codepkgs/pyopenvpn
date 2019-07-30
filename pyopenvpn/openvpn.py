import sys
import socket
import re


class Openvpn(object):
    """
    use openvpn management interface to get openvpn infor
    """

    def __init__(self, host, port):
        """
        connect openvpn management interface
        :param host: openvpn management interface ip address
        :param port: openvpn management interface port
        """

        timeout = 3

        try:
            address = (host, int(port))
            self._s = socket.create_connection(address, timeout)
        except:
            self.close()
            raise

    @staticmethod
    def sys_version():
        """
        get python verison
        :return:
        """

        if sys.version_info[0] == 2:
            sys_version = 2
        else:
            sys_version = 3
        return sys_version

    def _socket_send(self, command):
        """
        send command to openvpn management interface
        :param command: command
        :return:
        """

        command = command + '\r\n'
        if self.sys_version() == 2:
            self._s.send(command)
        else:
            self._s.send(bytes(command, 'utf-8'))

    def _socket_recv(self, length):
        """
        get recv from command
        :param length: recv length
        :return:
        """

        if self.sys_version == 2:
            return self._s.recv(length)
        else:
            return self._s.recv(length).decode('utf-8')

    @staticmethod
    def _parse_data(data):
        """
        parse recv data
        :param data: recv data
        :return:
        """
        data = data.split('\r\n')
        if data[-1] == 'END':
            return data[:-1]
        elif data[-2] == 'END':
            return data[:-2]
        else:
            return data

    def _send(self, command):
        """
        send command and get recv
        :param command: openvpn management inteface command
        :return:
        """
        data = ''

        self._socket_send(command)

        while True:
            socket_data = self._socket_recv(1024)
            socket_data = re.sub('>INFO(.)*\r\n', '', socket_data)
            data += socket_data
            if data.endswith('\nEND\r\n'):
                break
            elif data.startswith('SUCCESS:'):
                break
            elif data.startswith('ERROR:'):
                break
        return data

    def close(self):
        """
        close socket
        :return:
        """
        self._s.close()

    def version(self):
        """
        get openvpn version
        :return:
        """
        data = self._send('version')
        ret = self._parse_data(data)[0]
        return ret.split()[3]

    def pid(self):
        """
        get openvpn process id
        :return:
        """

        data = self._send('pid')
        ret = self._parse_data(data)[0]
        try:
            pid = ret.split('=')[-1]
        except IndexError:
            pid = None
        return pid

    def clients(self):
        """
        get all online clients
        :return:
        """
        ret = []
        data = self._send('status')
        parse_result = self._parse_data(data)
        if 'ROUTING TABLE' in parse_result:
            flag = 1
        else:
            flag = 2

        if flag == 1:
            routing_table_index = parse_result.index('ROUTING TABLE')
            users = parse_result[3:routing_table_index]
            users_vips = parse_result[routing_table_index + 2:-2]
            if len(users) == 0:
                return ret

            for u in users:
                u_list = u.split(',')
                common_name = u_list[0]
                for v in users_vips:
                    v_list = v.split(',')
                    if common_name in v_list:
                        vip = v_list[0]
                        user = {
                            'common_name': common_name,
                            'remote_ip': u_list[1].split(':')[0],
                            'virtual_ip': vip,
                            'recv_bytes': u_list[2],
                            'send_bytes': u_list[3],
                            'login_time': u_list[-1]
                        }

                        ret.append(user)
                        break
                    else:
                        continue

            return ret

        if flag == 2:
            client_lists = [c for c in parse_result if c.startswith('CLIENT_LIST')]

            if len(client_lists) == 0:
                return ret

            for c in client_lists:
                c_list = c.split(',')
                user = {
                    'common_name': c_list[1],
                    'remote_ip': c_list[2].split(':')[0],
                    'virtual_ip': c_list[3],
                    'recv_bytes': c_list[5],
                    'send_bytes': c_list[6],
                    'login_time': c_list[7]
                }

                ret.append(user)
            return ret

    def kill(self, common_name):
        command = 'kill {}'.format(common_name)
        data = self._send(command)
        parse_data = self._parse_data(data)
        if parse_data[0].startswith('SUCCESS'):
            return True
        else:
            return False


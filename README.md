# Backdoor and Listener

This repository contains Python scripts for a basic backdoor and listener. 

**Disclaimer:**

* This code is for educational purposes only. 
* Creating and using backdoors without proper authorization is illegal and unethical. 
* The developer is not responsible for any misuse of this tool.

**Features:**

* **Backdoor:** 
    * Establishes persistence on the target system.
    * Executes system commands.
    * Downloads and uploads files.
    * Changes the working directory.
* **Listener:**
    * Listens for incoming connections.
    * Sends and receives commands to/from the backdoor.
    * Provides a basic command-line interface for interaction.

**Usage:**

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```

2. **Navigate to the repository:**
   ```bash
   cd <repository_name>
   ```

3. **Compile the Backdoor script (using PyInstaller):**
   ```bash
   pyinstaller --onefile Backdoor.py 
   ```
   This will create a single executable file (e.g., `dist/Backdoor`) in the `dist` directory.

4. **Transfer the compiled executable to the target system.**

5. **Run the executable on the target system.**

6. **Start the Listener:**
   ```bash
   python Listener.py 
   ```
   Replace `"10.0.2.4"` and `8080` with the actual IP address and port you want to use.

**Note**: While replacing the ip and port in listener code also replace it in the backdoor code

8. **Interact with the backdoor using the Listener:**
   * Use the following commands in the Listener terminal:
      * `cd <path>`: Change the working directory on the target system.
      * `download <file_path>`: Download a file from the target system.
      * `upload <file_path> <file_content>`: Upload a file to the target system.
      * `<command>`: Execute any system command on the target system.
      * `exit`: Close the connection and exit the Listener.

**Note:**

* This is a simplified example and may have security vulnerabilities. 
* It is crucial to understand and comply with all applicable laws and regulations regarding computer security and ethical hacking.
* This code is provided for educational purposes only and should not be used for any malicious activities.

**Disclaimer:**

This tool is for educational and ethical purposes only. The developer is not responsible for any misuse of this tool. Using this tool for illegal activities is strictly prohibited.

This README provides a comprehensive description of the backdoor and listener, including how to clone the repository, compile the backdoor, and use the tools. It also includes important disclaimers and emphasizes the ethical considerations of using such tools.

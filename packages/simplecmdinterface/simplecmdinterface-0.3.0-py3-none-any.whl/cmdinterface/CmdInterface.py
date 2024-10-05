import subprocess
class CmdInterface:
    def __init__(self,nude=True,rm_boilerplate=True,end_signal="cmd_end_command_signal_rand_string_extension_to_avoid_matching_with_user_command",log_mode=False):
        
        self.end_command_signal=end_signal
        self.nude=nude
        self.process = subprocess.Popen("cmd", stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        self.lock=False
        self.command_count=0
        self.log_mode=log_mode
        self.log=[]



        if rm_boilerplate==True:
            #just an empty first command to clear the boiler plate for the next ones, this is not added in the command count #TODO MAKE SOMETHING THAT DOESNT INJECT A NEW COMMAND
            self.send_command("@echo.")


    def __del__(self):
        # Clean up
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait()

    def kill(self):
        # Clean up
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait()

    def send_command(self,command):

        #print(command)
        
        #multithreading prevention
        while True:
            if self.lock==False:
                break
        self.lock=True
        self.command_count+=1

        
        # Define a unique signal to indicate the end of a command's output
        end_command_signal = self.end_command_signal
        extension=f"&& echo {end_command_signal}"
        command_with_signal = f"{command} {extension}\n"
        #print(command_with_signal)
        self.process.stdin.write(command_with_signal)
       
        self.process.stdin.flush()
        #print("ok")

        # Read output until the end signal is detected
        output = []
        cnt=0
        while True:
            line = self.process.stdout.readline()
            if end_command_signal in line:
                cnt+=1
            if cnt==2:
                break  # Stop reading after detecting the end signal
            if self.nude==True:
                output.append(line.replace(extension,""))
            else:
                output.append(line)
        if self.log_mode==True:
            self.log+=output
        self.lock=False
        #print(output)
        return output
    

    def get_log(self):
        return self.log.copy()
    
    def turn_on_logging(self):
        self.log_mode=True

    def turn_off_logging(self):
        self.log_mode=False

    def get_command_count(self):
        return int(self.command_count)
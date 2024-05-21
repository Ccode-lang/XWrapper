import subprocess
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static, Header
from textual.worker import get_current_worker
from textual import events
import signal
import os
from time import sleep
import socket

botp = None

class XWUI(App):
    num = 0
    text = None
    buffer = ""
    loop = None

    clientSocket = None

    def print(self, string):
        self.buffer += string
        self.call_from_thread(self.text.update, self.buffer)
    
    def print2(self, string):
        self.buffer += string
        self.text.update(self.buffer)
    
    def on_mount(self) -> None:
        self.text = self.query_one(Static)
        loop = self.run_worker(self.main_loop, thread=True, exclusive=True)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.settimeout(1.0)
        pass

    async def on_input_changed(self, message: Input.Changed) -> None:
        pass
    
    def main_loop(self) -> None:
        for line in self.run_bot():
            pass
        self.exit_bot()
        
    def exit_bot(self):
        for line in iter(botp.stdout.readline, ""):
            self.print(line + "\n")
        botp.stdout.close()
        ret_code = botp.wait()
        if ret_code:
            self.print(f"Return code: {ret_code}\n")
        self.clientSocket.close()
        self.print("Bot ended.\n")
        self.print("Ending in 10 seconds\n")
        sleep(10)
        self.exit()

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            inp = self.query_one(Input).value
            if inp == "exit":
                os.kill(botp.pid, signal.CTRL_C_EVENT)
            elif inp == "ping":
                self.clientSocket.sendto("ping".encode(), ("127.0.0.1", 5036))
            self.query_one(Input).value = ""
        
    
    def run_bot(self):
        global botp
        global ended_normal
        try:
            botp = subprocess.Popen(["python", "-u", "bot.py"], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)
            for line in iter(botp.stdout.readline, ""):
                self.print(line + "\n")
                yield line
        except:
            pass

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="output")
        yield Input(placeholder="Enter commands here")

app = XWUI()

# This is why python sucks. Just stop with the weird error handling
s = signal.signal(signal.SIGINT, signal.SIG_IGN)
app.run()
signal.signal(signal.SIGINT, s)
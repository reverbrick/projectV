class mpy():

    def __init__(self, sock):
        self.sock = sock

    def enter_raw_repl(self, soft_reset=True):
        try:
            self.sock.write(b"\r\x03\x03")  # ctrl-C twice: interrupt any running program

            # flush input (without relying on serial.flushInput())
            n = self.sock.inWaiting()
            while n > 0:
                self.sock.read(n)
                n = self.sock.inWaiting()

            self.sock.write(b"\r\x01")  # ctrl-A: enter raw REPL

            if soft_reset:
                data = self.read_until(1, b"raw REPL; CTRL-B to exit\r\n>")
                if not data.endswith(b"raw REPL; CTRL-B to exit\r\n>"):
                    print(data)
                    raise CommsError("could not enter raw repl")

                self.sock.write(b"\x04")  # ctrl-D: soft reset

                # Waiting for "soft reboot" independently to "raw REPL" (done below)
                # allows boot.py to print, which will show up after "soft reboot"
                # and before "raw REPL".
                data = self.read_until(1, b"soft reboot\r\n")
                if not data.endswith(b"soft reboot\r\n"):
                    print(data)
                    raise CommsError("could not enter raw repl")

            data = self.read_until(1, b"raw REPL; CTRL-B to exit\r\n")
            if not data.endswith(b"raw REPL; CTRL-B to exit\r\n"):
                print(data)
                raise CommsError("could not enter raw repl")

            self.in_raw_repl = True
        except CommsError:
            print("comms error")

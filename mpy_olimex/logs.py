import picoweb
import network
import machine
import sys
import ulogging as logging
import time

net = network.LAN()
net.active(True)
net.ifconfig(('192.168.125.89', '255.255.255.0', '192.168.125.1', '8.8.8.8'))
log = []
log.append("Net address: %s"%str(net.ifconfig()))

app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("%s"%log[0])
    yield from resp.awrite(b"""\
<br>
<form action='/restart'>
    <button> Restart Olimex </button>
</form>
<form action='/poweroff'>
    <button> Shutdown program </button>
</form>
<form action='/ledon'>
    <button> Led ON </button>
</form>
<form action='/ledoff'>
    <button> Led OFF </button>
</form>
""")

@app.route("/restart")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:
        req.parse_qs()
    machine.reset()

@app.route("/poweroff")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:
        req.parse_qs()
    sys.exit()

@app.route("/ledon")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:
        req.parse_qs()
    for x in range(50):
        pyb.LED(1).on()
    	time.sleep(0.1)
    	pyb.LED(1).off()
        time.sleep(0.1)

@app.route("/ledoff")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:
        req.parse_qs()
    pyb.LED(1).off()

logging.basicConfig(level=logging.INFO)
app.run(debug=True, host="192.168.125.89")

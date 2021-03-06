import uasyncio as asyncio

def print_http_headers(url):
    reader, writer = yield from asyncio.open_connection(url, 80)
    print("================")
    query = "GET / HTTP/1.0\r\n\r\n"
    yield from writer.awrite(query.encode('latin-1'))
    while True:
        line = yield from reader.readline()
        if not line:
            break
        if line:
            print(line.rstrip())

url = "192.168.125.112"
loop = asyncio.get_event_loop()
#task = asyncio.async(print_http_headers(url))
#loop.run_until_complete(task)
loop.run_until_complete(print_http_headers(url))
loop.close()

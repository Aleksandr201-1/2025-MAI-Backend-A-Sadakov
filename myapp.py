from pass_gen import generate_password

def app(environ, start_response):
    data = b"Hello, world!\n\n"
    data += b"Generated passwords:\n"
    for i in range(5):
        tstr = f"{i+1}.{generate_password()}\n"
        data += tstr.encode('UTF-8')
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
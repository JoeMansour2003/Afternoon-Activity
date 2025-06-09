import socket
print(socket.gethostname())
if socket.gethostname() in ["Joes-MacBook-Air.local", "Joes-MacBook-Air-2.local"]:
    from camp_t.local_settings import *
else:
    from camp_t.production_settings import *
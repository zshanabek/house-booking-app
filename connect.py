import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")


token = "64346f05509d5bcc4a0c7672626fd2ee1334593a"
# token = "ece27aa267d077b65336e90d8b09f376c82741bb"
host = "localhost:8000"
# host = "akv-technopark.herokuapp.com:5864211"
url = "ws://{}/ws?token={}".format(host, token)
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

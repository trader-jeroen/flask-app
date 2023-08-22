from flask import Flask, render_template
from pybit.unified_trading import WebSocket
from collections import deque
from threading import Thread
from time import sleep

app = Flask(__name__)

# Keep track of the last 60 seconds of data
data_queue = deque(maxlen=60)

# Bybit WebSocket
def handle_message(message):
    global data_queue

    for trade in message["data"]:
        data_queue.append({
            'symbol': trade['s'],
            'last_price': trade['p'],
            'volume': trade['v'],
        })

def bybit_websocket():
    ws = WebSocket(testnet=True, channel_type="linear")
    ws.trade_stream(symbol="BTCUSDT", callback=handle_message)

    while True:
        sleep(1)

@app.route('/')
def index():
    return render_template('volume.html', data=list(data_queue))

if __name__ == '__main__':
    t = Thread(target=bybit_websocket)
    t.start()
    app.run(debug=True)

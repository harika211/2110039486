from flask import Flask, jsonify,requests, render_template 
import time
from collections import deque
from utils import fetch_number

app = Flask(__name__)

WINDOW_SIZE = 10
stored_numbers = deque(maxlen=WINDOW_SIZE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    prev_state = list(stored_numbers)
    start_time = time.time()
    numbers = fetch_number(numberid)
    response_time = time.time() - start_time

    if response_time > 0.5 or numbers is None:
        return jsonify({
            "windowPrevState": prev_state,
            "windowCurrState": list(stored_numbers),
            "numbers": [],
            "avg": calculate_average(stored_numbers)
        }), 200

    for num in numbers:
        if num not in stored_numbers:
            stored_numbers.append(num)
    
    curr_state = list(stored_numbers)
    avg = calculate_average(stored_numbers)

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": numbers,
        "avg": avg
    }), 200

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return round(sum(numbers) / len(numbers), 2)

if __name__ == '__main__':
    app.run(port=9876)

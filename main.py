import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, redirect, url_for, jsonify, session, request, g
import Adafruit_DHT
import secret


class Door():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.OUT)
        GPIO.output(26, GPIO.LOW)
        self.temp_sensor = Adafruit_DHT.DHT11
        self.temp_pin = 4
        self.humidity = 0
        self.temperature = 0
        self.door_open = False
        self.door_is_open_message = "<br><br>Door is currently OPEN <br><br> click to close!<br><br><br>", "door_opened"
        self.door_is_closed_message = "<br><br><br>Door is currently CLOSED<br><br>", "door_closed"

    def close_door(self):
        self.update_door_status()
        print(":door_open: ", self.door_open)
        if self.door_open == 1:
            print("Door already closed")
            return "Door already closed"

        print('closing door\n')
        GPIO.output(26, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(26, GPIO.LOW)
        print('closed door\n')

        return "Closing door..."

    def get_door_status(self):
        self.update_door_status()
        if not self.door_open:
            return self.door_is_open_message
        return self.door_is_closed_message

    def update_door_status(self):
        self.door_open = GPIO.input(25)
        print("DOOR STATUS: ", self.door_open)

    def update_temperature_status(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.temp_sensor, self.temp_pin)
        if not humidity:
            humidity = "NO RESPONSE FROM SENSOR"
        if not temperature:
            temperature = "NO RESPONSE FROM SENSOR"
        self.humidity = int(humidity)
        self.temperature = int((int(temperature) * 1.8) + 32)
        print("TEMP STATUS: ", humidity, temperature)




app = Flask(__name__)
app.secret_key = secret.secret_key
door = Door()


@app.before_request
def before_request_func():
    print("before_request executing!")
    g.user = None
    if "logged_in" in session:
        g.user = session["logged_in"]

    if not g.user and request.endpoint not in ['check_password', 'submit_password']:
        return redirect(url_for('check_password'))
    elif g.user and request.endpoint == 'check_password':
        return redirect(url_for('index'))

@app.route("/")
def index():
    door_status, door_color = door.get_door_status()
    return render_template('home.html', button_text=door_status, button_color=door_color)

@app.route("/close/")
def call_close():
    print("close door called in Flask")
    door.close_door()
    return redirect(url_for('index'))


@app.route("/open/")
def call_open():
    return redirect(url_for('index'))

@app.route("/get_door_status/")
def get_door_status():
    door_status, door_color = door.get_door_status()
    return jsonify({"door_status": door_status, "door_color": door_color})

@app.route("/get_temperature_status/")
def get_temperate_status():
    door.update_temperature_status()
    return jsonify({"temperature": door.temperature, "humidity": door.humidity})

@app.route("/need_password")
def check_password():
    return render_template('password.html')

@app.route("/submit_password", methods=["POST"])
def submit_password():
    password = request.form["password"]

    # Validate the password (replace with your own password validation logic)
    if password == secret.password:
        session["logged_in"] = True
        return redirect(url_for("index"))
    else:
        return render_template('password.html', bad_password="Incorrect Password")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    # GPIO.cleanup()
    print('GPIO cleanup complete!\n')

#hello from Tim@@


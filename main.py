import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, redirect, url_for, jsonify
import Adafruit_DHT


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
        self.humidity = humidity
        self.temperature = temperature
        print("TEMP STATUS: ", humidity, temperature)




app = Flask(__name__)
door = Door()


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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    # GPIO.cleanup()
    print('GPIO cleanup complete!\n')

#hello from Tim@@


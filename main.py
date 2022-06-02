import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, redirect, url_for


class Door():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.OUT)
        GPIO.output(26, GPIO.LOW)
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


app = Flask(__name__)
door = Door()


@app.route("/")
def index():
    door_status, door_color = door.get_door_status()
    return render_template('home.html', button_text=door_status, button_color=door_color)

@app.route("/close/")
def call_close():
    door.close_door()
    return redirect(url_for('index'))


@app.route("/open/")
def call_open():
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    # GPIO.cleanup()
    print('GPIO cleanup complete!\n')

#hello from Tim@@


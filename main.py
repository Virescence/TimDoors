import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, redirect, url_for


class Door():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(26, GPIO.OUT)

    def __init__(self):
        self.door_open = True
        self.door_is_open_message = "<br><br>Door is currently OPEN <br><br> click to close!<br><br><br>", "door_opened"
        self.door_is_closed_message = "<br><br>Door is currently CLOSED <br><br> click to open!<br><br><br>", "door_closed"

    def open_door(self):
        if self.door_open:
            return "Door was already open!"
        # call code to open door
        print('opening door\n')
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(26, GPIO.LOW)
        print('door opened\n')

        return "Opening door..."

    def close_door(self):
        if not self.door_open:
            return "Door was already closed!"
        # call code to close door
        print('closing door\n')
        GPIO.output(26, GPIO.LOW)
        time.sleep(2)
        GPIO.output(26, GPIO.HIGH)
        print('closed door\n')

        return "Closing door..."

    def get_door_status(self):
        if self.door_open:
            self.door_open = False
            return self.door_is_open_message
        self.door_open = True
        return self.door_is_closed_message

    def update_door_status(self):
        # call code to get status of door
        # self.door_open = (GPIO.input(25))
        self.door_open = not self.door_open
        # self.door_open = not self.door_open


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
    door.open_door()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    # GPIO.cleanup()
    print('GPIO cleanup complete!\n')


# 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

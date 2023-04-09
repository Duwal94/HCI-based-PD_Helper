import subprocess
import serial
import serial.tools.list_ports
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import time
import os 

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
serialInst = serial.Serial('COM3', 9600, timeout=1)

def getSerialOutput():
    while True:
        if serialInst.in_waiting:
            packet = serialInst.readline().decode('utf-8').rstrip()
            serial_data = list(map(float, packet.split(' ')))
            data = {
            "temperature": serial_data[0],
            "humidity": serial_data[1],
            "PPM": serial_data[2]
            }
            return data



def blink_led(pin):
    serialInst.write(bytes(str(pin), 'utf-8'))
    time.sleep(1)
    

@app.get("/")
def index(request: Request):
    data = getSerialOutput()
    return templates.TemplateResponse("index.html", {"request": request, "temperature": data['temperature'], "humidity": data['humidity'], "PPM": data['PPM'],})
    

@app.post("/run")
async def run_file():
    subprocess.run(['python', 'C:/Users/riyesh/OneDrive/Desktop/gaze_controlled_keyboard_p10/gaze_controlled_keyboard_p10.py'])
    return {"message": "File ran successfully."}

@app.post("/run1")
async def run_file1():
    subprocess.run(['python', 'C:/Users/riyesh/OneDrive/Desktop/gaze_controlled_keyboard_p10/voiceacct.py'])
    return {"message": "File ran successfully."}

@app.post("/blink_led_2")
async def blink_led_2_endpoint(request: Request):
    blink_led('f')
    data = getSerialOutput()
    return templates.TemplateResponse("index.html", {"request": request, "message": "AC is On!","temperature": data['temperature'], "humidity": data['humidity'], "PPM": data['PPM']})

@app.post("/blink_led_3")
async def blink_led_3_endpoint(request: Request):
    blink_led('a')
    data = getSerialOutput()
    return templates.TemplateResponse("index.html", {"request": request, "message": "Fan is On","temperature": data['temperature'], "humidity": data['humidity'], "PPM": data['PPM']})

@app.post("/blink_led_4")
async def blink_led_4_endpoint(request: Request):
    blink_led('l')
    data = getSerialOutput()
    return templates.TemplateResponse("index.html", {"request": request, "message": "Lights are ON!","temperature": data['temperature'], "humidity": data['humidity'], "PPM": data['PPM']})

if __name__ == '__main__':
     import uvicorn
     uvicorn.run(app, host="127.0.0.1", port=8000)
     
    





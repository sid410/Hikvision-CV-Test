# Hikvision-CV-Test
Testing opencv algos on Hikvision cam

### Run the virtual environment
```
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Setup the environment variables
- Create .env file
- Provide the following camera info:
```
CAM_USER=
CAM_PASS=
CAM_IP=
```

### Test opencv Algorithms
First connect to the wifi router the camera is connected, then run

```
py .\cvTest.py
```
Press `1` to change between grayscale and background subtraction

Press `q` to exit

---
### Accessing the Camera GUI
To access the cam GUI and configuration settings, read the part about how to enable IE mode in Edge from this [link](https://windowsreport.com/your-browser-not-supported-hikvision/)

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
```
py .\cvTest.py
```
Press `1` to change between grayscale and background subtraction

Press `q` to exit

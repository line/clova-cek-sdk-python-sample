# Clova Example Extension

This is a simple Clova Extention to demonstrate how to use the Clova Extension SDK for python. Have a look at `home-extension.py` to see how the CEK SDK can be used.
For this example the Custom Extension in the Clova-Developers Center has been setup with the following custom Intends.
`TurnOn`, `TurnOff`, `HomeStatus`, `PlayASound`  
The `TurnOn` and `TurnOff` Intents can have Custom Slots with the names `Light` or `AirConditioner`.


## Documentation

* [Clova Platform Guide](https://clova-developers.line.me/guide/)
* [Clova Extension Python SDK](https://line.github.io/clova-cek-sdk-python/)

## How to Setup Environment
#### Install pip:
```
sudo easy_install pip
```

#### Install Flask:
```
pip install Flask
```

#### Install CEK SDK:
```
pip install clova-cek-sdk
```

#### Run Flask server:
```
FLASK_APP=home-extension.py python3 -m flask run --host=0.0.0.0
```

## How to manually Test
You can run the Flask server locally and use `curl` to test if the server works.

#### POST
```
curl -H "Content-Type: application/json" -X POST -d @"./test/data/example_request.txt" http://localhost:5000/app
```

#### GET
```
curl -X GET http://localhost:5000/
```

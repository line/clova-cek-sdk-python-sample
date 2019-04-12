#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, request, jsonify
import cek
import logging

app = Flask(__name__)

# Create a separate logger for this application
logger = logging.getLogger('home_clova_extension')

# Set the default language, currently 'en', 'ja' and 'ko' are supported
# Turn on the debug mode only for development.
# Debug_mode will turn off validation of application_id
# and request verification
clova = cek.Clova(
    application_id="my.application.id", default_language="en", debug_mode=True)


class HomeState(object):
    def __init__(self):
        self.is_aircon_on = False
        self.is_light_on = False
        self.currentTemperature = 30
        self.refrigerator = ["beer", "sausage"]


# In this example we use a dictionary with keys as user_ids
# to keep track of the home states of different users
user_home_state = dict()


@app.route('/app', methods=['POST'])
def my_service():

    # Forward the request to the Clova Request Handler
    # Just pass in the binary request body and the request header
    # as a dictionary
    body_dict = clova.route(body=request.data, header=request.headers)

    response = jsonify(body_dict)
    # make sure we have correct Content-Type that CEK expects
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response


@clova.handle.launch
def launch_request_handler(clova_request):

    # You can answer in different languages within one response
    welcome_japanese = cek.Message(message="ようこそ!", language="ja")
    welcome_korean = cek.Message(message="환영!", language="ko")

    response = clova.response([
        "Welcome~~!", welcome_japanese, welcome_korean, "How can i help you?"
    ])
    return response


@clova.handle.intent("HomeStatus")
def home_status_handler(clova_request):

    home_state = user_home_state.get(clova_request.context.user.id, HomeState())
    if home_state.is_aircon_on:
        aircon_state = "Air conditioner is turned on. "
    else:
        aircon_state = "Air conditioner is turned off. "

    if home_state.is_light_on:
        light_state = "Light is turned on. "
    else:
        light_state = "Light is turned off. "

    temperature = "Current room temperature is about {} degrees. ".format(
        home_state.currentTemperature)
    refrigerator = "Your refrigerator contains {}. ".format(" and ".join(
        home_state.refrigerator))
    message = aircon_state + light_state + temperature + refrigerator

    message_set = cek.MessageSet(
        brief="Home is in good condition!", verbose=message)
    response = clova.response(message_set)
    return response


@clova.handle.intent("PlayASound")
def play_a_sound_handler(clova_request):
    # To play an audio file provide an url
    sound_url = cek.URL("http://soundbible.com/grab.php?id=2215&type=mp3")
    response = clova.response(["This is for all dogs in the home.", sound_url])
    return response


@clova.handle.intent("TurnOn")
def turn_on_handler(clova_request):
    user_id = clova_request.context.user.id
    slots = clova_request.slots
    home_state = user_home_state.get(user_id, HomeState())
    device_name = None
    if 'Light' in slots:
        device_name = 'Light'
        home_state.is_light_on = True
    if 'AirConditioner' in slots:
        device_name = 'AirConditioner'
        home_state.is_aircon_on = True
        home_state.currentTemperature = 20

    user_home_state[user_id] = home_state
    if not device_name:
        return clova.response(
            "Sorry, I could not understand. What do you want to turn on?")
    else:
        response_text = "{} turned on.".format(device_name)
        logger.info(response_text)
        response = clova.response(
            message=response_text,
            reprompt="Do you want to switch on something else?")
        return response


@clova.handle.intent("TurnOff")
def turn_off_handler(clova_request):
    user_id = clova_request.context.user.id
    slots = clova_request.slots
    home_state = user_home_state.get(user_id, HomeState())
    device_name = None
    if 'Light' in slots:
        device_name = 'Light'
        home_state.is_light_on = False
    if 'AirConditioner' in slots:
        device_name = 'Air Conditioner'
        home_state.is_aircon_on = False
        home_state.currentTemperature = 30

    user_home_state[user_id] = home_state
    if not device_name:
        return clova.response(
            "Sorry, I could not understand. What do you want to turn off?")
    else:
        response_text = "{} turned off.".format(device_name)
        logger.info(response_text)
        return clova.response(response_text)


# Handles Build in Intents
@clova.handle.intent("Clova.GuideIntent")
def guide_intent(clova_request):
    attributes = clova_request.session.attributes

    # The session_attributes in the current response will become
    # the session_attributes in the next request
    message = ("I can switch things on and off."
               "I can give you a status of your home and "
               "I can play dog music to entertain your pets!")
    if 'HasExplainedService' in attributes:
        message = "I just explained you what i can do!"

    response = clova.response(message)
    response.session_attributes = {'HasExplainedService': True}
    return response


@clova.handle.intent("Clova.CancelIntent")
def cancel_intent(clova_request):
    logger.info("User canceled the Service.")


@clova.handle.intent("Clova.YesIntent")
def yes_intent(clova_request):
    return clova.response("Yes, yes it is.")


@clova.handle.intent("Clova.NoIntent")
def no_intent(clova_request):
    return clova.response("No... Ok I understand.")


@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    logger.info("Session ended.")


# In case not all intents have been implemented
# the handler falls back to the default handler
@clova.handle.default
def default_handler(request):
    return clova.response("Sorry I don't understand! Could you please repeat?")

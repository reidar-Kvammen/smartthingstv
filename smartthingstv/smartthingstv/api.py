#Smartthings TV integration#
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json
import os
API_BASEURL = "https://api.smartthings.com/v1"
API_DEVICES = API_BASEURL + "/devices/"
COMMAND_POWER_OFF = "{'commands': [{'component': 'main','capability': 'switch','command': 'off'}]}"
COMMAND_REFRESH = "{'commands':[{'component': 'main','capability': 'refresh','command': 'refresh'}]}"
COMMAND_PAUSE = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'pause'}]}"
COMMAND_MUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'mute'}]}"
COMMAND_UNMUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'unmute'}]}"
COMMAND_PLAY = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'play'}]}"
COMMAND_STOP = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'stop'}]}"
COMMAND_REWIND = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'rewind'}]}"
COMMAND_FAST_FORWARD = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'fastForward'}]}"

class smartthingstv:

  def __init__(self):
      self._state = "off"
      self._name = name
      self._muted = False
      self._volume = 10
      self._api_key = api_key
      self._device_id = device_id
  def __exit__(self, type, value, traceback):
      self.close()


  def device_update(self):
      API_KEY = self._api_key
      REQUEST_HEADERS = {"Authorization": "Bearer " + API_KEY}
      DEVICE_ID = self._device_id
      API_DEVICE = API_DEVICES + DEVICE_ID
      API_DEVICE_STATUS = API_DEVICE + "/states"
      API_COMMAND = API_DEVICE + "/commands"
      cmdurl = requests.post(API_COMMAND,data=COMMAND_REFRESH ,headers=REQUEST_HEADERS)
      resp = requests.get(API_DEVICE_STATUS,headers=REQUEST_HEADERS)
      data = resp.json()
      device_volume = data['main']['volume']['value']
      device_state = data['main']['switch']['value']
      device_source = data['main']['inputSource']['value']
      device_all_sources = data['main']['supportedInputSources']['value']
      device_tv_chan = data['main']['tvChannel']['value']
      device_tv_chan_name = data['main']['tvChannelName']['value']
      device_muted = data['main']['mute']['value'] 
      self._state = device_state
      self._volume = device_volume
      self._source_list = device_all_sources
      if device_muted == "mute":
         self._muted = True
      else:
         self._muted = False
      if device_tv_chan_name == "":
         self._source = device_source
      else:
         self._source = device_tv_chan_name
      self._channel = device_tv_chan
      self._channel_name = device_tv_chan_name

  def send_command(self, command, cmdtype):
      API_KEY = self._api_key
      REQUEST_HEADERS = {"Authorization": "Bearer " + API_KEY}
      DEVICE_ID = self._device_id
      API_DEVICES = API_BASEURL + "/devices/"
      API_DEVICE = API_DEVICES + DEVICE_ID
      API_COMMAND = API_DEVICE + "/commands"

      if cmdtype == "setvolume": # sets volume
         API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'setVolume','arguments': "
         API_COMMAND_ARG  = "[{}]}}]}}".format(command)
         API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
         cmdurl = requests.post(API_COMMAND,data=API_FULL ,headers=REQUEST_HEADERS)
      elif cmdtype == "stepvolume": # steps volume up or down
         if command == "up":
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeUp'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
         else:
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeDown'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
      elif cmdtype == "audiomute": # mutes audio
         if self._muted == False:
            cmdurl = requests.post(API_COMMAND,data=COMMAND_MUTE ,headers=REQUEST_HEADERS)
         else:
            cmdurl = requests.post(API_COMMAND,data=COMMAND_UNMUTE ,headers=REQUEST_HEADERS)
      elif cmdtype == "switch": # turns off
         cmdurl = requests.post(API_COMMAND,data=COMMAND_POWER_OFF ,headers=REQUEST_HEADERS)
      elif cmdtype == "selectsource": #changes source
         API_COMMAND_DATA =  "{'commands':[{'component': 'main','capability': 'mediaInputSource','command': 'setInputSource', 'arguments': "
         API_COMMAND_ARG  = "['{}']}}]}}".format(command)
         API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
         cmdurl = requests.post(API_COMMAND,data=API_FULL ,headers=REQUEST_HEADERS)


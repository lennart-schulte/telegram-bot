#!/usr/bin/python3

### Ideas ###
# weather from local weather station
# a not-yet-existent todo list from a web interface
# user authentication


import requests
import time

# TODO logging
class TelegramBot:
    def __init__(self, apiKeyFilename="APIKEY", currentUpdateIdFilename="CURRENTUPDATEID"):
        self.baseUrl = self.__getBaseUrl(apiKeyFilename)
        if self.baseUrl == None:
            raise FileNotFoundError("No API key found")
        getMe = self.getMe()
        if getMe['ok'] == False:
            raise RuntimeError("API key does not work", getMe)

        self.currentUpdateIdFilename = currentUpdateIdFilename
        content = self.__readFile(currentUpdateIdFilename)
        if content == None or content == '':
            print("File {} does not exist, using current update_id 0".format(currentUpdateIdFilename))
            self.currentUpdateId = 0
        else:
            print("Update ID: {}".format(content))
            self.currentUpdateId = int(content)

    def __getBaseUrl(self, apiKeyFilename):
        apiKey = self.__readFile(apiKeyFilename)
        if apiKey == None:
            return None
        return "https://api.telegram.org/bot{}/".format(apiKey)

    def __readFile(self, filename):
        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def __writeFile(self, filename, content, mode="w+"):
        with open(filename, mode) as f:
            f.write(str(content))

    def getMe(self):
        return self.__get("getMe")

    def getUpdates(self):
        return self.__get("getUpdates")

    def __get(self, method):
        url = "{}{}".format(self.baseUrl, method)
        r = requests.get(url)
        return r.json()

    def handleUpdates(self):
        updates = self.getUpdates()
        if not 'result' in updates:
            print("No updates found:", updates)
            return
        # TODO error handling
        for update in updates['result']:
            update_id = int(update['update_id'])

            if update_id <= self.currentUpdateId:
                continue
            self.currentUpdateId = update_id
            self.__writeFile(self.currentUpdateIdFilename, update_id)

            message = update['message']
            text = message['text']
            chat_id = message['chat']['id']
            first_name = message['chat']['first_name']

            text_response = None
            if text == "/ping":
                text_response = "Pong!"

            if text_response == None:
                print("Message from {}: '{}' .. sending no response".format(first_name, text))
                continue
            print("Message from {}: '{}' .. sending '{}'".format(first_name, text, text_response))
            self.sendMessage(chat_id, text_response)
            # TODO error handling

    def sendMessage(self, chat_id, text):
        payload = {'chat_id': chat_id, 'text': text}
        return self.__send("sendMessage", payload)

    def __send(self, method, payload):
        url = "{}{}".format(self.baseUrl, method)
        return requests.post(url, payload)


t = TelegramBot()
try:
    while True:
        t.handleUpdates()
        time.sleep(1)
except KeyboardInterrupt:
    print('Shutting down')


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .utils import check_weather
from rasa_sdk.events import ReminderScheduled, FollowupAction
import datetime
import time, threading

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ActionCheckWeather(Action):
   def name(self) -> Text:
      return "action_check_weather"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      dispatcher.utter_message("Hello World! from custom action")
      return []

class ActionCheckWeather_1(Action):
   def name(self) -> Text:
      return "action_external"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      dispatcher.utter_message("External Action")
      return []

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = ''
        weather = ''
        temp = ''
        entities=tracker.latest_message['entities']
        for ent in entities:
            print(ent['value'])
            city = ent['value']
            temper, weather = check_weather(ent['value'])
            print(temper, weather)
            temp=int(temper['temp']-273)
            print(temp)
        #dispatcher.utter_message("utter_temp",
        #   tracker,temp=temp)
        dispatcher.utter_message(text = f" {weather} in {city.title()}. Today's temperature is {temp} degree Celcius.")
        return []

class ActionCloud(Action):

    def name(self) -> Text:
        return "action_climate_api"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city_entity = tracker.latest_message['entities']
        print(city_entity[0]['value'])
        e = city_entity[0]['value']
        """for entity in city_entity:
            print(f'entity is {entity["value"]}')
            print(entity['value'])
            temp=int(check_weather(entity['value'])['temp']-273)
        #dispatcher.utter_message("utter_temp",
        #   tracker,temp=temp)"""
        #dispatcher.utter_message(text = f'Today"s temperature is {temp} degree Celcius.')
        temp=int(check_weather(e)['temp']-273)
        dispatcher.utter_message(text = f'Today"s temperature {temp} degree Celcius.')
        return []

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("Entered ACTION SET REMINDER")
        dispatcher.utter_message("I will remind you in 5 seconds.")
        entities = tracker.latest_message.get("entities")
        date = datetime.datetime.now() + datetime.timedelta(seconds=5)

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )
        #threading.Timer(10, ActionSetReminder.run).start()
        return [reminder]


class ActionReactToReminder(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        #name = next(tracker.get_slot("person"), "someone")
        dispatcher.utter_message(text= f"Remember to call!")
        asr_obj = ActionSetReminder()
        #asr_obj.name()
        #asr_obj.run(dispatcher, tracker, domain)
        return [FollowupAction('action_set_reminder')]




    
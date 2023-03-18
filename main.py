import json
import os.path
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers import MDDatePicker

# Размер окна для запуска на ПК. Перед созданием APK файла, удалить или закомментировать.
from kivy.core.window import Window
Window.size = (1080/3, 2160/3)


class MyScreenManager(ScreenManager):
    pass


class Menu(Screen):
    pass


class Setting(Screen):
    pass


class Day(Screen):
    pass


class MainApp(MDApp):
    settings = {
        "fuel_consumption_per_100_km": "Не настроено"
    }
    day = {
        "date": "Дата",
        "start": "",
        "stop": "",
        "total": " ",
        "route": " ",
        "fuel_consumed": "Не настроено",
        "fueling_in_liters": "0",
        "fueling_in_rubles": "0",
        "fuel_card_balance": "Не задано..."
    }

    if not os.path.isfile("./settings.json"):
        with open("./settings.json", "w") as file:
            json.dump(settings, file, indent=4)
    else:
        with open("./settings.json", "r") as file:
            settings = json.load(file)

    if not os.path.isfile("./day.json"):
        with open("./day.json", "w") as file:
            json.dump(day, file, indent=4)
    else:
        with open("./day.json", "r") as file:
            day = json.load(file)

    def pick_date(self, *args):
        date = ".".join(reversed(str(args[1]).split("-")))
        self.root.ids.date.text = date
        self.day["date"] = date
        self.update_day_json()

    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.pick_date)
        date_picker.open()

    def update_settings_json(self):
        with open("./settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def update_day_json(self):
        with open("./day.json", "w") as file:
            json.dump(self.day, file, indent=4)

    def calculation_and_update_total(self, **kwargs):
        self.day |= kwargs.items()

        if (
            self.day["start"] and
            self.day["stop"] and
            int(self.day["start"]) < int(self.day["stop"])
        ):
            self.day["total"] = str(
                int(self.day["stop"]) - int(self.day["start"]))
            self.root.ids.total.text = self.day["total"]
        else:
            self.day["total"] = " "
            self.root.ids.total.text = self.day["total"]

        self.update_day_json()

    def calculation_and_update_fuel_consumed(self):
        if self.settings["fuel_consumption_per_100_km"] == "Не настроено":
            self.day["fuel_consumed"] = "Не настроено"
            self.root.ids.fuel_consumed.text = self.day["fuel_consumed"]
        else:
            if self.day["total"] == " ":
                self.day["fuel_consumed"] = "0"
                self.root.ids.fuel_consumed.text = self.day["fuel_consumed"]
            else:
                fuel_consumed = str(
                    int(self.day["total"]) *
                    int(self.settings["fuel_consumption_per_100_km"]) /
                    100
                )
                self.day["fuel_consumed"] = fuel_consumed
                self.root.ids.fuel_consumed.text = self.day["fuel_consumed"]

    def update_fueling(self, id, text):
        if text:
            self.day[id] = str(int(self.day[id]) + int(text))
            self.root.ids[id].text = self.day[id]
            if id == "fueling_in_rubles":
                self.calculation_fuel_card_balance(text)
            self.update_day_json()
        else:
            self.root.ids[id].text = self.day[id]

    def update_route(self, *args):
        self.day["route"] = " ".join(args)
        self.update_day_json()

    def setting_fuel_consumption_per_100_km(self, text):
        if text:
            self.settings["fuel_consumption_per_100_km"] = str(text)
            self.update_settings_json()
        else:
            self.root.ids.fuel_consumption_per_100_km.text = self.settings[
                "fuel_consumption_per_100_km"
            ]

    def setting_fuel_card_balance(self, text):
        if text:
            self.day["fuel_card_balance"] = str(text)
            self.root.ids.settings_fuel_card_balance.text = self.day["fuel_card_balance"]
            self.root.ids.fuel_card_balance.text = self.day["fuel_card_balance"]
            self.update_day_json()
        else:
            self.root.ids.settings_fuel_card_balance.text = self.day["fuel_card_balance"]
            self.root.ids.fuel_card_balance.text = self.day["fuel_card_balance"]

    def calculation_fuel_card_balance(self, last_fueling):
        if self.day["fuel_card_balance"] == "Не задано...":
            pass
        else:
            fuel_card_balance = str(
                int(self.day["fuel_card_balance"]) -
                int(last_fueling)
            )
            self.update_fuel_card_balance(fuel_card_balance)

    def update_fuel_card_balance(self, text):
        self.day["fuel_card_balance"] = str(text)
        self.root.ids.fuel_card_balance.text = self.day["fuel_card_balance"]
        self.root.ids.settings_fuel_card_balance.text = self.day["fuel_card_balance"]
        self.update_day_json()

    def unfocus_route_input(self, text):
        if text:
            if text[-1] == "\n":
                self.root.ids.route.text = text[:-1]
                self.root.ids.route.focus = False


if __name__ == "__main__":
    MainApp().run()

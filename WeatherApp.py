import sys
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.enter_city_name_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):


        self.setWindowTitle("WEATHER APP")


        vbox = QVBoxLayout()
        vbox.addWidget(self.enter_city_name_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)


        self.enter_city_name_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.enter_city_name_label.setObjectName("enter_city_name_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Bonheur Royale;
                }
            QLabel#enter_city_name_label{
                font-style: Bonheur Royale;
                font-size: 30px;
                font-weight: bold;
                }
            QLineEdit#city_input{
                font-size: 40px;
                }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
                }
            QLabel#temperature_label{
                font-size: 75px;
                }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
                }
            QLabel#description_label{
                font-size: 100px;
                }
        """)


        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key = "a9db46f7600a360c940705bb020fca4a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as HTTPError:
            match response.status_code:
                case 400 :
                    self.display_error("Bad Requests:\nPlease Check Your Input")
                case 401:
                    self.display_error("Unauthorised:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess Is Denied")
                case 404:
                    self.display_error("Not Found:\nCIty Not Found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease Try Again")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid Response From Server")
                case 503:
                    self.display_error("Service Unavailable:\nServer Is Down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo Response From Server")
                case _:
                    self.display_error(f"HTTPError Occurred:\n{HTTPError}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\ncCheck Your Internet Connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe Request Timed Out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck The Url")
        except requests.exceptions.RequestException as ReqError:
            self.display_error(f"Requests Error:\n{ReqError}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)

        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        self.description_label.setStyleSheet("font-size:45px;")

        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15

        weather_description = data["weather"][0]["description"]

        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.display_emoji(weather_id))


    @staticmethod
    def display_emoji(weather_id):

        if 200 <= weather_id <= 232 :
            return "⛈️"
        if 300 <= weather_id <= 321 :
            return "🌦️"
        if 500 <= weather_id <= 531 :
            return "🌧️"
        if 600 <= weather_id <= 622 :
            return "❄️"
        if 701 <= weather_id <= 741 :
            return "🌫️"
        if 801 <= weather_id <= 804 :
            return "️☁️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        else :
            return ""


def  main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

main()

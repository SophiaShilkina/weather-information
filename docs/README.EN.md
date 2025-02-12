# weather-information

### [Russian README](https://github.com/SophiaShilkina/weather-information/blob/master/docs/README.md)

## Description

An HTTP server providing weather information using an asynchronous framework.
Data is obtained from the Open-Meteo API: https://open-meteo.com/

## Dependencies

The project uses the following libraries:

- `fastapi` for creating an async;
- `httpx` for making asynchronous HTTP reques;
- `uvicorn` as an ASGI server to run;
- `APScheduler` for ex;
- `pydantic` for data validation an;
- `SQLAlchemy` for database interactions.

## Methods

### GET /coordinates

**Description:**  
This method takes coordinates and returns temperature, wind speed, and at

**Request Parameters:**
- `latitude` (float, required): Latitude in the range from -90 to 90.
- `longitude` (float, required): Longitude in the range from -180 to 180.

**Return Value:**  
Returns data in JSON format containing temperature, wind speed, and atmospheric pressure 
information.

**Example Request:**

`curl "http://127.0.0.1:8000/coordinates?latitude=55.7558&longitude=37.6173"`

---

### POST /registration

**Description:**  
This method is used for user registration. It takes a username and returns a unique 
identifier (ID) for the new user. Each user can have their own list of cities and 
corresponding weather forecasts.

**Request Parameters:**
- `username` (string, required): The username.

**Return Value:**  
Returns a JSON response with the new user’s ID or the ID of an already registered user 
with the same `username`.

**Usage Conditions:**  
All string input data sent in the request must be in English and case-sensitive. The 
values must be unique.

**Example Request:**

`curl -X POST "http://127.0.0.1:8000/registration" -H "Content-Type: application/json" 
-d "{\"username\": \"Examiner\"}"`

---

### POST /cities/{usid}

**Description:**  
This method takes a city name and its coordinates and adds it to the list of cities being 
tracked for weather forecasts for a specific user. The server stores and updates the 
daily weather forecast for the specified cities every 15 minutes.

**Path Parameters:**
- `usid` (integer, required): The user ID for whom the city is being added.

**Request Parameters:**
- `city` (string, required): The city name.
- `latitude` (float, required): Latitude in the range from -90 to 90.
- `longitude` (float, required): Longitude in the range from -180 to 180.

**Usage Conditions:**  
All string input data sent in the request must be in English and case-sensitive.

**Example Request:**

`curl -X POST "http://127.0.0.1:8000/cities/1" -H "Content-Type: application/json" -d 
"{\"city\": \"Moscow\", \"latitude\": 55.4507, \"longitude\": 37.3659}"`

---

### GET /forecast/{usid}

**Description:**  
This method returns a list of cities for which weather forecasts are available for a 
specific user.

**Path Parameters:**
- `usid` (integer, required): The user ID for whom the city list is returned.

**Return Value:**  
Returns a list containing information about cities for which weather forecasts are 
available to the user.

**Example Request:**

`curl "http://127.0.0.1:8000/forecast/1"`

---

### GET /currentweather/{usid}

**Description:**  
This method takes a city name and a time and returns the weather for that city at the 
specified time on the current day for a specific user. It allows selecting which 
weather parameters to include in the response: temperature, humidity, wind speed, 
and precipitation.

**Path Parameters:**
- `usid` (integer, required): The user ID for whom the weather is returned.

**Request Parameters:**
- `city` (string, required): The city name.
- `time_w` (string, required): Time in the format HH:MM.
- `temperature` (boolean, optional): Include temperature in the response. Pass true to enable.
- `humidity` (boolean, optional): Include humidity in the response. Pass true to enable.
- `wind_speed` (boolean, optional): Include wind speed in the response. Pass true to enable.
- `precipitation` (boolean, optional): Include precipitation information in the response. Pass true to enable.

**Return Value:**  
Returns a JSON response with the requested weather parameters.

**Usage Conditions:**  
All string input data sent in the request must be in English and case-sensitive. 
Unneeded parameters do not require false values.

**Example Request:**

`curl "http://127.0.0.1:8000/currentweather/1?city=Moscow&time_w=14:00&temperature=true&humidity=true"`

## Installation and Running

1. Navigate to the desired directory and clone the repository:
   ```bash
   git clone https://github.com/SophiaShilkina/weather-information.git
   ```
   
2. Install dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```
   
3. Run the application:
   ```bash
   python app.py
   ```
   The server will be available at: http://127.0.0.1:8000

### Contribution

If you want to contribute to the project, please create a branch with your changes and open a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contact

If you have questions or collaboration proposals, you can contact me on Telegram:
[Sophia](https://t.me/ShilkinaSK).

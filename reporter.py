import requests
import json
import csv

def city_input():
    while True:
        user_city = input("What city do you want to see weather data for? ").strip().lower()
        if user_city == "":
            print(f"\nYou must type in a city name...")
            continue
        else:
            return user_city

def get_data(user_city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    parameters = {
        "q": user_city,
        "appid": "ec963f126d39c2f1da5f047ced732c0e"
    }
    try:
        print("Grabbing Data...")
        res = requests.get(base_url, params = parameters)
        res.raise_for_status
    except requests.exceptions.HTTPError:
        print(f"Unable to process request. Check the name of {user_city} or the key within the program.")
    except requests.exceptions.ConnectionError:
        print(f"Unable to connect to server. Check the URL within this program or wait and try again.")
    try:
        response = json.loads(res.text)
    except json.JSONDecodeError:
        print("Not Valid JSON Data")
    return response

def reformat_data(dictonary):
    new_dictonary = {}
    new_dictonary['city'] = dictonary.get("name")
    new_dictonary['country code'] = (dictonary.get("sys", {}).get("country"))
    new_dictonary['temp'] = (dictonary.get("main", {}).get("temp"))
    new_dictonary['humidity'] = (dictonary.get("main", {}).get("humidity"))
    new_dictonary['description'] = dictonary["weather"][0]["description"]
    print(f"In {new_dictonary['city']} CC: {new_dictonary['country code']} its {new_dictonary['temp']} Celsius at a humidity of {new_dictonary['humidity']} it is also {new_dictonary['description']}")
    return new_dictonary

def add_csv_data(dictonary):
    output_file = 'city_data.csv'
    fieldnames = ['city', 'country code', 'temp', 'humidity', 'description']
    data = [dictonary]
    try:
        with open(output_file, mode= 'a', newline= '') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writerows(data)
        print(f"Data written to {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}")

def read_csv_data(file):
    count = 0
    try:
        with open(file, mode='r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                count += 1
                city = row['city']
                country_code = row['country code']
                temp = row['temp']
                print(f"In {city} CC: {country_code} with a temp of {temp}C.")
            print(f"There is {count} cities in this CSV")
    except FileNotFoundError:
        print("File is not found")
    except ValueError:
        print("Failed to convert data")

if __name__ == "__main__":
    reformat_data(get_data(city_input))
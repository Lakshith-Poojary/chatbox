import requests

def check_weather(city): 
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    url = api_address + city 
    json_data = requests.get(url).json() 
    format_add = json_data['main'] 
    weather = json_data['weather'][-1]['main']
    #print(format_add) 
    return format_add, weather
#print(check_weather("mysore"))
#x = check_weather("mysore")[0]['temp']
#print(x)
'''
def Weather(city): 
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='

    url = api_address + city 
    json_data = requests.get(url).json() 
    print(json_data)
    format_add = json_data['main'] 
    return format_add
print(Weather('Mumbai'))'''
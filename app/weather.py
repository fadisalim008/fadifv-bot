import requests

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"

        r = requests.get(url).json()

        current = r["current_condition"][0]

        temp = current["temp_C"]
        feel = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        desc = current["weatherDesc"][0]["value"]

        return f"""
الطقس في {city}

الحرارة: {temp}°C
الاحساس: {feel}°C
الحالة: {desc}
الرطوبة: {humidity}%
الرياح: {wind} km/h
"""

    except:
        return "ماكدرت اجيب الطقس"

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
import re
from apscheduler.schedulers.background import BackgroundScheduler  

app = Flask(__name__)
app.secret_key = 'supersecretkey'  
scheduler = BackgroundScheduler()
scheduler.start()

birthday_wishes_store = {}

def is_valid(birthdate: str):
    regex = r"^([a-z]{3,9})\s([0-2]?[0-9]|3[0-1]),\s?([0-9]{4})$"
    if matches := re.search(regex, birthdate, re.IGNORECASE):
        return matches.group(1), matches.group(2), matches.group(3)
    else:
        raise ValueError("Invalid Date Format.")

def month_to_integer(month: str):
    months = {
        "fullname": {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        },
        "abbreviated_name": {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sept": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        },
    }
    if month in months["fullname"]:
        return months["fullname"][month]
    elif month in months["abbreviated_name"]:
        return months["abbreviated_name"][month]
    else:
        raise ValueError("Month not found.")

def calculate_age(birthmonth: str, birthday: int, birthyear: int, today):
    total_age = (today.year - birthyear)
    if month_to_integer(birthmonth) > today.month:
        total_age -= 1
    elif month_to_integer(birthmonth) == today.month:
        if birthday > today.day:
            total_age -= 1
    return total_age

def calculate_days(birthmonth: str, birthday: int, today):
    year_birthday = date(today.year, month_to_integer(birthmonth), birthday)
    if year_birthday < today:
        year_birthday = year_birthday.replace(year=today.year + 1)
    time_to_birthday = abs(year_birthday - today)
    return time_to_birthday.days

def zodiac_sign(month: int, day: int):
    signs = {
        (1, 20): "Aquarius", (2, 19): "Pisces",
        (3, 21): "Aries", (4, 20): "Taurus",
        (5, 21): "Gemini", (6, 21): "Cancer",
        (7, 23): "Leo", (8, 23): "Virgo",
        (9, 23): "Libra", (10, 23): "Scorpio",
        (11, 22): "Sagittarius", (12, 22): "Capricorn"
    }
    for (start_month, start_day), sign in signs.items():
        if (month > start_month) or (month == start_month and day >= start_day):
            current_sign = sign
        else:
            return current_sign
    return "Capricorn"

def chinese_zodiac(year: int):
    zodiacs = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
    return zodiacs[year % 12]

def time_until_next_birthday(birthmonth: str, birthday: int, today):
    year_birthday = date(today.year, month_to_integer(birthmonth), birthday)
    if year_birthday < today:
        year_birthday = year_birthday.replace(year=today.year + 1)
    delta = year_birthday - today

    days = delta.days
    total_seconds = delta.total_seconds()
    hours = total_seconds // 3600
    return days, int(hours)


def personalized_message(age: int, zodiac: str) -> str:
    messages = {
        "Aquarius": "Aquarians are original and independent thinkers! Enjoy your creative journey at age {}.",
        "Pisces": "Pisces are compassionate and artistic souls! At age {}, may your empathy guide you!",
        "Aries": "Bold and ambitious, Aries charge ahead. You are unstoppable at age {}!",
        "Taurus": "Stable and reliable, Taurus! At age {}, may your grounded nature bring success.",
        "Gemini": "Gemini, with your curious and adaptable nature, age {} is a time for exploration and learning!",
        "Cancer": "Nurturing and intuitive Cancer, may age {} bring emotional growth and fulfillment.",
        "Leo": "Leo, your confidence and charisma shine brightly! Embrace the spotlight at age {}.",
        "Virgo": "Detail-oriented Virgo, age {} is perfect for achieving your meticulous goals and improvements.",
        "Libra": "Libra, seek balance and harmony in age {}. Your diplomacy will lead to wonderful outcomes.",
        "Scorpio": "Intense and passionate Scorpio, age {} will be transformative and empowering for you.",
        "Sagittarius": "Adventurous Sagittarius, age {} is an opportunity for new experiences and exciting journeys.",
        "Capricorn": "Ambitious Capricorn, your dedication at age {} will pave the way for remarkable achievements."
    }
    return messages.get(zodiac, "Have a fantastic year ahead!").format(age)

# Schedule a birthday wish to be printed at a specific time
def schedule_birthday_wish(user_email, message, birthmonth, birthday):
    today = date.today()
    next_birthday = date(today.year, month_to_integer(birthmonth), birthday)
    if next_birthday < today:
        next_birthday = date(today.year + 1, month_to_integer(birthmonth), birthday)

    # Schedule task for midnight of the next birthday
    scheduler.add_job(func=send_birthday_wish, trigger="date", run_date=next_birthday, args=[user_email, message])

def send_birthday_wish(user_email, message):
    # Placeholder for sending email (integrate with actual email service)
    print(f"Sending birthday wish to {user_email}: {message}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        birthdate = request.form["birthdate"].lower()
        birthday_wish = request.form.get("birthday_wish", "")
        user_email = request.form.get("email", "")
        try:
            birthmonth, birthday, birthyear = is_valid(birthdate)
            today = date.today()
            age = calculate_age(birthmonth, int(birthday), int(birthyear), today)
            days = calculate_days(birthmonth, int(birthday), today)
            sign = zodiac_sign(month_to_integer(birthmonth), int(birthday))
            chinese_zodiac_sign = chinese_zodiac(int(birthyear))
            days_until_birthday, hours_until_birthday = time_until_next_birthday(birthmonth, int(birthday), today)
            personalized_birthday_message = personalized_message(age, sign)
            today_formatted = today.strftime("%A, %B %d, %Y")

            if birthday_wish and user_email:
                # Schedule birthday wish
                schedule_birthday_wish(user_email, birthday_wish, birthmonth, int(birthday))
                flash("Your birthday wish has been scheduled!")

            return render_template("index.html", age=age, days=days, sign=sign, chinese_zodiac_sign=chinese_zodiac_sign, days_until_birthday=days_until_birthday, hours_until_birthday=hours_until_birthday, personalized_birthday_message=personalized_birthday_message, today_formatted=today_formatted)

        except ValueError as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

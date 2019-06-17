from bot.helpers           import is_even
from bot.helpers.subject   import StudentSubject
from bot.helpers.constants import WEEKDAYS
from bot.helpers.constants import MONTHS

from datetime import datetime
from datetime import timedelta


def beautify_classes(json_response, next, edited_subjects):
    weekly_schedule = []
    
    today = datetime.today() + timedelta(days=7 if next else 0)
    todays_weekday = today.isoweekday()
    
    for weekday in WEEKDAYS:
        date = today + timedelta(days=weekday - todays_weekday)  # Date of each day
        
        subjects_list = []
        
        # Adding appropriate edited classes to schedule
        for subject in edited_subjects:
            if subject.weekday == weekday and subject.is_even == (not is_even() if next else is_even()):
                subjects_list.append((subject.begin_hour, subject))

        if str(weekday) in json_response:
            # Removing extraspaces
            json_response[str(weekday)] = [ {
                    key: " ".join(value.split()) for key, value in subject.items()
                } for subject in json_response[str(weekday)]
            ]
            
            for subject in json_response[str(weekday)]:
                # No subjects - no schedule. For day-offs
                if "День консультаций" in subject["disciplName"] or "Военная подготовка" in subject["disciplName"]: break
                
                # Do not show subjects on even weeks when they are supposed to be on odd weeks if that's not asked
                if subject["dayDate"] == "неч" if (not is_even() if next else is_even()) else subject["dayDate"] == "чет": continue
                
                # Do not show subjects with certain dates (21.09) on other dates (28 сентября)
                day_month = "{}.{}".format(int(date.strftime("%d")), date.strftime("%m"))
                if "." in subject["dayDate"] and day_month not in subject["dayDate"]: continue

                studentSubject = StudentSubject()

                studentSubject.time = subject["dayTime"]
                
                # Do not show subject if there is its edited alternative
                if studentSubject.begin_hour in [ begin_hour for begin_hour, _ in subjects_list ]: continue
                
                studentSubject.building = subject["buildNum"]
                studentSubject.auditorium = subject["audNum"]
                studentSubject.dates = subject["dayDate"]
                studentSubject.title = subject["disciplName"]
                studentSubject.type = subject["disciplType"]
                studentSubject.teacher = subject["prepodName"]
                studentSubject.department = subject["orgUnitName"]
                
                subjects_list.append((studentSubject.begin_hour, studentSubject))
        
        subjects_list.sort(key=lambda subject: subject[0])  # Sort by begin_hour
        
        daily_schedule = "".join([ subject.get() for _, subject in subjects_list ])

        weekly_schedule.append("".join([
            "*{weekday}, {day} {month}*".format(
                weekday=WEEKDAYS[weekday],
                day=int(date.strftime("%d")),
                month=MONTHS[date.strftime("%m")]
            ),
            daily_schedule if daily_schedule != "" else "\n\nВыходной"
        ]))
    
    # Adding Sunday as well
    date = today + timedelta(days=7 - todays_weekday)

    weekly_schedule.append("*Воскресенье, {day} {month}*\n\nОднозначно выходной".format(
        day=int(date.strftime("%d")),
        month=MONTHS[date.strftime("%m")]
    ))

    return weekly_schedule

def beautify_exams(json_response):
    # Removing extraspaces & standardizing values to string type
    json_response = [ {
            key: " ".join(str(value).split()) for key, value in subject.items()
        } for subject in json_response
    ]
    
    schedule = ""
    
    for subject in json_response:
        time_place = "\n\n*[ {date}, {time} ][ {building}, {auditorium} ]*".format(
            date=subject["examDate"],
            time=subject["examTime"],
            building="{}ка".format(subject["buildNum"]),  # Make buildings look beautiful
            auditorium=subject["audNum"]
        )
        
        subject_name = "\n*{subject_name}*".format(subject_name=subject["disciplName"])
        
        teacher = "\n@ {teacher}".format(teacher=subject["prepodName"].title()) if subject["prepodName"] else ""
        
        # Concatenate all the stuff above
        schedule = "".join([ schedule, time_place, subject_name, teacher ])

    return [ schedule ]

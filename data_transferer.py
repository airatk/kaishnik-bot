from bot.helpers.student import Student

from pickle import load
from pickle import dump
from pickle import HIGHEST_PROTOCOL

from sys import argv


type = argv[1]  # Type of data transfer
input_path = argv[2]
output_path = argv[3]

d = {}  # Transfer dictionary
r = None  # Receiver

with open(input_path, "rb") as file: r = load(file)

if type == "obj":  # To dictionary with Student objects
    for id, student in r.items():
        d[id]                          = Student()
        d[id]._institute               = student["institute"]
        d[id]._institute_id            = student["institute_id"]
        d[id]._year                    = student["year"]
        d[id]._group_number            = student["group_number"]
        d[id]._group_number_schedule   = student["group_number_schedule"]
        d[id]._group_number_score      = student["group_number_score"]
        d[id]._name                    = student["name"]
        d[id]._name_id                 = student["name_id"]
        d[id]._names                   = student["names"]
        d[id]._student_card_number     = student["student_card_number"]
        d[id]._notes                   = student["notes"]
        d[id]._edited_subjects         = student["edited_subjects"]

elif type == "str":  # To simple dictionary
    for id, student in r.items():
        d[id]                          = {}
        d[id]["institute"]             = student._institute
        d[id]["institute_id"]          = student._institute_id
        d[id]["year"]                  = student._year
        d[id]["group_number"]          = student._group_number
        d[id]["group_number_schedule"] = student._group_number_schedule
        d[id]["group_number_score"]    = student._group_number_score
        d[id]["name"]                  = student._name
        d[id]["name_id"]               = student._name_id
        d[id]["names"]                 = student._names
        d[id]["student_card_number"]   = student._student_card_number
        d[id]["notes"]                 = student._notes
        d[id]["edited_subjects"]       = student._edited_subjects
else:
    print(
        "Incorrect options!\n"
        "python3 data_transferer.py [ type: obj, str ] [ input path ] [ output path ]"
    )
    
    exit()

with open(output_path, "wb") as file: dump(r, file, HIGHEST_PROTOCOL)

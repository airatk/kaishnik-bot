from bot.shared.api.student import Student

from pickle import load
from pickle import dump
from pickle import HIGHEST_PROTOCOL

from sys import argv


result_data_type: str = argv[1]
input_path: str = argv[2]
output_path: str = argv[3]

input_data: {int: None} = None
output_data: {int: None} = {}

with open(input_path, "rb") as input_file: input_data = load(input_file)

if result_data_type == "obj":  # `str` to `Student`
    for (id, student) in input_data.items():
        output_data[id]                    = Student()
        output_data[id]._is_setup          = student["is_setup"]
        output_data[id]._is_full           = student["is_full"]
        output_data[id]._institute         = student["institute"]
        output_data[id]._institute_id      = student["institute_id"]
        output_data[id]._year              = student["year"]
        output_data[id]._group             = student["group"]
        output_data[id]._group_schedule_id = student["group_schedule_id"]
        output_data[id]._group_score_id    = student["group_score_id"]
        output_data[id]._name              = student["name"]
        output_data[id]._name_id           = student["name_id"]
        output_data[id]._names             = student["names"]
        output_data[id]._card              = student["card"]
        output_data[id]._notes             = student["notes"]
        output_data[id]._edited_subjects   = student["edited_subjects"]
        
elif result_data_type == "str":  # `Student` to `str`
    for (id, student) in input_data.items():
        output_data[id]                      = {}
        output_data[id]["is_setup"]          = student._is_setup
        output_data[id]["is_full"]           = student._is_full
        output_data[id]["institute"]         = student._institute
        output_data[id]["institute_id"]      = student._institute_id
        output_data[id]["year"]              = student._year
        output_data[id]["group"]             = student._group
        output_data[id]["group_schedule_id"] = student._group_schedule_id
        output_data[id]["group_score_id"]    = student._group_score_id
        output_data[id]["name"]              = student._name
        output_data[id]["name_id"]           = student._name_id
        output_data[id]["names"]             = student._names
        output_data[id]["card"]              = student._card
        output_data[id]["notes"]             = student._notes
        output_data[id]["edited_subjects"]   = student._edited_subjects
        
else:
    print(
        "Incorrect options!\n"
        "python3 {script} [ type: obj, str ][ input path ][ output path ]".format(script=argv[0])
    )
    
    exit()

with open(output_path, "wb") as output_file:
    dump(output_data, output_file, HIGHEST_PROTOCOL)

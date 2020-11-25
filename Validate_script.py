import json
import os
from jsonschema import Draft4Validator

# Перезапишем лог файл
with open('script_log.txt', 'w') as file:
    file.write('')

# Поиск и получение имен файлов json и схем в корене проекта.
list_name_event = list(os.walk('./event'))[0][2]
list_name_schema = list(os.walk('./schema'))[0][2]

# Извлечем данные из файлов
list_json_event = []
for e_name in list_name_event:
    with open('./event/' + e_name, 'r') as file_data:
        data = json.load(file_data)
        list_json_event.append(data)

list_json_schema = []
for s_name in list_name_schema:
    with open('./schema/' + s_name, 'r') as file_schema:
        schema = json.load(file_schema)
        list_json_schema.append(schema)


# Функция проверки валидности json схем
def schema_checker(schema, name):
    check_schema = Draft4Validator(schema=Draft4Validator.META_SCHEMA)
    if check_schema.is_valid(schema):
        with open('script_log.txt', 'a') as file:
            file.write('Schema {} is valid\n'.format(name))
    else:
        for err in check_schema.iter_errors(instance=schema):
            with open('script_log.txt', 'a') as file:
                file.write(err)


# Проверим схемы в папке schema
for s in range(len(list_name_schema)):
    schema_checker(list_json_schema[s], list_name_schema[s])

# Проверим json данные по каждой схеме
for s in range(len(list_name_schema)):
    validator = Draft4Validator(schema=list_json_schema[s])
    for e in range(len(list_name_event)):
        with open('script_log.txt', 'a') as file:
            file.write('\nFile {0} had checked with schema {1}.\nFile have next problem:'
                       .format(list_name_event[e], list_name_schema[s]))
        for error in validator.iter_errors(instance=list_json_event[e]):
            with open('script_log.txt', 'a') as file:
                file.write('\n    ' + repr(error))

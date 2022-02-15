from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = []
    for one_row in rows:
        full_name = one_row[0] + ' ' + one_row[1] + ' ' + one_row[2]
        full_name_split = full_name.split(' ', maxsplit=2)
        last_name = full_name_split[0].replace(' ', '')
        first_name = full_name_split[1].replace(' ', '')
        patronymic = full_name_split[2].replace(' ', '')
        list_split_full_name = [last_name, first_name, patronymic]
        one_row[0] = last_name
        one_row[1] = first_name
        one_row[2] = patronymic

        pattern = re.compile(r"(\+7|8)?[\s-]*\(?([\d]{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d+)*\s?\(?(доб.)?[\s]?(\d+)?\)?")
        new_phone_number = pattern.sub(r"+7(\2)\3-\4-\5 \6\7", one_row[5])
        if 'доб' not in new_phone_number:
            new_phone_number = new_phone_number.replace(' ', '')
        one_row[5] = new_phone_number

        contacts_list.append(one_row)


list_repetitive_person = []
for i in range(len(contacts_list)-1):
    for j in range(i+1, len(contacts_list)):
        list_one_repetitive_person = []
        if (contacts_list[i][0] == contacts_list[j][0]) and (contacts_list[i][1] == contacts_list[j][1]):
            list_one_repetitive_person.append(i)
            list_one_repetitive_person.append(j)
            list_repetitive_person.append(list_one_repetitive_person)

list_value_repeated_persons = []
for one_elem in list_repetitive_person:
    list_value_repeated_one_person = []
    for one_repeat in range(len(list_repetitive_person)):
        list_value_repeated_one_person.append(contacts_list[one_elem[one_repeat]])
    list_value_repeated_persons.append(list_value_repeated_one_person)

list_numbers_of_duplicated_persons = []
for one_structure in list_repetitive_person:
    for one_string in one_structure:
        list_numbers_of_duplicated_persons.append(one_string)



list_no_duplicate_persons = []
for one_list in list_value_repeated_persons:
    list_no_duplicate_one_person = []
    counter = 0
    for one_person in one_list:
        if counter > 0:
            field_counter = 0
            for one_param in one_person:
                if one_param != '':
                    list_no_duplicate_one_person[field_counter] = one_param
                field_counter += 1
        else:
            for one_field in one_person:
                list_no_duplicate_one_person.append(one_field)
        counter += 1
    list_no_duplicate_persons.append(list_no_duplicate_one_person)

position = 0
for one_human_number in list_numbers_of_duplicated_persons:
    counter_humans = 0
    for person in contacts_list:
        if counter_humans == (one_human_number - position):
            contacts_list.pop(counter_humans)
            position += 1
        else:
            counter_humans += 1


for one_profile in list_no_duplicate_persons:
    contacts_list.append(one_profile)




with open("phonebook_fixed.csv", "w", encoding='utf-8') as output_f:
    datawriter = csv.writer(output_f, delimiter=',')
    datawriter.writerows(contacts_list)
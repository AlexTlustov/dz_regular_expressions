from pprint import pprint
import re
import csv

# Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_csv/phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# Создание списка lastname
reg_lastname = r'^[А-я]\w+'
list_lastname = []
for i in contacts_list:
    res = re.findall(reg_lastname, ' '.join(i))
    if res == None:
        continue
    elif res == []:
        continue
    elif ''.join(res).strip() in list_lastname:
        continue 
    else:
        list_lastname.append(''.join(res).strip())

                           
# Создание списка firstname
reg_firstname = r'.[А-Я][а-я]\w+'
list_firstname = []
for i in contacts_list:
    res = re.search(reg_firstname, ' '.join(i))
    if res == None:
        continue
    elif res.group().strip() in list_firstname:
        continue
    else:
        list_firstname.append(res.group().strip())  


# Создание списка surname
reg_surname = r'[А-Я]\w+\Bвич|[А-Я]\w+\Bвна'
list_surname = []
for i in contacts_list:
    res = re.findall(reg_surname, ' '.join(i))
    if res == None:
        continue
    elif res == []:
        continue
    elif ''.join(res).strip() in list_surname:
        continue 
    else:
        list_surname.append(''.join(res).strip())


# Создание словаря lastname и email 
reg_email = r'[0-9a-zA-Z]\w+[.@]\w+[.@]\w+.+'
dict_email = {}
for row in contacts_list:
    for element in row:
        res_lastname = re.findall(reg_lastname, ' '.join(row))
        res_email = re.findall(reg_email, ' '.join(row))
        if res_email == None:
            continue
        elif res_lastname == [] and res_email == []:
            continue
        elif ''.join(res_lastname).strip() in list_lastname:
             dict_email[''.join(res_lastname)] = ''.join(res_email)
        else:
            continue
# Создание списка email
list_email = []
for k, v in dict_email.items():
    list_email.append(v)



# Создание словаря organization и lastname
reg_organization = r'\bМинфин|\bФНС'
dict_organization = {}
for row in contacts_list:
    for element in row:
        res_lastname = re.findall(reg_lastname, ' '.join(row))
        res_organization = re.findall(reg_organization, ' '.join(row))
        if res_organization == None:
            continue
        elif res_lastname == [] and res_organization == []:
            continue
        elif ''.join(res_lastname).strip() in list_lastname and len(res_organization) > 0:
             dict_organization[''.join(res_lastname)] = ''.join(res_organization)
        else:
            continue
# Создание списка organization
list_organization = []
for k, v in dict_organization.items():
    list_organization.append(v)



# Создание словаря position
dict_position = {}
for row in contacts_list:
    for element in row:
        res_lastname = re.findall(reg_lastname, ' '.join(row))
        if res_lastname == []:
            continue
        elif ''.join(res_lastname).strip() in list_lastname and len(row[4]) > 0:
             dict_position[''.join(res_lastname)] = row[4]
        elif ''.join(res_lastname).strip() in list_lastname and len(row[4]) <= 0:
             dict_position[''.join(res_lastname)] = ''
        else:
            continue
# Создание списка position
list_position = []
for k, v in dict_position.items():
    list_position.append(v)


# Создание списка phone
reg_phone = r'(\+7|8)( \(| |\(|)(\d{3})(\) |\)|-|)(\d{3})(-|)(\d{2})(\-|)(\d{2})( \(\w+. (\d{4})\)| \w+. (\d{4}))|(\+7|8)( \(| |\(|)(\d{3})(\) |\)|-|)(\d{3})(-|)(\d{2})(\-|)(\d{2})'
shablon1= r'+7(\15\3)\5\17-\7\19-\21\9'
shablon2 = r'+7(\15\3)\5\17-\7\19-\21\9 доб.\11\12'
list_phones = []
for i in contacts_list:
    result = re.sub(reg_phone, shablon1, ', '.join(i))
for i in contacts_list:
    res = re.search(reg_phone, ' '.join(i))
    if res != None:
        ext_number1 = res.group(11)
        ext_number2 = res.group(12)
        if ext_number1 is not None:
            new_phone = re.sub(reg_phone, shablon2, res.group())
            list_phones.append(new_phone)
        elif ext_number2 is not None: 
            new_phone = re.sub(reg_phone, shablon2, res.group())
            list_phones.append(new_phone)
        else:
            new_phone = re.sub(reg_phone, shablon1, res.group())
            list_phones.append(new_phone)
    else:
        continue

# Код для записи файла в формате CSV:
with open("new_phonebook_raw.csv", mode='w', encoding='utf-8') as f:
    names = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    datawriter = csv.DictWriter(f, fieldnames=names)
    datawriter.writeheader()
    for i in zip(list_lastname, list_firstname, list_surname, list_organization, list_position, list_phones, list_email):
        datawriter.writerow({'lastname': i[0], 'firstname': i[1], 'surname': i[2], 'organization': i[3], 'position': i[4], 'phone': i[5], 'email': i[6]})

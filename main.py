import re
import csv


def open_csv():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def save_csv(new_phonebook):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_phonebook)


def csv_processing(contacts_list):
    phonebook = []
    for number, row in enumerate(contacts_list[1:]):
        name = (re.search(r'^(\w+)[,\s]?(\w+)[,\s]?(\w+)?', ' '.join(row[0:2]))[0]).split()
        email = row[-1]
        phone = re.sub(r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d+)\s*[\s(]?(доб.)*\s*(\d+)?[\s)]?',
                       r'+7(\2)\3-\4-\5 \6\7', row[-2])
        position = row[4]
        organization = row[3]
        surname = name[2] if len(name) == 3 else ''
        firstname = name[1]
        lastname = name[0]
        phonebook.append([lastname, firstname, surname, organization, position, phone.strip(), email])
    return phonebook


def list_clearning(phonebook):
    new_phonebook = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]
    add_contacts = []
    for i in range(len(phonebook)):
        for j in range(i + 1, len(phonebook)):
            flag = False
            name_surname = (phonebook[i][0], phonebook[i][1])
            person = []
            if name_surname not in add_contacts:
                if phonebook[i][0] == phonebook[j][0] and phonebook[i][1] == phonebook[j][1]:
                    for num, param in enumerate(phonebook[i]):
                        if param:
                            person.append(param)
                        else:
                            person.append(phonebook[j][num])
                    new_phonebook.append(person)
                    add_contacts.append(name_surname)
                    flag = True
            else:
                flag = True
                break
        if not flag and name_surname not in add_contacts:
            new_phonebook.append(phonebook[i])
            add_contacts.append(name_surname)
    return new_phonebook


def main():
    contacts_list = open_csv()
    phonebook = csv_processing(contacts_list)
    new_phonebook = list_clearning(phonebook)
    save_csv(new_phonebook)

if __name__ == '__main__':
    main()

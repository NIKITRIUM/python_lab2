from csv import DictReader
from random import sample
import xml.etree.ElementTree as ET


def check_length(csv_file, limit):
    csv_file.seek(0)
    reader = DictReader(csv_file, delimiter=';')
    titles = [data["Название"] for data in reader]
    counter = 0
    for title in titles:
        if len(title) > limit:
            counter += 1
    print(f'Количество записей, у которых поле "Название" длиннее {limit} символов: {counter}.')


def author_search(csv_file, author):
    csv_file.seek(0)
    reader = DictReader(csv_file, delimiter=';')
    books = [[data["Название"], data["Автор (ФИО)"], data["Дата поступления"]] for data in reader]
    counter = 0
    printed_books = []
    for title, book_author, give_date in books:
        if give_date != '':
            date = give_date.split(' ')
            date_year = int(date[0].split('.')[-1])
            if 2016 <= date_year <= 2018:
                if author.lower() in book_author.lower():
                    if [title, book_author] not in printed_books:
                        counter += 1
                        printed_books.append([title, book_author])
                        print(f'{counter}. "{title}" {book_author}')

                    
def make_references(csv_file, count):
    csv_file.seek(0)
    reader = DictReader(csv_file, delimiter=';')
    books = [[data["Название"], data["Автор (ФИО)"], data["Дата поступления"]] for data in reader]
    result = ''
    counter = 0
    for title, book_author, give_date in sample(books, count):
        date = give_date.split(' ')
        date_year = date[0].split('.')[-1]
        counter += 1
        result += f'{counter}. {book_author}. {title} - {date_year}\n'
    return result


def do_parsing():
    tree = ET.parse("currency.xml")
    root = tree.getroot()
    char_codes = []
    for valute in root.findall("Valute"):
        nominal = int(valute.find("Nominal").text)
        char_code = valute.find("CharCode").text

        if nominal == 10 or nominal == 100:
            char_codes.append(char_code)

    print("Валюты с номиналом 10 или 100:", *char_codes)
    return char_codes


def get_tags(csv_file):
    csv_file.seek(0)
    reader = DictReader(csv_file, delimiter=';')
    unique_tags = []
    for data in reader:
        raw_tags = data["Жанр книги"]
        for tag in raw_tags.split('#'):
            tag = tag.strip()
            if tag != '' and tag not in unique_tags:
                if '/' in tag:
                    new_tags = tag.split('/')
                    for i in range(tag.count('/')+1):
                        new_tag = new_tags[i].strip()
                        if new_tag not in unique_tags:
                            unique_tags.append(new_tag)
                else:
                    unique_tags.append(tag)
    print(f'Уникальные теги:')
    print(', '.join(unique_tags))


def get_popular(csv_file, count):
    csv_file.seek(0)
    reader = DictReader(csv_file, delimiter=';')
    books = [[
        data["Название"], 
        data["Автор (ФИО)"], 
        data["Кол-во выдач"], 
        data["Тип"]]
        for data in reader]
    unique_books = {}
    for title, author, give_count, book_type in books:
        book_key = (title, author, book_type)
        give_count = int(give_count)
        if book_key not in unique_books or give_count > unique_books[book_key]:
            unique_books[book_key] = give_count
    sorted_books = sorted(unique_books.items(), key = lambda book: book[1], reverse=True)[:count]
    print(f"Топ-{count} самых популярных книг:")
    for i in range(1,count+1):
        ((title, author, book_type), give_count) = sorted_books[i-1]
        print(f'{i}. "{title}" - {author}. Выдач: {give_count}. (формат: {book_type})')

            
with open("books.csv", encoding="utf-8") as books:
    #check_length(books,30)
    # author_search(books, 'иван')
    #with open("bibliography.txt", 'w', encoding="utf-8") as out_file:
      #   out_file.write(make_references(books,20))
    get_tags(books)
    #get_popular(books, 20)

do_parsing()

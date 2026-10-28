from csv import DictReader


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
            if 2016<=date_year <= 2018:
                if author.lower() in book_author.lower():
                    if [title, book_author] not in printed_books:
                        counter += 1
                        printed_books.append([title, book_author])
                        print(f'{counter}. "{title}" {book_author}')
                    



with open("books.csv", encoding="utf-8") as books:
    check_length(books,30)
    author_search(books, 'КО')
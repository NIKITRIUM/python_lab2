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

with open("books.csv", encoding="utf-8") as books:
    check_length(books,30)
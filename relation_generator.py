'''
Author generator
'''
import json
from random import randint
from random import uniform
import names



def author_gen(num):
    '''
    main method
    '''
    #populating arrays with countries and gender
    countries = [country.rstrip('\n') for country in open("Data/list.countries")]
    genders = ["male", "female"]

    #init author list
    authors_json = []

    #Generating records
    for i in range(num):

        author_id = i
        gender = genders[randint(0, 1)]
        country = countries[randint(0, 241)]
        firstname = names.get_first_name(gender=gender)
        lastname = names.get_last_name()
        birthyear = randint(1000, 2000)

        author = {
            "author_id":author_id,
            "firstname":firstname,
            "lastname":lastname,
            "gender:":gender,
            "birthplace":country,
            "birthyear":birthyear
            }

        authors_json.append(author)



    #insert the generated authour json into a file
    with open("Data/relation.authors.json", "w") as openf:
        json.dump(authors_json, openf, sort_keys=True, indent=4, ensure_ascii=False)
        openf.write('\n')

def book_gen(num):
    '''
    main method
    '''
    #populating arrays with book titles
    titles = [title.rstrip('\n') for title in open("Data/list.titles")]


    #init book list
    book_json = []

    #generates the forieng key depending on the author relation size
    try:
        with open("Data/relation.authors.json", "r") as openf:
            json_list = json.load(openf)
    except FileNotFoundError:
        print("Author data file not found!")
        return
    total_id = len(json_list) - 1
    #Generating records
    for i in range(num):

        book_id = i
        title = titles[randint(0, 750)]
        author_id = randint(0, total_id)
        price = float("{0:.2f}".format(uniform(10.0, 100.0)))

        book = {
            "book_id":book_id,
            "title":title,
            "author_id":author_id,
            "price:":price,
            }

        book_json.append(book)

    #insert the generated book json into a file
    with open("Data/relation.books.json", "w") as openf:
        json.dump(book_json, openf, sort_keys=True, indent=5, ensure_ascii=False)
        openf.write('\n')

'''
Natural join between authors and books datafile
'''
import json

def natural_join():
    '''
    natural join method
    '''

    try:
        #gets authors data
        with open("Data/relation.authors.json") as openf:
            authors_json = json.load(openf)
        #gets books data
        with open("Data/relation.books.json") as openf:
            books_json = json.load(openf)
    except FileNotFoundError:
        print("Files not found!")
        return

    #init book relation
    join_json = []
    #natural join between two data files
    for author in authors_json:
        author_id = author["author_id"]
        for book in books_json:
            if author_id == book["author_id"]:
                record = author.copy()
                record.update(book)
                join_json.append(record)

    print("Number of records after natural join: {}\n".format(len(join_json)))
    #insert the join result inside a file
    with open("Data/relation.joint.json", "w") as openf:
        json.dump(join_json, openf, sort_keys=True, indent=5, ensure_ascii=False)
        openf.write('\n')






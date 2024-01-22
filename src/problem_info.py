from datastore import Datastore

def get_problem(num: int) -> dict:
    with Datastore('problems.db', 'schema.sql') as db:
        db.insert_problem(10, 'title ad', 'slugger')
        row = db.select_problem(num)
        if row:
            print('found a row lol')
            print(row)
        else:
            print('no')



    # convert num to slug
    # fetch problem info
    # parse problem info
    # return

def get_slug(num: int) -> str:
    pass

get_problem(10)
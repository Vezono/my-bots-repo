import os

# environ = os.environ
environ = {'database':'mongodb://gbball:onionland@database-shard-00-00-fcfmt.gcp.mongodb.net:27017,'
                      'database-shard-00-01-fcfmt.gcp.mongodb.net:27017,'
                      'database-shard-00-02-fcfmt.gcp.mongodb.net:27017/test?ssl=true&replicaSet=database-shard-0'
                      '&authSource=admin&retryWrites=true&w=majority',
           'britbot':'970751955:AAEFdmjC8_nblWSPiVyxnGTRH3nRUGgACUw',
           'gogbot':'1017113506:AAFPTkBxF-VFhbVEyAwZ-J2C8kHMDh4IshE'}

creator = 792414733

n = 0
r = {'drink': 'Выпить',
     'reject': 'Отказаться',
     'throw': 'Вылить'}
games={}
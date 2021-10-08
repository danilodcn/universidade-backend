from typing import List
from redis import Redis
try:
    from tables import Model
except:
    from app.tables import Model

class Banco(Redis):
    def __init__(self, suffix="count", **kw, ):
        super().__init__(**kw)
        self.suffix = suffix

    def set_one(self, table: Model):

        with self.pipeline() as pipe:
            
            for key, field, value in table.get_data():
                pipe.hset(key, field, value)
                # print(key)
            try:
                pipe.execute()
                # key = "{}:{}".format(key, self.suffix)
                # self.incrby(key, 1)
            except:
                return False
        return True
        
    def set_many(self, tables: List[Model]):
        for table in tables:
            self.set_one(table)

    def get_last_number(self, class_name: str, increment=False):
        table_name = "{}:{}".format(class_name, self.suffix)

        if increment:
            return self.incrby(table_name, 1)

        else:
            number =  self.get(table_name)
            if number == None:
                number = 0

            return number

    def get_last(self, name, search=None):
        if search is None: search = "*"
        name += search
        keys = self.keys(name)
        numeros = [key.decode().split(":")[-1] for key in keys]
        numeros = map(int, numeros)
        return max(numeros)

    
    def search_for_key(self, search_term="", getvalues=False): 
        keys = self.keys(search_term)
        # import ipdb; ipdb.set_trace()
        keys = [key.decode() for key in keys]
        if getvalues:
            return self.__iterator_in_search_for_keys(keys)
        else:
            return keys

    def __iterator_in_search_for_keys(self, keys: list):
        for key in keys:
            try:
                hkeys = self.hkeys(key)
                values = self.hmget(key, *hkeys)
                
                hkeys = [k.decode() for k in hkeys]
                values = [v.decode() for v in values]
                
                yield {key: dict(zip(hkeys, values))}
                continue
            except Exception as e:
                print(e)
                import ipdb; ipdb.set_trace()

    def del_key(self, keys):
        if not isinstance(keys, (list, tuple)):
            keys = [keys]

        return self.delete(*keys)
    
    def del_for_search_term(self, search_term=""):
        keys = self.keys(search_term)

        return self.delete(*keys)



    
    
    
# Author: kevinh939@gmail.com

from xmlrpc import client


class Common(client.ServerProxy):
    def __init__(self, url: str, user: str, db: str, pw: str):
        super().__init__(uri="{}/xmlrpc/2/common".format(url))
        self.__db = db
        self.user = user
        self.__password = pw

        uid = self._auth()
        self.__uid = uid if isinstance(uid, int) else False

    def _auth(self):
        return self.authenticate(self.__db, self.user, self.__password, {})

    def get_password(self):
        return self.__password

    def get_db(self):
        return self.__db

    def get_uid(self):
        return self.__uid


class ClientAPI(client.ServerProxy):

    """
       self.search_read([('id', '=', '371')], fields=["full_name", 'users']))
       self._query_rpc("write", [371, 193], {'users': [(6, 0, [874, 698, 630, 704])],
                                               'implied_ids': [(6, 0, [238])],
                                               })

       self.write_to_many([371, 193], {
           'implied_ids': [238],
           'users': [874, 698, 630, 704]})

        self.write([193],
                   {'name': "Usuario Final",
                    'category_id': 121})

         self.search_read(model="ir.module.category", fields=['name', 'id'])
    """

    def __init__(self, url: str = "", db: str = "", user: str = "", password: str = "", **kwargs):
        self.common = Common(url, user, db, password)
        if self.common.get_uid():
            super().__init__(uri="{}/xmlrpc/2/object".format(url), **kwargs)
            self.url = url
            self.model = "res.groups"
            self.message_conn = self.show_message()
        else:
            print("Cannot Authenticate with {}".format(url))

    def show_message(self):
        info = self.search_read("res.users",
                                domain=[("id", "=", self.common.get_uid())],
                                fields=['id', 'name'])

        msg = "\nDefault connection with {}\t\n {}\n".format(info[0].get("name"), self.url)
        print(msg)
        return msg

    def get_model(self):
        return self.model

    def get_uid(self):
        return self.common.get_uid()

    def set_model(self, model):
        self.model = self.model if "" else model

    def _quey_rpc(self, operation: str, *args, **kwargs):
        return self.execute_kw(
            self.common.get_db(),
            self.common.get_uid(),
            self.common.get_password(),
            self.get_model(),
            operation,
            args,
            kwargs)

    def search_read(self, model: str = "", domain=None, **kwargs):
        if domain is None:
            domain = []
        elif not isinstance(domain[-1], tuple):
            domain = [tuple(domain)]
        kwargs.pop("pretty_out", None)
        kwargs.pop("sort_keys", None)
        if model:
            self.set_model(model)
        return self._quey_rpc("search_read", domain, **kwargs)

    def write_to_many(self, ids_dest: list, values: dict, model: str = "", tpl0: int = 6, tpl1=0):
        fixed_values = dict()
        if model:
            self.set_model(model)
        for field, value in values.items():
            fixed_values[str(field)] = [(tpl0, tpl1, value)]

        return self._quey_rpc("write", ids_dest, fixed_values)

    def write(self, ids_dest: list, values: dict, model: str = "",):
        if model:
            self.set_model(model)
        return self._quey_rpc("write", ids_dest, values)

    def create(self, model: str = "", *args):
        if model:
            self.set_model(model)
        return self._quey_rpc("create", *args)

    def read(self, model: str = "", *args, **kwargs):
        if model:
            self.set_model(model)
        return self._quey_rpc("read", *args, **kwargs)

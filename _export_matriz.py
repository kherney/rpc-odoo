# Author: kevinh939@gmail.com

from librpc.generators import RpcXlsxAPI
import argparse
import datetime
import json


def append_between2list(list_source: list, list_dest: list):
    if list_source:
        for item in list_source:
            list_dest.append(item)
    return list_dest


def add_listitem_to_set(list_source: list, set_dest: set):
    if list_source:
        for item in list_source:
            set_dest.add(item)
    return set_dest


def check_id(id_group: any, ids_exists: set):
    if id_group and isinstance(id_group, int):
        if (id_group in ids_exists) and (id_group in [1, 359]):
            return False
        else:
            return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cfile",
                        type=argparse.FileType('r', encoding='latin-1'),
                        help="Credential Odoo Thomas: url, db, user and pwd")
    args = parser.parse_args()

    file = json.load(args.cfile)

    menu, access_rignt = worksheet_names = ('Menus', 'Permisos',)
    menu_fields, access_fields = header = (["complete_name", ],
                                          ['name', 'model_id', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink'])

    rpc_object = RpcXlsxAPI(
        "TEST",
        worksheet_names,
        header,
        url=file['url'],
        db=file['db'],
        user=file["user"],
        password=file["password"],)

    roles_domain = ["|", "|", "|", "|", "|",
                    ("name", "ilike", "CSC_"),
                    ("name", "ilike", "TGC_"),
                    ("name", "ilike", "TGS_"),
                    ("name", "ilike", "USA_PRD_"),
                    ("name", "ilike", "USA_FI_"),
                    ("name", "ilike", "_FIN_EXT_"),]

    groups_object = rpc_object.search_read("res.groups",
                                           roles_domain,
                                           fields=['display_name', 'id', 'implied_ids'])
    groups = dict()

    for group in groups_object:
        group_id = group.get('id')
        group_name = group.get('display_name')
        group_inherits_ids = group.get('implied_ids')

        inherit_ids = set()
        inherit_ids.add(group_id)
        temporal_ids = list()

        if group_id:

            inherit_ids = add_listitem_to_set(group_inherits_ids, inherit_ids)
            temporal_ids = append_between2list(group_inherits_ids, temporal_ids)

            while temporal_ids:
                actual_id = temporal_ids[0]
                if check_id(actual_id, inherit_ids):

                    ids = rpc_object.search_read("res.groups",
                                                 [("id", "=", actual_id)],
                                                 fields=['implied_ids'])[-1].get('implied_ids')
                    temporal_ids.pop(0)
                    temporal_ids = append_between2list(ids, temporal_ids)
                    inherit_ids.add(actual_id)

                else:
                    temporal_ids.pop(0)
        else:
            print("{} with id: {} cant be False".format(group_name, group_id))

        groups.setdefault(group_id, {'name': group_name, 'inherit_ids': inherit_ids})
        print("Inherits groups in {}:{}\trole loaded".format(group_name, group_id))

    print("\n\n\tLoad access by groups - Take cofe by 15 minutes aprox")
    for group_id, dict_value in groups.items():
        _group_name = dict_value.get('name')
        _inherit_ids = list(dict_value.get('inherit_ids'))

        _ = rpc_object.read('res.groups', _inherit_ids,
                            fields=["full_name", "menu_access", "model_access"],
                            context={'lang': "es_CO"}
                            )
        for group_inherit in _:
            inherit_group_name = group_inherit.get("full_name")
            menus_list = rpc_object.read("ir.ui.menu",
                                         group_inherit.get("menu_access"),
                                         fields=menu_fields,
                                         context={'lang': "es_CO"})
            rpc_object.save_rows(menu, _group_name,
                                 inherit_group_name,
                                 menus_list)

            access_right_list = rpc_object.read("ir.model.access",
                                                group_inherit.get("model_access"),
                                                fields=access_fields,
                                                context={'lang': "es_CO"})
            rpc_object.save_rows(access_rignt, _group_name,
                                 inherit_group_name,
                                 access_right_list)

    rpc_object.write_rows(menu)
    rpc_object.write_rows(access_rignt)
    rpc_object.close_xlsx()

    end_script = datetime.datetime.now()
    delta_time = end_script - init_script
    minute, second = divmod(delta_time.total_seconds(), 60)
    print("\nScript duration: {} Minutes and {} Seconds".format(minute, second))


if __name__ == '__main__':
    init_script = datetime.datetime.now()
    print("Scripts begin {}".format(init_script.time()))
    main()

# Author: kevinh939@gmail.com

from librpc import api
import argparse


def main():
    parser = argparse.ArgumentParser(description='Sesion de usuario Odooo en portalerp')
    parser.add_argument("--user", type=str, help='Usuario DA de odoo')
    parser.add_argument("--url", default='https://portalerp.thomasgreg.com/',
                        type=str, help='Dominio de Odoo, Por defecto portal.erp ')
    parser.add_argument('-db', "--database", default="thomasgregandsons-master-987137",
                        type=str, help='database location')
    parser.add_argument('-pw', "--password", type=str, default="")
    parser.add_argument("--cfile", type=argparse.FileType('r', encoding='latin-1'), required=False)
    parser.add_argument('-ask_pw', action='store_true', dest='ask_password')

    args = parser.parse_args()

    if args.cfile:
        conf_file = json.load(args.cfile)
        connection = api.ClientAPI(conf_file['url'],
                                   conf_file['db'],
                                   conf_file['user'],
                                   conf_file['password'])

        # print("Default connection with {} ".format(
        #     connection.search_read("res.users",
        #                            domain=[("id", "=", connection.get_uid())],
        #                            fields=['id', 'name'],
        #                            )))
    else:
        print("No Config file given")


if __name__ == '__main__':
    import json
    main()

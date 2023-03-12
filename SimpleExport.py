# Author: kevinh939@gmail.com

from librpc.generators import ClientJSON, ClientCSV
import argparse


def connection_request(option: str, file: dict):
    if option == "json":
        session = ClientJSON(
            url=file['url'],
            db=file['db'],
            user=file["user"],
            password=file["password"],)
        return session
    elif option == "csv":
        session = ClientCSV(
            url=file['url'],
            db=file['db'],
            user=file["user"],
            password=file["password"],)
        return session
    else:
        return False


def get_dir_name(raw_dir: str):
    if "/" in raw_dir:
        list_raw_dir = raw_dir.split("/")
        list_raw_dir.append("")
        return list_raw_dir[-1], "/".join(list_raw_dir[:-1])
    else:
        return raw_dir, False


def main():
    """ Usage:
             python3.8 SimpleExport.py file.conf json -f name -m res.partner --domain name ilike kevin --pretty-format

    """
    description = ('Tool for generate an export data file from Odoo ERP in '
                   ' csv or json format.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("cfile",
                        type=argparse.FileType('r', encoding='latin-1'),
                        help="Credential Odoo Thomas: url, db, user and pwd")
    parser.add_argument("type",
                        type=str,
                        help="Format file, specify json or csv")
    parser.add_argument('--model', '-m',
                        type=str,
                        help="model to request",
                        default="res.groups",
                        required=False)
    parser.add_argument('--fields', '-f',
                        nargs='+',
                        help="fields to request",
                        required=True)
    parser.add_argument('--domain',
                        nargs='+',
                        help="Operator like {}, like.You must set the domain in order:"
                             " --domain field operator value".format(PERMIT_OPERATOR_DOMAIN),
                        required=False)
    parser.add_argument('--out-dir', nargs='?',
                        type=str,
                        help="write the output of infile to outfile. Put the name also"
                             "By default it'll write in the current runtime location",
                        default="data/by_default",
                        const="by_default",
                        required=False)
    parser.add_argument('--pretty-format',
                        help='sort a pretty output of dictionaries alphabetically by key',
                        action='store_true',
                        default=False)
    args = parser.parse_args()

    if args.cfile and args.type in ['json', 'csv']:
        _domain = args.domain
        _model = args.model
        _fields = args.fields
        if not _domain or (_domain[1] in PERMIT_OPERATOR_DOMAIN and len(_domain) == MAGIC_NUMBER):
            conf_file = json.load(args.cfile)
            rpc_object = connection_request(args.type, conf_file)
            if not rpc_object:
                sys.exit()
            name, dir_name = get_dir_name(args.out_dir)

            rpc_object.set_dir_name(dir_name)
            rpc_object.set_model(_model)
            rpc_object.export(name,
                              pretty_out=args.pretty_format,
                              sort_keys=True,
                              domain=_domain,
                              fields=_fields)
        else:
            _e_message = "\n Bad input Domain {}. Remember {} inputs and the basic operators {}".format(
                        " ".join(_domain),
                        MAGIC_NUMBER,
                        PERMIT_OPERATOR_DOMAIN)
            print(_e_message)
    else:
        print("\nNo Config file given or Bad --type option")


if __name__ == '__main__':
    import json
    import sys

    PERMIT_OPERATOR_DOMAIN = ['=', '!=', '<=', '<', '>', '>=', '=?', '=like', '=ilike', 'like',  'ilike', 'in']
    MAGIC_NUMBER = 3
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

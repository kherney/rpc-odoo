# Author: kevinh939@gmail.com


import functools


def export_csv(func):
    import csv

    @functools.wraps(func)
    def wrapper_export_csv(*args, **kwargs):
        data, name = func(*args, **kwargs)
        csv_name = "{}.csv".format(name)
        with open(csv_name, "w", newline='') as csvfile:
            fieldnames = kwargs.get("fields")
            writer = csv.DictWriter(csvfile, fieldnames, dialect="excel")
            writer.writeheader()

            for record in data:
                writer.writerow(record)
            csvfile.close()

        return True
    return wrapper_export_csv


def export_json(func):
    import json

    @functools.wraps(func)
    def wrapper_export_json(*args, **kwargs):
        data, name = func(*args, **kwargs)
        json_name = "{}.json".format(name)
        with open(json_name, 'w') as jsonfile:
            for record in data:
                if kwargs.get("pretty_out"):
                    json.dump(record, jsonfile, indent=4, sort_keys=kwargs.get("sort_keys"))
                else:
                    json.dump(record, jsonfile, sort_keys=kwargs.get("sort_keys"))
                jsonfile.write('\n')
            jsonfile.close()
        return True
    return wrapper_export_json

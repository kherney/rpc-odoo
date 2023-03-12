# Author: kevinh939@gmail.com

from thomas.api import ClientAPI
from thomas.wrapper_decorator import export_csv, export_json
import datetime
import xlsxwriter


class RpcXlsxAPI(ClientAPI):

    def __init__(self, file_name: str, worksheet_name: tuple, header: tuple, **kwargs):
        super().__init__(**kwargs)
        self.name = "{}.xlsx".format(file_name)
        self.workbook = xlsxwriter.Workbook(self.name)
        self.rows = self._generate_rows(worksheet_name)
        self.worksheets = self._generate_worksheet(worksheet_name)
        self.headers = self.get_headers(worksheet_name, header)

    def get_headers(self, worksheet_names_tuple: tuple, header_tuple: tuple):
        header_dict = dict()
        _condition = bool(len(worksheet_names_tuple) == len(header_tuple))
        if _condition:
            for i in range(len(worksheet_names_tuple)):
                header_dict.setdefault(worksheet_names_tuple[i],
                                       header_tuple[i])
            return header_dict
        elif not worksheet_names_tuple and len(header_tuple) == 1:
            return header_tuple[-1]
        else:
            print("Header can't be empty ")
            import sys
            sys.exit()

    def _generate_worksheet(self, worksheet_names: tuple):
        if worksheet_names:
            worksheet_names_dict = dict()
            for i in range(len(worksheet_names)):
                name = worksheet_names[i]
                worksheet_names_dict.setdefault(name,
                                                self.workbook.add_worksheet(name))
            return worksheet_names_dict
        else:
            return self.workbook.add_chartsheet()

    def _generate_rows(self, worksheet_names: tuple):
        if worksheet_names:
            row_dict = dict()
            for i in range(len(worksheet_names)):
                name = worksheet_names[i]
                row_dict.setdefault(name,
                                    list())
            return row_dict
        else:
            return list()

    def write_rows(self, worksheet: str):
        i = 0
        if isinstance(self.worksheets, dict):
            _worksheet = self.worksheets.get(worksheet)
        else:
            _worksheet = self.worksheets

        if isinstance(self.rows, dict):
            _rows = self.rows.get(worksheet)
        else:
            _rows = self.rows

        for row in _rows:
            _worksheet.write_row('A{}'.format(i), row)
            i += 1

    def save_rows(self, worksheet: str, main_group: str, inherit_group: str, ids_list: list):
        def get_row():
            built_row = list()
            built_row.append(main_group)
            built_row.append(inherit_group)
            for key in _header:
                value = id_dict.get(key)
                if not isinstance(value, list):
                    built_row.append(value)
                elif isinstance(value, list):
                    built_row.append(value[-1])
            return built_row

        if isinstance(self.rows, dict):
            _rows = self.rows.get(worksheet)
            _header = self.headers.get(worksheet)
        else:
            _rows = self.rows

        if ids_list:
            for id_dict in ids_list:
                _rows.append(get_row(),)
        else:
            _rows.append([main_group, inherit_group, "No {}".format(worksheet)])

    def close_xlsx(self):
        self.workbook.close()


class ClientFileGenerator(ClientAPI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dir_name = str

    def set_dir_name(self, name):
        self.dir_name = name if name else ""

    def get_dir_name(self):
        return self.dir_name

    def export(self, file_name: str, domain=None, **kwargs):
        data = self.search_read(self.get_model(), domain, **kwargs)
        file_name = "{}{}".format(self.dir_name, file_name)

        name = '{}_{}_{}'.format(file_name,
                                 self.get_model(),
                                 datetime.date.today(),
                                 )
        return data, name


class ClientCSV(ClientFileGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @export_csv
    def export(self, file_name: str, domain=None, **kwargs):
        return super().export(file_name, domain, **kwargs)


class ClientJSON(ClientFileGenerator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @export_json
    def export(self, file_name: str, domain=None, pretty_out=False, sort_keys=True, **kwargs):
        return super(ClientJSON, self).export(file_name, domain, **kwargs)

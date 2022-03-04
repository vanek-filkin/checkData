from flask_restful import Resource
import ipaddress
import csv


class CheckData(Resource):
    @staticmethod
    def apply_mask(ip_address, mask):
        """
        Применяет маску к ip адрессу
        :param ip_address: ip адресс
        :param mask: маска подсети
        :return: вычисленная подсеть
        """
        result = '{0}.{1}.{2}.{3}'
        oct_list = []
        for ip_oct, mask_oct in zip(ip_address.split('.'), mask.split('.')):
            oct_list.append(str(int(ip_oct) | int(mask_oct)))
        return result.format(*oct_list)

    def get(self):
        """
        Принимает запрос на обрвботку файла и обробатывает.
        :return: код 200
        """
        data_column = {                   # Словарь с именами для обращения к солбцам
            "ip": 0, "subnet_mask": 1,
            "subnet_address": 2, "num_of_device": 3,
            "name": 5, "Error": 6
        }
        with open("data/Test_Python.csv") as readfile, open("data/Test_Python_Output.csv", "w") as writefile:
            reader = csv.reader(readfile, delimiter=';')
            writer = csv.writer(writefile, delimiter=';',lineterminator="\r")
            device_correct_num = 0
            for index, row in enumerate(reader):
                error_string = ""
                """
                Проверка на валидность данных с помощью ipaddress
                """
                try:
                    ip = ipaddress.ip_address(row[data_column["ip"]])
                except ValueError:
                    error_string += "IP err "
                try:
                    subnet_mask = ipaddress.ip_address(row[data_column["subnet_mask"]])
                except ValueError:
                    error_string += "Mask err "
                try:
                    subnet_address = ipaddress.ip_address(row[data_column["subnet_address"]])
                except ValueError:
                    if not row[data_column["subnet_address"]] == "":
                        error_string += "Subnet err "
                    else:
                        subnet_address = ""
                if not error_string:
                    """
                    Проверка адреса подсети
                    """
                    check_subnet_address = CheckData.apply_mask(str(ip), str(subnet_mask))
                    if check_subnet_address != subnet_address and subnet_address:
                        error_string += "Subnet incorrect "
                    if subnet_address == "":
                        row[data_column["subnet_address"]] = check_subnet_address
                """
                Проверка корректности номера компьютера.
                """
                num_of_device = row[data_column["num_of_device"]]
                if not num_of_device.isdigit() or int(num_of_device) < 0:
                    error_string += "Num Err "
                elif int(num_of_device) > device_correct_num:
                    device_correct_num = int(num_of_device)
                else:
                    device_correct_num += 1
                    row[data_column["num_of_device"]] = str(device_correct_num)
                row.append(error_string)
                writer.writerow(row)
        return 200

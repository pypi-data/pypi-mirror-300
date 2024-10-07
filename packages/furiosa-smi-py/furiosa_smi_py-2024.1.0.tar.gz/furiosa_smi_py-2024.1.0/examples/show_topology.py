from tabulate import tabulate
from furiosa_smi_py import list_devices

def main():
    devices = list_devices()
    table = []
    headers = ['Device']

    for device1 in devices:
        headers.append(device1.device_info().name())
        row = []
        row.append(device1.device_info().name())
        for device2 in devices:
            link_type = device1.get_device_to_device_link_type(device2)
            row.append(link_type)
        table.append(row)

    print(tabulate(table, headers = headers, tablefmt = "fancy_grid"))

if __name__ == "__main__":
    main()
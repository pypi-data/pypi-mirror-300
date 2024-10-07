from furiosa_smi_py import list_devices

def main():
    devices = list_devices()
    for device in devices:
        device_info = device.device_info()
        print("Device Info")
        print(f"\t\tDevice Arch: {device_info.arch()}")
        print(f"\t\tDevice Cores: {device_info.core_num()}")
        print(f"\t\tDevice NUMA Node: {device_info.numa_node()}")
        print(f"\t\tDevice Name: {device_info.name()}")
        print(f"\t\tDevice Serial: {device_info.serial()}")
        print(f"\t\tDevice UUID: {device_info.uuid()}")
        print(f"\t\tDevice BDF: {device_info.bdf()}")
        print(f"\t\tDevice Major: {device_info.major()}")
        print(f"\t\tDevice Minor: {device_info.minor()}")
        print(f"\t\tDevice Firmware Version: {device_info.firmware_version()}")
        print(f"\t\tDevice Driver Version: {device_info.driver_version()}")

        device_files = device.device_files()
        print("Device Files")
        for file in device_files:
            print(f"\t\tDevice File Cores: {file.cores()}")
            print(f"\t\tDevice File Path: {file.path()}")

        core_status = device.core_status()
        print("Core Status")
        for core_id, status in core_status.items():
            print(f"\t\tCore ID: {core_id}")
            print(f"\t\tCore Status: {status}")

        error_info = device.device_error_info()
        print("Device Error Info")
        print(f"\t\tDevice axi post error count: {error_info.axi_doorbell_error_count()}")
        print(f"\t\tDevice axi fetch error count: {error_info.axi_fetch_error_count()}")
        print(f"\t\tDevice axi discard error count: {error_info.axi_discard_error_count()}")
        print(f"\t\tDevice axi doorbell error count: {error_info.axi_doorbell_error_count()}")
        print(f"\t\tDevice pcie post error count: {error_info.pcie_post_error_count()}")
        print(f"\t\tDevice pcie fetch error count: {error_info.pcie_fetch_error_count()}")
        print(f"\t\tDevice pcie discard error count: {error_info.pcie_discard_error_count()}")
        print(f"\t\tDevice pcie doorbell error count: {error_info.pcie_doorbell_error_count()}")
        print(f"\t\tDevice device error count: {error_info.device_error_count()}")

        print(f"Device Liveness: {device.liveness()}")

        print(f"Device Power Consumption: {device.power_consumption()}")

        device_temperature = device.device_temperature()
        print("Device Temperature")
        print(f"\t\tDevice SOC Peak: {device_temperature.soc_peak()}")
        print(f"\t\tDevice Ambient: {device_temperature.ambient()}")

        device_utilization = device.device_utilization()
        print("Device Utilization")
        pe_utilization = device_utilization.pe_utilization()
        for pe in pe_utilization:
            print(f"\t\tPE Core: { pe.core()}")
            print(f"\t\tPE Time Window Mill: { pe.time_window_mill()}")
            print(f"\t\tPE Usage Percentage: { pe.pe_usage_percentage()}")

        memory_utilization = device_utilization.memory_utilization()
        print("Memory Utilization")
        print(f"\t\tMemory Total Bytes: {memory_utilization.total_bytes()}")
        print(f"\t\tMemory In Use Bytes: {memory_utilization.in_use_bytes()}")

if __name__ == "__main__":
    main()
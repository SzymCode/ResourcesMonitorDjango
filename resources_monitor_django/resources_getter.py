import psutil
import time
import ctypes
from .interfaces.resources_base import ResourcesBase


class ComputerResources(ResourcesBase):
    def __init__(self, network_interface_name="Ethernet"):
        self.network_interface_name = network_interface_name

    def get_processor_percentage_usage(self):
        return psutil.cpu_percent()

    def get_ram_percentage_usage(self):
        return psutil.virtual_memory().percent

    def get_network_usage(self):
        net_in, _ = self._get_network_in_out_values()
        return net_in

    def _get_network_in_out_values(self):  # change the inf variable according to the interface
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[self.network_interface_name]
        net_in_1 = net_stat.bytes_recv
        net_out_1 = net_stat.bytes_sent
        time.sleep(1)
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[self.network_interface_name]
        net_in_2 = net_stat.bytes_recv
        net_out_2 = net_stat.bytes_sent

        net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
        net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)

        return net_in, net_out

    def get_uptime(self):
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()

        t = int(str(t)[:-3])

        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)

        return f"{days} days, {hour:02}:{mins:02}:{sec:02}"

    def get_disk_capacity(self):
        hdd = psutil.disk_usage('C:/')
        return round(float(hdd.total) / (2 ** 30), 2)

    def get_disk_usage(self):
        hdd = psutil.disk_usage('C:/')
        return round(float(hdd.used) / (2 ** 30), 2)

    def get_total_disk_usage(self):
        return f"{self.get_disk_usage()} / {self.get_disk_capacity()} GB"

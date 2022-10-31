from abc import ABC, abstractmethod


class ResourcesBase(ABC):
    @abstractmethod
    def get_processor_percentage_usage(self):
        pass

    @abstractmethod
    def get_ram_percentage_usage(self):
        pass

    @abstractmethod
    def get_network_usage(self):
        pass

    @abstractmethod
    def get_disk_capacity(self):
        pass

    @abstractmethod
    def get_disk_usage(self):
        pass

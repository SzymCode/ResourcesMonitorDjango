import json
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from .resources_getter import ComputerResources


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        computer_resources = ComputerResources()
        await self.accept()
        while True:
            cpu_percentage_usage = computer_resources.get_processor_percentage_usage()
            ram_percentage_usage = computer_resources.get_ram_percentage_usage()
            network_in_usage = computer_resources.get_network_usage()
            total_disk_usage = computer_resources.get_total_disk_usage()
            uptime = computer_resources.get_uptime()

            await self.send(json.dumps({"cpuPercentageUsage": f"{cpu_percentage_usage}",
                                        "ramPercentageUsage": f"{ram_percentage_usage}",
                                        "networkUsage": f"{network_in_usage}",
                                        "diskUsage": f"{total_disk_usage}",
                                        "uptime": f"{uptime}"}))
            await sleep(2)

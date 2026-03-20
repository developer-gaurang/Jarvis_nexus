from skills.base_skill import BaseSkill
import psutil

class SystemMonitorSkill(BaseSkill):
    name = "SystemMonitor"
    description = "Monitors local system stats like CPU and RAM."

    def can_handle(self, user_input: str) -> bool:
        keywords = ["cpu", "ram", "memory", "system status"]
        return any(keyword in user_input.lower() for keyword in keywords)

    def execute(self, user_input: str, context: dict) -> str:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        return f"System Status: CPU is at {cpu_usage}% and Memory is at {ram_usage}%."

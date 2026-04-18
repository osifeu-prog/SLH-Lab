import psutil
import json
import time
from datetime import datetime

def get_system_stats():
    return {
        "disk": psutil.disk_usage('D:\\').percent,
        "memory": psutil.virtual_memory().percent,
        "cpu": psutil.cpu_percent(interval=1),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def write_stats():
    stats = get_system_stats()
    with open("D:\\AISITE\\system_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"[{stats['timestamp']}] Disk: {stats['disk']}% | RAM: {stats['memory']}% | CPU: {stats['cpu']}%")

if __name__ == "__main__":
    while True:
        write_stats()
        time.sleep(10)   # עדכון כל 10 שניות

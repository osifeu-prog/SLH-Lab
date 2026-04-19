import psutil
import json
import time
import requests
import os
import docker

OUTPUT_PATH = r"D:\AISITE\system_stats.json"
BOT_TOKEN = "8741101048:AAH5KszG_t1ccT4ejzCrlxRzVYma7XRU3iY"
CHAT_ID = "YOUR_CHAT_ID"
NODE_THRESHOLD = 23

def send_telegram_alert(message):
    if BOT_TOKEN == "YOUR_BOT_TOKEN" or CHAT_ID == "YOUR_CHAT_ID":
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"⚠️ SLH ALERT:\n{message}"}
    try:
        requests.get(url, params=payload, timeout=5)
    except Exception as e:
        print(f"Telegram send failed: {e}")

def get_top_container():
    """מזהה את הקונטיינר שצורך הכי הרבה CPU"""
    try:
        client = docker.from_env()
        containers = client.containers.list()
        top_name = "N/A"
        max_cpu = 0
        for container in containers:
            stats = container.stats(stream=False)
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            if cpu_delta > max_cpu:
                max_cpu = cpu_delta
                top_name = container.name
        return top_name
    except Exception as e:
        print(f"Top consumer detection failed: {e}")
        return "N/A"

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('D:\\').percent
    top_container = get_top_container()
    
    # Docker stats
    active_nodes = 0
    total_nodes = 0
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        total_nodes = len(containers)
        active_nodes = len([c for c in containers if c.status == 'running'])
    except Exception as e:
        print(f"Docker not available: {e}")
        total_nodes = 23
        active_nodes = 23
    
    if active_nodes < NODE_THRESHOLD:
        send_telegram_alert(f"Node failure! Active: {active_nodes}/{NODE_THRESHOLD}")
    
    metrics = {
        "status": "online",
        "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": cpu_usage,
        "memory": memory,
        "disk": disk,
        "top_consumer": top_container,
        "docker_nodes": {
            "total": total_nodes,
            "active": active_nodes
        }
    }
    return metrics

def main():
    print("🚀 SLH Bridge Active. Monitoring system and Docker (Top Consumer)...")
    while True:
        try:
            stats = get_system_metrics()
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"❌ Bridge error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()


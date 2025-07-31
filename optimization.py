import os
import time
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set(style="darkgrid")

# ----------------- Power & Cost Config -----------------
BASE_POWER = 50
POWER_PER_CPU = 0.7
COST_PER_KWH = 0.12
INTERVAL = 10
DURATION = 60
# --------------------------------------------------------

def estimate_power(cpu_percent):
    return BASE_POWER + (cpu_percent * POWER_PER_CPU)

log_file = "optimization_log.txt"
with open(log_file, "a") as f:
    f.write(f"\n\n--- Optimization started at {datetime.now()} ---\n")

print("⚙ [1] Killing unwanted CPU-consuming processes...")
kill_list = ['yes', 'stress', 'top', 'ping']
killed = []

for proc in psutil.process_iter(['pid', 'name']):
    try:
        if proc.info['name'] in kill_list:
            proc.kill()
            killed.append(proc.info['name'])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

with open(log_file, "a") as f:
    f.write(f"Killed processes: {killed}\n")

print("⚙ [2] Stopping Apache2 service if active...")
os.system("sudo systemctl stop apache2")
with open(log_file, "a") as f:
    f.write("Attempted to stop Apache2\n")

print("⚙ [3] Clearing system cache...")
os.system("sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null")
with open(log_file, "a") as f:
    f.write("Cleared system memory cache\n")

# ✅ Monitor after optimization
print("⏱ [4] Monitoring for 1 mins post-optimization...")

log = []
for _ in range(DURATION // INTERVAL):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    power = estimate_power(cpu)
    energy = (power / 1000) * (INTERVAL / 3600)

    log.append({
        'Time': time.strftime('%H:%M:%S'),
        'CPU': cpu,
        'RAM': ram,
        'Power (W)': power,
        'Energy (kWh)': energy
    })
    time.sleep(INTERVAL)

df = pd.DataFrame(log)
df.to_csv("usage_after.csv", index=False)

total_energy = df['Energy (kWh)'].sum()
total_cost = total_energy * COST_PER_KWH

with open(log_file, "a") as f:
    f.write(f"Average CPU: {df['CPU'].mean():.2f}%\n")
    f.write(f"Average RAM: {df['RAM'].mean():.2f}%\n")
    f.write(f"Total Energy: {total_energy:.6f} kWh\n")
    f.write(f"Estimated Cost: ${total_cost:.4f}\n")

print(f"\n📊 Average CPU: {df['CPU'].mean():.2f}% | "
      f"Average RAM: {df['RAM'].mean():.2f}%")
print(f"🔋 Total Energy Consumed: {total_energy:.6f} kWh")
print(f"💰 Estimated Cost: ${total_cost:.4f}")

plt.figure(figsize=(10, 5))
plt.plot(df['Time'], df['CPU'], label='CPU Usage (%)', marker='o')
plt.plot(df['Time'], df['RAM'], label='RAM Usage (%)', marker='o')
plt.plot(df['Time'], df['Power (W)'], label='Power (Watts)', marker='x')
plt.title("Resource & Power Usage After Optimization")
plt.xlabel("Time")
plt.ylabel("Usage / Power")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

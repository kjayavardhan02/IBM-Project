# monitor_and_plot.py
import psutil
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

# ----------------- Power & Cost Config -----------------
BASE_POWER = 50             # Watts at idle
POWER_PER_CPU = 0.7         # Watts per 1% CPU usage
COST_PER_KWH = 0.12         # Cost in $ per kWh
INTERVAL = 10               # Sampling interval in seconds
DURATION = 60              # Total monitoring time in seconds
# --------------------------------------------------------

def estimate_power(cpu_percent):
    """Estimate power consumption (Watts) based on CPU usage."""
    return BASE_POWER + (cpu_percent * POWER_PER_CPU)

print("🔎 Monitoring for 1 minutes...")

log = []
for _ in range(DURATION // INTERVAL):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    power = estimate_power(cpu)
    energy = (power / 1000) * (INTERVAL / 3600)  # kWh for this interval

    log.append({
        'Time': time.strftime('%H:%M:%S'),
        'CPU': cpu,
        'RAM': ram,
        'Power (W)': power,
        'Energy (kWh)': energy
    })
    time.sleep(INTERVAL)

df = pd.DataFrame(log)

# Save results
df.to_csv("usage_before.csv", index=False)

# Summary
total_energy = df['Energy (kWh)'].sum()
total_cost = total_energy * COST_PER_KWH
print(f"\n📊 Average CPU: {df['CPU'].mean():.2f}% | "
      f"Average RAM: {df['RAM'].mean():.2f}%")
print(f"🔋 Total Energy Consumed: {total_energy:.6f} kWh")
print(f"💰 Estimated Cost: ${total_cost:.4f}")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(df['Time'], df['CPU'], label='CPU Usage (%)', marker='o')
plt.plot(df['Time'], df['RAM'], label='RAM Usage (%)', marker='o')
plt.plot(df['Time'], df['Power (W)'], label='Power (Watts)', marker='x')
plt.title("Resource & Power Usage Before Optimization")
plt.xlabel("Time")
plt.ylabel("Usage / Power")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

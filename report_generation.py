import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------- Power & Cost Config ----------------
COST_PER_KWH = 0.12
# ------------------------------------------------------

# Load data
df_before = pd.read_csv("usage_before.csv")
df_after = pd.read_csv("usage_after.csv")

# ✅ Calculate averages
avg_cpu_before = df_before['CPU'].mean()
avg_cpu_after = df_after['CPU'].mean()
avg_ram_before = df_before['RAM'].mean()
avg_ram_after = df_after['RAM'].mean()

# ✅ Calculate energy and cost
total_energy_before = df_before['Energy (kWh)'].sum()
total_energy_after = df_after['Energy (kWh)'].sum()
cost_before = total_energy_before * COST_PER_KWH
cost_after = total_energy_after * COST_PER_KWH

# ✅ Calculate percentage improvements
cpu_reduction = ((avg_cpu_before - avg_cpu_after) / avg_cpu_before) * 100 if avg_cpu_before else 0
ram_reduction = ((avg_ram_before - avg_ram_after) / avg_ram_before) * 100 if avg_ram_before else 0
energy_saved = total_energy_before - total_energy_after
cost_saved = cost_before - cost_after

# ---------------- Generate Comparison Graphs ----------------
plt.figure(figsize=(14, 6))

# CPU Comparison
plt.subplot(1, 3, 1)
plt.plot(df_before['Time'], df_before['CPU'], label='Before', color='red', marker='o')
plt.plot(df_after['Time'], df_after['CPU'], label='After', color='green', marker='o')
plt.title('CPU Usage Comparison')
plt.xlabel('Time')
plt.ylabel('CPU (%)')
plt.legend()
plt.xticks(rotation=45)

# RAM Comparison
plt.subplot(1, 3, 2)
plt.plot(df_before['Time'], df_before['RAM'], label='Before', color='red', marker='o')
plt.plot(df_after['Time'], df_after['RAM'], label='After', color='green', marker='o')
plt.title('RAM Usage Comparison')
plt.xlabel('Time')
plt.ylabel('RAM (%)')
plt.legend()
plt.xticks(rotation=45)

# Power Comparison
plt.subplot(1, 3, 3)
plt.plot(df_before['Time'], df_before['Power (W)'], label='Before', color='red', marker='x')
plt.plot(df_after['Time'], df_after['Power (W)'], label='After', color='green', marker='x')
plt.title('Power Consumption Comparison')
plt.xlabel('Time')
plt.ylabel('Power (Watts)')
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("comparison_graphs.png")
plt.close()

# ---------------- Create PDF Report ----------------
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "VM Energy Optimization Report", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, f"""
CPU Usage Reduced: {cpu_reduction:.2f}%
RAM Usage Reduced: {ram_reduction:.2f}%

Energy Before: {total_energy_before:.6f} kWh
Energy After: {total_energy_after:.6f} kWh

Cost Before: ${cost_before:.4f}
Cost After: ${cost_after:.4f}

Total Energy Saved: {energy_saved:.6f} kWh
Total Cost Saved: ${cost_saved:.4f}
""")

pdf.ln(5)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Resource Usage Comparison", ln=True)

pdf.image("comparison_graphs.png", x=10, w=180)

pdf.output("Final_Energy_Report.pdf")
print("✅ PDF report saved as Final_Energy_Report.pdf")

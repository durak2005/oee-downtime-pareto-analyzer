import pandas as pd
import matplotlib.pyplot as plt

def calculate_oee(planned_time_min, downtime_min, ideal_cycle_sec, total_parts, good_parts):
    """
    Toplam Ekipman Etkinliği (OEE) 3 temel bileşenini hesaplar:
    Availability (A), Performance (P), Quality (Q)
    """
    operating_time_min = planned_time_min - downtime_min
    availability = operating_time_min / planned_time_min
    
    operating_time_sec = operating_time_min * 60
    performance = (ideal_cycle_sec * total_parts) / operating_time_sec
    
    quality = good_parts / total_parts
    oee = availability * performance * quality
    
    return {
        "Availability": availability * 100,
        "Performance": performance * 100,
        "Quality": quality * 100,
        "OEE": oee * 100
    }

def plot_oee_and_pareto(oee_metrics, downtime_data):
    """OEE skorlarını ve Duruş Pareto Analizini yan yana çizer."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})
    
    # 1. OEE Metrikleri Çubuk Grafiği
    metrics = list(oee_metrics.keys())
    values = list(oee_metrics.values())
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#6366f1']
    
    bars = ax1.bar(metrics, values, color=colors, edgecolor='black', width=0.55)
    ax1.set_ylim(0, 110)
    ax1.set_ylabel("Yüzde (%)", fontsize=11)
    ax1.set_title("OEE Performans Karnesi", fontsize=12, fontweight='bold')
    ax1.grid(axis='y', linestyle=':', alpha=0.6)
    
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 2, f"%{h:.1f}", 
                 ha='center', va='bottom', fontweight='bold', fontsize=10)
        
    # 2. Pareto Grafiği (Duruş Nedenleri)
    df = pd.DataFrame(downtime_data).sort_values(by="Duration", ascending=False)
    df["CumPercentage"] = (df["Duration"].cumsum() / df["Duration"].sum()) * 100
    
    ax2_line = ax2.twinx()
    
    ax2.bar(df["Reason"], df["Duration"], color='#0284c7', edgecolor='black', width=0.5, label='Duruş Süresi (dk)')
    ax2_line.plot(df["Reason"], df["CumPercentage"], color='#dc2626', marker='D', linewidth=2, label='Kümülatif %')
    
    # %80 Pareto Referans Çizgisi
    ax2_line.axhline(80, color='#16a34a', linestyle='--', linewidth=1.5, label='%80 Eşiği')
    
    ax2.set_ylabel("Duruş Süresi (Dakika)", fontsize=11, color='#0284c7')
    ax2_line.set_ylabel("Kümülatif Payı (%)", fontsize=11, color='#dc2626')
    ax2_line.set_ylim(0, 110)
    ax2.set_xticklabels(df["Reason"], rotation=20, ha='right', fontsize=9)
    ax2.set_title("Kök-Neden Duruş Pareto Analizi (80/20 Kuralı)", fontsize=12, fontweight='bold')
    ax2.grid(axis='y', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig("oee_pareto_analysis.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    # 8 saatlik vardiya (480 dk), 30 dk yemek/planlı mola -> 450 dk planlı çalışma
    oee_results = calculate_oee(
        planned_time_min=450,
        downtime_min=75,
        ideal_cycle_sec=18,
        total_parts=1100,
        good_parts=1056
    )
    
    downtimes = [
        {"Reason": "Mekanik Arıza", "Duration": 145},
        {"Reason": "Kalıp Değişimi", "Duration": 95},
        {"Reason": "Malzeme Bekleme", "Duration": 60},
        {"Reason": "Operatör Yokluğu", "Duration": 45},
        {"Reason": "Elektrik Kesintisi", "Duration": 30}
    ]
    
    print("OEE Sonuçları:", oee_results)
    plot_oee_and_pareto(oee_results, downtimes)

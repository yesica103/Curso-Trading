"""
TRADING ANALYTICS - Google Colab
Análisis automático de rendimiento de trading

Instrucciones:
1. Abre Google Colab (colab.research.google.com)
2. Crea nuevo notebook
3. Copia este código completo
4. Sube tu CSV cuando se te solicite
5. Ejecuta las celdas en orden
"""

# ============================================================
# CELDA 1: Instalación y Setup
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("✅ Librerías cargadas correctamente")
print("📊 Listo para analizar tus trades\n")

# ============================================================
# CELDA 2: Cargar Datos
# ============================================================

from google.colab import files
import io

print("📁 Sube tu archivo CSV de trading:")
uploaded = files.upload()

# Leer CSV
filename = list(uploaded.keys())[0]
df = pd.read_csv(io.BytesIO(uploaded[filename]))

# Limpiar headers (remover espacios)
df.columns = df.columns.str.strip()

# Convertir fechas
df['Open Time'] = pd.to_datetime(df['Open Time'])
df['Close Time'] = pd.to_datetime(df['Close Time'])

# Calcular duración de trades
df['Duration'] = (df['Close Time'] - df['Open Time']).dt.total_seconds() / 60  # minutos

# Crear columna de resultado
df['Result'] = df['Profit'].apply(lambda x: 'Win' if x > 0 else 'Loss')

print(f"✅ Datos cargados: {len(df)} trades")
print(f"📅 Periodo: {df['Open Time'].min().date()} a {df['Close Time'].max().date()}")
print("\n📋 Primeros 5 trades:")
print(df[['Open Time', 'Type', 'Lots', 'Profit', 'Pips']].head())

# ============================================================
# CELDA 3: Métricas Clave
# ============================================================

def calculate_metrics(df):
    """Calcula todas las métricas de trading"""
    
    # Básicas
    total_trades = len(df)
    winning_trades = len(df[df['Profit'] > 0])
    losing_trades = len(df[df['Profit'] < 0])
    
    win_rate = (winning_trades / total_trades) * 100
    
    # P&L
    gross_profit = df[df['Profit'] > 0]['Profit'].sum()
    gross_loss = abs(df[df['Profit'] < 0]['Profit'].sum())
    net_profit = df['Profit'].sum()
    
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0
    
    # Promedios
    avg_win = df[df['Profit'] > 0]['Profit'].mean() if winning_trades > 0 else 0
    avg_loss = df[df['Profit'] < 0]['Profit'].mean() if losing_trades > 0 else 0
    
    avg_rrr = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    
    # Extremos
    best_trade = df['Profit'].max()
    worst_trade = df['Profit'].min()
    
    # Comisiones
    total_commission = df['Commission'].sum()
    total_swap = df['Swap'].sum()
    
    # Lotes
    avg_lots = df['Lots'].mean()
    total_volume = df['Volume'].sum()
    
    # Duración
    avg_duration = df['Duration'].mean()
    
    # Drawdown (simplified)
    df_sorted = df.sort_values('Close Time')
    cumulative_profit = df_sorted['Profit'].cumsum()
    running_max = cumulative_profit.cummax()
    drawdown = cumulative_profit - running_max
    max_drawdown = drawdown.min()
    
    metrics = {
        'Total Trades': total_trades,
        'Winning Trades': winning_trades,
        'Losing Trades': losing_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Gross Profit ($)': round(gross_profit, 2),
        'Gross Loss ($)': round(gross_loss, 2),
        'Net Profit ($)': round(net_profit, 2),
        'Profit Factor': round(profit_factor, 2),
        'Avg Win ($)': round(avg_win, 2),
        'Avg Loss ($)': round(avg_loss, 2),
        'Avg RRR': round(avg_rrr, 2),
        'Best Trade ($)': round(best_trade, 2),
        'Worst Trade ($)': round(worst_trade, 2),
        'Total Commission ($)': round(total_commission, 2),
        'Total Swap ($)': round(total_swap, 2),
        'Avg Lots': round(avg_lots, 2),
        'Total Volume': round(total_volume, 0),
        'Avg Duration (min)': round(avg_duration, 2),
        'Max Drawdown ($)': round(max_drawdown, 2)
    }
    
    return metrics

# Calcular métricas
metrics = calculate_metrics(df)

# Mostrar resultados
print("=" * 60)
print("📊 MÉTRICAS DE RENDIMIENTO")
print("=" * 60)
for key, value in metrics.items():
    print(f"{key:.<40} {value}")
print("=" * 60)

# ============================================================
# CELDA 4: Análisis de Patrones
# ============================================================

print("\n🔍 ANÁLISIS DE PATRONES\n")

# 1. Rendimiento por tipo de operación
print("1️⃣ Rendimiento por Tipo (Buy vs Sell):")
type_analysis = df.groupby('Type').agg({
    'Profit': ['count', 'sum', 'mean'],
    'Pips': 'mean'
}).round(2)
print(type_analysis)

# 2. Rendimiento por tamaño de lote
print("\n2️⃣ Rendimiento por Tamaño de Lote:")
df['Lot_Range'] = pd.cut(df['Lots'], bins=[0, 0.5, 1, 2, 10], 
                          labels=['Micro (0-0.5)', 'Mini (0.5-1)', 
                                  'Standard (1-2)', 'Large (2+)'])
lot_analysis = df.groupby('Lot_Range').agg({
    'Profit': ['count', 'sum', 'mean']
}).round(2)
print(lot_analysis)

# 3. Rendimiento por día de la semana
print("\n3️⃣ Rendimiento por Día de la Semana:")
df['Day_of_Week'] = df['Open Time'].dt.day_name()
day_analysis = df.groupby('Day_of_Week').agg({
    'Profit': ['count', 'sum', 'mean']
}).round(2)
print(day_analysis)

# 4. Rendimiento por hora del día
print("\n4️⃣ Rendimiento por Hora del Día:")
df['Hour'] = df['Open Time'].dt.hour
hour_analysis = df.groupby('Hour').agg({
    'Profit': ['count', 'sum', 'mean']
}).round(2)
print(hour_analysis.head(10))

# 5. Duración vs Rentabilidad
print("\n5️⃣ Duración vs Rentabilidad:")
df['Duration_Range'] = pd.cut(df['Duration'], 
                               bins=[0, 30, 60, 120, 1000], 
                               labels=['<30min', '30-60min', '1-2h', '>2h'])
duration_analysis = df.groupby('Duration_Range').agg({
    'Profit': ['count', 'sum', 'mean']
}).round(2)
print(duration_analysis)

# ============================================================
# CELDA 5: Visualizaciones
# ============================================================

print("\n📈 Generando visualizaciones...\n")

# Crear figura con múltiples subplots
fig = plt.figure(figsize=(16, 12))

# 1. Curva de Equity
ax1 = plt.subplot(2, 3, 1)
df_sorted = df.sort_values('Close Time')
cumulative_profit = df_sorted['Profit'].cumsum()
ax1.plot(df_sorted['Close Time'], cumulative_profit, linewidth=2, color='blue')
ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax1.set_title('Curva de Equity', fontsize=14, fontweight='bold')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('P&L Acumulado ($)')
ax1.grid(True, alpha=0.3)

# 2. Win Rate por Semana
ax2 = plt.subplot(2, 3, 2)
df_sorted['Week'] = df_sorted['Close Time'].dt.isocalendar().week
weekly_wr = df_sorted.groupby('Week').apply(
    lambda x: (x['Profit'] > 0).sum() / len(x) * 100
)
ax2.bar(weekly_wr.index, weekly_wr.values, color='green', alpha=0.7)
ax2.axhline(y=50, color='red', linestyle='--', label='50% threshold')
ax2.set_title('Win Rate Semanal', fontsize=14, fontweight='bold')
ax2.set_xlabel('Semana')
ax2.set_ylabel('Win Rate (%)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Distribución de P&L
ax3 = plt.subplot(2, 3, 3)
ax3.hist(df['Profit'], bins=20, color='purple', alpha=0.7, edgecolor='black')
ax3.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax3.set_title('Distribución de P&L', fontsize=14, fontweight='bold')
ax3.set_xlabel('Profit ($)')
ax3.set_ylabel('Frecuencia')
ax3.grid(True, alpha=0.3)

# 4. Buy vs Sell Performance
ax4 = plt.subplot(2, 3, 4)
type_profit = df.groupby('Type')['Profit'].sum()
colors = ['green' if x > 0 else 'red' for x in type_profit.values]
ax4.bar(type_profit.index, type_profit.values, color=colors, alpha=0.7)
ax4.set_title('Buy vs Sell - P&L Total', fontsize=14, fontweight='bold')
ax4.set_ylabel('Profit ($)')
ax4.grid(True, alpha=0.3)

# 5. Lotes vs Rentabilidad
ax5 = plt.subplot(2, 3, 5)
ax5.scatter(df['Lots'], df['Profit'], alpha=0.6, s=50, c=df['Profit'], 
            cmap='RdYlGn', edgecolors='black', linewidth=0.5)
ax5.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax5.set_title('Tamaño de Lote vs Rentabilidad', fontsize=14, fontweight='bold')
ax5.set_xlabel('Lotes')
ax5.set_ylabel('Profit ($)')
ax5.grid(True, alpha=0.3)

# 6. Heatmap de Hora vs Día
ax6 = plt.subplot(2, 3, 6)
pivot = df.pivot_table(values='Profit', index='Day_of_Week', 
                       columns='Hour', aggfunc='mean')
sns.heatmap(pivot, annot=False, fmt='.0f', cmap='RdYlGn', 
            center=0, ax=ax6, cbar_kws={'label': 'Avg Profit ($)'})
ax6.set_title('Heatmap: Día vs Hora', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('trading_analysis.png', dpi=300, bbox_inches='tight')
print("✅ Gráficos guardados como 'trading_analysis.png'")
plt.show()

# ============================================================
# CELDA 6: Top 10 Mejores y Peores Trades
# ============================================================

print("\n" + "=" * 60)
print("🏆 TOP 10 MEJORES TRADES")
print("=" * 60)
best_trades = df.nlargest(10, 'Profit')[['Open Time', 'Type', 'Lots', 
                                          'Pips', 'Profit', 'Duration']]
print(best_trades.to_string(index=False))

print("\n" + "=" * 60)
print("💀 TOP 10 PEORES TRADES")
print("=" * 60)
worst_trades = df.nsmallest(10, 'Profit')[['Open Time', 'Type', 'Lots', 
                                            'Pips', 'Profit', 'Duration']]
print(worst_trades.to_string(index=False))

# ============================================================
# CELDA 7: Recomendaciones Automatizadas
# ============================================================

print("\n" + "=" * 60)
print("💡 RECOMENDACIONES BASADAS EN TUS DATOS")
print("=" * 60)

recommendations = []

# 1. Win Rate
if metrics['Win Rate (%)'] < 50:
    recommendations.append(
        f"⚠️ Win Rate bajo ({metrics['Win Rate (%)']}%). "
        "Necesitas mejorar selección de entradas o aumentar RRR a 1:2+"
    )

# 2. Profit Factor
if metrics['Profit Factor'] < 1.5:
    recommendations.append(
        f"⚠️ Profit Factor bajo ({metrics['Profit Factor']}). "
        "Corta pérdidas más rápido y deja correr ganadores"
    )

# 3. RRR
if metrics['Avg RRR'] < 1.5:
    recommendations.append(
        f"⚠️ RRR promedio insuficiente ({metrics['Avg RRR']}). "
        "Busca trades con mínimo 1:2 RRR"
    )

# 4. Comisiones
commission_pct = (abs(metrics['Total Commission ($)']) / metrics['Gross Profit ($)']) * 100
if commission_pct > 10:
    recommendations.append(
        f"⚠️ Comisiones altas ({commission_pct:.1f}% del gross profit). "
        "Reduce frecuencia de trading o cambia broker"
    )

# 5. Lotes
if df['Lots'].std() > 1:
    recommendations.append(
        "⚠️ Alta variación en tamaño de lotes. "
        "Estandariza gestión de riesgo a 1% por trade"
    )

# 6. Duración
if metrics['Avg Duration (min)'] < 60:
    recommendations.append(
        f"⚠️ Duración promedio muy corta ({metrics['Avg Duration (min)']:.0f} min). "
        "Evita scalping, busca trades de mayor timeframe"
    )

# Mostrar recomendaciones
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. {rec}")

print("\n" + "=" * 60)
print("✅ Análisis completado")
print("=" * 60)

# ============================================================
# CELDA 8: Generar Plan de Acción
# ============================================================

print("\n📋 PLAN DE ACCIÓN PERSONALIZADO\n")

# Calcular balance actual
balance_inicial = 10000
balance_actual = balance_inicial + metrics['Net Profit ($)']

print(f"💰 Balance Actual: ${balance_actual:,.2f}")
print(f"🎯 Meta 14 días: ${balance_actual * 1.15:,.2f} (+15%)")
print(f"📈 Ganancia requerida: ${balance_actual * 0.15:,.2f}\n")

# Parámetros recomendados
risk_per_trade = 0.01  # 1%
min_rrr = 2.0
max_trades_per_day = 1
target_win_rate = 0.60

daily_target = (balance_actual * 0.15) / 14
risk_amount = balance_actual * risk_per_trade

print("⚙️ PARÁMETROS RECOMENDADOS:")
print(f"  • Riesgo por trade: {risk_per_trade*100}% (${risk_amount:.2f})")
print(f"  • RRR mínimo: 1:{min_rrr}")
print(f"  • Trades por día: {max_trades_per_day}")
print(f"  • Win rate objetivo: {target_win_rate*100}%")
print(f"  • Ganancia diaria objetivo: ${daily_target:.2f}\n")

# Calcular lotes recomendados
stop_loss_pips = 30
lot_size = risk_amount / (stop_loss_pips * 10)
print(f"📊 TAMAÑO DE LOTE RECOMENDADO:")
print(f"  • Con SL de {stop_loss_pips} pips: {lot_size:.2f} lotes")
print(f"  • TP mínimo: {stop_loss_pips * min_rrr:.0f} pips")

# ============================================================
# CELDA 9: Exportar Resultados
# ============================================================

# Crear resumen en CSV
summary_df = pd.DataFrame([metrics])
summary_df.to_csv('trading_summary.csv', index=False)

# Crear reporte en TXT
with open('trading_report.txt', 'w', encoding='utf-8') as f:
    f.write("REPORTE DE TRADING\n")
    f.write("=" * 60 + "\n\n")
    for key, value in metrics.items():
        f.write(f"{key}: {value}\n")
    f.write("\n" + "=" * 60 + "\n")
    f.write("RECOMENDACIONES\n")
    f.write("=" * 60 + "\n")
    for i, rec in enumerate(recommendations, 1):
        f.write(f"\n{i}. {rec}\n")

print("\n✅ Archivos generados:")
print("  📄 trading_summary.csv")
print("  📄 trading_report.txt")
print("  🖼️ trading_analysis.png")

# Descargar archivos
print("\n📥 Descargando archivos...")
files.download('trading_summary.csv')
files.download('trading_report.txt')
files.download('trading_analysis.png')

print("\n🎉 Análisis completado exitosamente!")
print("💪 ¡Ahora aplica el plan y a pasar esa cuenta!")
# 📊 PLANTILLA TRADING DASHBOARD

## Instrucciones de Uso

### Para Google Sheets:
1. Abre Google Sheets
2. Crea un nuevo archivo llamado "Trading Dashboard 2025"
3. Copia las fórmulas de cada sección a continuación

### Para Excel:
1. Abre Excel
2. Crea nuevo libro llamado "Trading Dashboard 2025"
3. Copia las fórmulas (ajusta formato de fechas si es necesario)

---

## 📋 HOJA 1: REGISTRO DIARIO DE TRADES

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Fecha** | **Hora** | **Par** | **Tipo** | **Lotes** | **Entrada** | **Salida** | **SL** | **TP** | **Pips** | **P&L $** | **Notas** |
| 11/06/25 | 14:08 | EURUSD | Sell | 1.6 | 1.15223 | 1.1532 | 1.153 | 1.1504 | -81 | -129.6 | SL hit |
| | | | | | | | | | | | |

**Fórmulas Clave:**
- **Columna J (Pips):** `=(F2-G2)*10000` (para EUR/USD)
- **Columna K (P&L):** `=J2*E2*10-7` (10=valor pip, 7=comisión promedio)

---

## 📊 HOJA 2: DASHBOARD DE MÉTRICAS

### Balance y Equity

| Métrica | Fórmula | Resultado |
|---------|---------|-----------|
| **Balance Inicial** | Manual | $10,000.00 |
| **Balance Actual** | `=J2+SUM('Registro Diario'!K:K)` | $9,732.72 |
| **Equity** | `=Balance Actual` | $9,732.72 |
| **Ganancia/Pérdida** | `=Balance Actual - Balance Inicial` | -$267.28 |
| **Retorno %** | `=(Balance Actual/Balance Inicial-1)*100` | -2.67% |

---

### Estadísticas de Trading

| Métrica | Fórmula Google Sheets | Resultado |
|---------|----------------------|-----------|
| **Total Trades** | `=COUNTA('Registro Diario'!K2:K)` | 23 |
| **Trades Ganadores** | `=COUNTIF('Registro Diario'!K2:K,">0")` | 10 |
| **Trades Perdedores** | `=COUNTIF('Registro Diario'!K2:K,"<0")` | 13 |
| **Win Rate %** | `=(Trades Ganadores/Total Trades)*100` | 43.48% |
| **Gross Profit** | `=SUMIF('Registro Diario'!K2:K,">0")` | $1,515.86 |
| **Gross Loss** | `=SUMIF('Registro Diario'!K2:K,"<0")` | -$1,487.48 |
| **Profit Factor** | `=Gross Profit/ABS(Gross Loss)` | 1.02 |
| **Avg Winning Trade** | `=AVERAGEIF('Registro Diario'!K2:K,">0")` | $151.59 |
| **Avg Losing Trade** | `=AVERAGEIF('Registro Diario'!K2:K,"<0")` | -$114.42 |
| **Largest Win** | `=MAX('Registro Diario'!K2:K)` | $450.00 |
| **Largest Loss** | `=MIN('Registro Diario'!K2:K)` | -$312.00 |
| **Avg RRR** | `=Avg Winning Trade/ABS(Avg Losing Trade)` | 1.32 |

---

### Métricas de Riesgo

| Métrica | Fórmula | Resultado |
|---------|---------|-----------|
| **Max Drawdown $** | Ver fórmula avanzada abajo | -$312.00 |
| **Max Drawdown %** | `=(Max Drawdown/Balance Inicial)*100` | -3.12% |
| **Comisiones Totales** | `=SUM('Registro Diario'!H2:H)` | -$245.00 |
| **Lotes Promedio** | `=AVERAGE('Registro Diario'!E2:E)` | 1.67 |

**Fórmula Drawdown Avanzada (Columna M en Registro):**
```
=MIN(K2:K$100)
```
Luego en Dashboard: `=MIN('Registro Diario'!M:M)`

---

## 📈 HOJA 3: SEGUIMIENTO DIARIO (Plan 14 Días)

| Día | Fecha | Trades Planeados | Trades Ejecutados | P&L Objetivo | P&L Real | Balance | Cumplió Reglas? | Notas |
|-----|-------|------------------|-------------------|--------------|----------|---------|-----------------|-------|
| 1 | Nov 7 | 1 | | $100 | | $9,832 | ☐ | |
| 2 | Nov 8 | 1 | | $100 | | $9,932 | ☐ | |

**Fórmulas:**
- **Columna G (Balance):** `=G2+F3` (balance anterior + P&L real)
- **Columna H:** Checkbox manual
- **Cumplimiento %:** `=COUNTIF(H2:H15,"☑")/14*100`

---

## 🎯 HOJA 4: ANÁLISIS SEMANAL

### Semana 1 (Nov 7-13)

| Métrica | Objetivo | Real | Diferencia |
|---------|----------|------|------------|
| Trades Totales | 7 | | |
| Win Rate | 60% | | |
| P&L Neto | +$700 | | |
| Comisiones | -$49 | | |
| Balance Final | $10,432 | | |

**Fórmulas:**
- **Columna C (Real):** `=SUMIFS('Registro Diario'!K:K,'Registro Diario'!A:A,">="&DATE(2025,11,7),'Registro Diario'!A:A,"<="&DATE(2025,11,13))`
- **Columna D:** `=C2-B2`

---

## 📊 HOJA 5: GRÁFICOS (Crear manualmente)

### Gráfico 1: Curva de Equity
- **Tipo:** Gráfico de líneas
- **Eje X:** Fecha (Registro Diario columna A)
- **Eje Y:** Balance acumulado
- **Datos:** Balance + P&L acumulado

### Gráfico 2: Win Rate por Semana
- **Tipo:** Gráfico de barras
- **Datos:** Análisis Semanal columna C (Win Rate Real)

### Gráfico 3: P&L por Día
- **Tipo:** Gráfico de columnas
- **Colores:** Verde (positivo), Rojo (negativo)

---

## ⚙️ CONFIGURACIÓN DE FORMATO CONDICIONAL

### En columna K (P&L $):
1. Seleccionar rango K2:K1000
2. Formato > Formato condicional
3. Regla 1: Si valor > 0 → Fondo verde claro
4. Regla 2: Si valor < 0 → Fondo rojo claro

### En columna H (Cumplió Reglas):
1. Si celda = "☑" → Fondo verde
2. Si celda = "☐" → Fondo gris

---

## 🔔 ALERTAS Y VALIDACIONES

### Validación de Riesgo (Columna N en Registro):
```
=IF(ABS(K2)>Balance*0.02,"⚠️ RIESGO EXCEDIDO","✅ OK")
```

### Alerta de Drawdown:
```
=IF(Balance Actual < Balance Inicial*0.95,"🚨 DRAWDOWN >5%","")
```

---

## 📥 IMPORTAR DATOS DESDE CSV

1. En Google Sheets: `Archivo > Importar > Cargar`
2. Seleccionar tu CSV de trading
3. Configurar:
   - Separador: Coma
   - Convertir texto a números
4. Mapear columnas a formato de Registro Diario

---

## 💾 RESPALDO AUTOMÁTICO

### Google Sheets (Recomendado):
- Se guarda automáticamente en la nube
- Acceso desde móvil/escritorio
- Compartir con mentor si aplica

### Excel:
- Guardar como: `Trading_Dashboard_2025.xlsx`
- Hacer backup semanal en Dropbox/Google Drive

---

## 📱 ACCESO MÓVIL

1. Descargar Google Sheets App
2. Abrir dashboard
3. Registrar trades en tiempo real
4. Ver métricas en vivo

---

## 🎨 PERSONALIZACIÓN

Ajusta colores, fuentes y layout a tu preferencia. Lo importante es:
- ✅ Fácil de actualizar diariamente
- ✅ Métricas visibles de un vistazo
- ✅ Motivante (ver progreso)
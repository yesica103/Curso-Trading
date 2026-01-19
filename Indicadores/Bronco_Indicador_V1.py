//@version=5
indicator("MC + Key Levels (Safe)", overlay=true)

// MANIPULATION CANDLE
prevHigh = high[1]
prevLow = low[1]

bullishMC = low < prevLow and high > prevHigh and close > prevHigh
bearishMC = high > prevHigh and low < prevLow and close < prevLow

barcolor(bullishMC or bearishMC ? color.blue : na)

// OFFSETS
lineLen = 200
labelGap = 5

// HTF LEVELS
pwHigh = request.security(syminfo.tickerid, "W", high[1], barmerge.gaps_off, barmerge.lookahead_off)
pdHigh = request.security(syminfo.tickerid, "D", high[1], barmerge.gaps_off, barmerge.lookahead_off)
dailyOpen = request.security(syminfo.tickerid, "D", open, barmerge.gaps_off, barmerge.lookahead_off)

// ====================
// PWH
// ====================
var line pwhLine = na
var label pwhLabel = na

if na(pwhLine)
    pwhLine := line.new(bar_index, pwHigh, bar_index + lineLen, pwHigh, color=color.orange, width=2)
    pwhLabel := label.new(bar_index, pwHigh, "PWH", style=label.style_label_right, color=color.orange, textcolor=color.white, size=size.tiny)
else
    line.set_y1(pwhLine, pwHigh)
    line.set_y2(pwhLine, pwHigh)
    line.set_x2(pwhLine, bar_index + lineLen)
    label.set_y(pwhLabel, pwHigh)
    label.set_x(pwhLabel, bar_index + lineLen + labelGap)

// ====================
// PDH
// ====================
var line pdhLine = na
var label pdhLabel = na

if na(pdhLine)
    pdhLine := line.new(bar_index, pdHigh, bar_index + lineLen, pdHigh, color=color.gray, width=1)
    pdhLabel := label.new(bar_index, pdHigh, "PDH", style=label.style_label_right, color=color.gray, textcolor=color.white, size=size.tiny)
else
    line.set_y1(pdhLine, pdHigh)
    line.set_y2(pdhLine, pdHigh)
    line.set_x2(pdhLine, bar_index + lineLen)
    label.set_y(pdhLabel, pdHigh)
    label.set_x(pdhLabel, bar_index + lineLen + labelGap)

// ====================
// DAILY OPEN
// ====================
var line doLine = na
var label doLabel = na

if na(doLine)
    doLine := line.new(bar_index, dailyOpen, bar_index + lineLen, dailyOpen, color=color.blue, width=1, style=line.style_dotted)
    doLabel := label.new(bar_index, dailyOpen, "Daily Open", style=label.style_label_right, color=color.blue, textcolor=color.white, size=size.tiny)
else
    line.set_y1(doLine, dailyOpen)
    line.set_y2(doLine, dailyOpen)
    line.set_x2(doLine, bar_index + lineLen)
    label.set_y(doLabel, dailyOpen)
    label.set_x(doLabel, bar_index + lineLen + labelGap)
    
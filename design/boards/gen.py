import json, datetime
# QUIZLUX v2 — navy + champagne gold
BG="#0B1428"; SF="#152747"; SF2="#1C345A"; GD="#C6A45A"; GD2="#E5CD8F"; BL="#4389D9"
TX="#F5F5F2"; MU="#AABBD5"; LINE="#26426B"; OK="#4CC38A"; ER="#E26D6D"
GDA="rgba(198,164,90,.14)"; GDB="rgba(198,164,90,.40)"
F="font-family:Manrope,sans-serif"
SERIF="font-family:'Cormorant Garamond',Georgia,serif"

def mark(s=28):
    return f'<svg aria-hidden="true" width="{s}" height="{s}" viewBox="0 0 32 32" fill="none"><circle cx="15" cy="15" r="10" stroke="{GD}" stroke-width="2.6"/><path d="M20.5 20.5L27 27" stroke="{GD}" stroke-width="2.6" stroke-linecap="round"/></svg>'
def word(fs=16, ls=0.2):
    return f'<span style="{F}; font-weight:800; letter-spacing:{ls}em; font-size:{fs}px; color:{TX}">QUIZ<span style="color:{GD}">LUX</span></span>'
def logo(fs=16, s=28): return f'<div style="display:flex; align-items:center; gap:8px">{mark(s)}{word(fs)}</div>'

def card(inner, extra="", bg=SF, border="transparent"):
    return f'<div style="background:{bg}; border:1px solid {border}; border-radius:16px; padding:14px; display:flex; flex-direction:column; gap:10px; {extra}">{inner}</div>'
def btn(label, kind="gold", extra=""):
    if kind=="gold": st=f"background:{GD}; color:{BG}; border:1px solid {GD}"
    elif kind=="line": st=f"background:transparent; color:{TX}; border:1px solid {LINE}"
    elif kind=="goldline": st=f"background:transparent; color:{GD2}; border:1px solid {GDB}"
    else: st=f"background:transparent; color:{MU}; border:1px solid transparent"
    return f'<button type="button" style="{st}; {F}; font-weight:800; font-size:14px; letter-spacing:0.08em; text-transform:uppercase; min-height:52px; border-radius:12px; padding:0 18px; cursor:pointer; {extra}">{label}</button>'
def sbtn(label, kind="line", extra=""): return btn(label, kind, "min-height:44px; font-size:12px; padding:0 14px; "+extra)
def label(t, c=MU): return f'<div style="font-size:11px; letter-spacing:0.14em; text-transform:uppercase; color:{c}; font-weight:700">{t}</div>'
def h(t, size=20, c=TX): return f'<div style="{F}; font-weight:800; font-size:{size}px; line-height:1.2; color:{c}">{t}</div>'
def p(t, c=MU, size=13): return f'<div style="font-size:{size}px; line-height:1.4; color:{c}">{t}</div>'
def chip(t, on=False):
    st = f"background:{GDA}; color:{GD2}; border:1px solid {GD}" if on else f"background:{SF}; color:{MU}; border:1px solid {LINE}"
    return f'<button type="button" style="{st}; {F}; font-size:13px; font-weight:700; min-height:44px; border-radius:22px; padding:0 16px; cursor:pointer">{t}</button>'
def row(inner, gap=8, extra=""): return f'<div style="display:flex; gap:{gap}px; align-items:center; {extra}">{inner}</div>'
def bar(pct, hgt=6, color=GD): return f'<div style="height:{hgt}px; background:{SF2}; border-radius:{hgt}px; overflow:hidden"><div style="width:{pct}%; height:100%; background:{color}"></div></div>'
def avatar(letter, size=44, ring=False, color=BL):
    rg = f"box-shadow:0 0 0 2px {BG}, 0 0 0 4px {GD};" if ring else ""
    return f'<div aria-hidden="true" style="width:{size}px; height:{size}px; border-radius:50%; background:{color}; color:{TX}; display:flex; align-items:center; justify-content:center; {F}; font-weight:800; font-size:{int(size*0.42)}px; flex:none; {rg}">{letter}</div>'

ICONS={
 "space":'<circle cx="12" cy="12" r="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(-20 12 12)"/>',
 "cinema":'<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M8 6l-2 4M13 6l-2 4M18 6l-2 4"/>',
 "football":'<circle cx="12" cy="12" r="9"/><path d="M12 8l3 2-1 3.5h-4L9 10z"/>',
 "history":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
 "science":'<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/>',
 "music":'<path d="M9 18V6l10-2v12"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="16" r="2"/>',
 "games":'<rect x="3" y="8" width="18" height="9" rx="4"/><path d="M8 10.5v4M6 12.5h4"/><circle cx="16" cy="12.5" r=".8"/>',
 "tv":'<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M9 21h6"/>',
 "olympic":'<circle cx="8" cy="10" r="4"/><circle cx="16" cy="10" r="4"/><circle cx="12" cy="15" r="4"/>',
}
def icon(name, s=20, c=GD2): return f'<svg aria-hidden="true" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
def ibox(name): return f'<div style="width:36px; height:36px; border-radius:10px; background:{SF2}; display:flex; align-items:center; justify-content:center; flex:none">{icon(name)}</div>'

NAVI={
 "Home":'<path d="M4 11l8-7 8 7v9H4z"/>',
 "Topics":'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 "Duels":'<path d="M5 6l6 6-6 6M19 6l-6 6 6 6"/>',
 "Profile":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
}
def nav(active):
    b=""
    for i in ["Home","Topics","Duels","Profile"]:
        on = i==active; c = GD if on else MU
        b+=(f'<button type="button" {"aria-current=\"page\"" if on else ""} style="flex:1; background:transparent; border:none; border-top:2px solid {GD if on else "transparent"}; min-height:64px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px; color:{c}; {F}; font-size:11px; font-weight:{800 if on else 600}; letter-spacing:0.06em; cursor:pointer">'
            f'<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{NAVI[i]}</svg>{i}</button>')
    return f'<nav aria-label="Main" style="display:flex; background:{SF}; border-top:1px solid {LINE}">{b}</nav>'

def page(title, body, bottom="", pad="20px 16px 12px", bg=BG):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
body{{margin:0}}
a{{color:{BL}}}a:hover{{color:{TX}}}
</style>
</helmet>
<div style="width:390px; height:844px; box-sizing:border-box; background:{bg}; color:{TX}; font-family:Manrope,sans-serif; display:flex; flex-direction:column">
<div style="flex:1; overflow:hidden; padding:{pad}; display:flex; flex-direction:column; gap:14px">
{body}
</div>
{bottom}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":844}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
S={}

# 0 Brand
def sw(name, hx, txt="#F5F5F2"): return f'<div style="flex:1; min-width:0"><div style="height:44px; border-radius:10px; background:{hx}; border:1px solid {LINE}"></div><div style="font-size:11px; font-weight:700; color:{TX}; margin-top:6px">{name}</div><div style="font-size:11px; color:{MU}">{hx}</div></div>'
def appicon(s):
    return f'<div aria-hidden="true" style="width:{s}px; height:{s}px; border-radius:{int(s*0.23)}px; background:{BG}; border:1px solid {LINE}; display:flex; align-items:center; justify-content:center">{mark(int(s*0.62))}</div>'
S["Brand.dc.html"]=("Brand", page("Brand",
 label("Brand system v2",GD)
 + card(f'<div style="padding:4px 0">{logo(28,44)}</div>'+p("Wordmark: Manrope 800, wide tracking. «LUX» in champagne gold. Mark: a ring with a tail — a Q, and a countdown timer.",MU,12),"gap:6px",SF)
 + f'<div style="font-family:Cormorant Garamond,Georgia,serif; font-weight:700; font-size:20px; letter-spacing:0.28em; color:{GD2}; text-align:center">THE GAME OF KNOWLEDGE</div>'
 + label("App icon")
 + row(appicon(88)+appicon(56)+appicon(36)+appicon(24),16,"align-items:flex-end")
 + label("Palette")
 + row(sw("Midnight",BG)+sw("Deep blue",SF)+sw("Royal",SF2),10,"align-items:flex-start")
 + row(sw("Champagne",GD)+sw("Light gold",GD2)+sw("Bright blue",BL),10,"align-items:flex-start")
 + row(sw("Ivory",TX)+sw("Slate",MU)+sw("Correct",OK),10,"align-items:flex-start")
 + label("Type")
 + row(f'<div style="{F}; font-weight:800; font-size:24px; color:{TX}">Aa Manrope</div><div style="{SERIF}; font-weight:700; font-size:22px; color:{GD2}; margin-left:auto">Cormorant Garamond</div>',10)
 ))

# 1 Splash
S["Splash.dc.html"]=("Splash", page("Splash",
 f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px">{mark(104)}{word(34,0.22)}<div style="width:48px; height:1px; background:{GD}"></div><div style="{SERIF}; font-weight:700; font-size:17px; letter-spacing:0.3em; color:{GD2}; text-align:center">THE GAME<br>OF KNOWLEDGE</div></div>'
 + f'<div style="padding:0 60px 28px">{bar(35,3)}</div>', pad="20px 16px 0"))

# 2 Home
S["Main.dc.html"]=("Home", page("Home",
 row(logo(15,26)+f'<div style="margin-left:auto; text-align:right; min-width:92px"><div style="font-size:12px; font-weight:800; color:{TX}">Level 7</div><div style="font-size:11px; color:{GD2}; font-weight:600; margin-bottom:4px">2,340 XP</div>{bar(62,4)}</div>'+avatar("A",40,True),12,"")
 + card(
     row(label("Your turn",GD)+f'<div style="margin-left:auto; font-size:12px; color:{MU}; font-weight:600">Round 2 of 3</div>',8)
     + row(avatar("M",48)+f'<div style="flex:1; min-width:0">{h("maya_r",17)}{p("Space · 2 rounds left")}</div>'
           +f'<div style="text-align:right"><div style="{F}; font-weight:800; font-size:28px; color:{TX}; line-height:1">5<span style="color:{MU}"> – </span>4</div><div style="font-size:11px; color:{GD2}; font-weight:700; margin-top:2px">You lead</div></div>',12)
     + btn("Play now"), "gap:12px", SF2, GDB)
 + card(
     row(f'<div style="flex:1">{h("Daily 10",17)}{p("Ten questions. One shot a day.")}</div>'+f'<div style="background:{GDA}; border:1px solid {GDB}; color:{GD2}; font-size:12px; font-weight:800; border-radius:14px; padding:5px 10px">+150 XP</div>',10)
     + row(f'<div style="flex:1">{bar(0,6)}</div><div style="font-size:12px; color:{MU}; font-weight:700">0 / 10</div>',10)
     + sbtn("Start challenge","goldline","width:100%"))
 + row(label("Your topics")+f'<button type="button" style="margin-left:auto; background:transparent; border:none; color:{BL}; font-size:12px; font-weight:700; min-height:32px; cursor:pointer">Discover more</button>',8)
 + f'<div style="display:flex; gap:10px">'
   + "".join(f'<button type="button" style="flex:1; min-width:0; background:{SF}; border:1px solid {LINE}; border-radius:14px; padding:10px; text-align:left; cursor:pointer; display:flex; flex-direction:column; gap:6px; min-height:44px">{icon(ic,18)}<span style="{F}; font-weight:800; font-size:13px; color:{TX}">{nm}</span><span style="font-size:11px; color:{GD2}; font-weight:700">Lv {lv}</span>{bar(pc,3)}</button>' for nm,ic,lv,pc in [("Space","space",5,70),("Cinema","cinema",3,40),("Football","football",6,85)])
   + '</div>'
 + label("Friends")
 + card(row(avatar("L",34,False,SF2)+f'<div style="flex:1; font-size:13px; color:{TX}"><b>leo_k</b> beat you in Flags &amp; Capitals</div>'+sbtn("Rematch"),10),"padding:10px 12px")
 + card(row(avatar("S",34,False,SF2)+f'<div style="flex:1; font-size:13px; color:{TX}"><b>sara.m</b> reached Level 10</div>'+sbtn("Cheer","ghost"),10),"padding:10px 12px"),
 nav("Home")))

# 3 Topics
def tile(name, ic, lvl, pc):
    sub = f'<span style="font-size:11px; color:{GD2}; font-weight:700">{lvl}</span>' if lvl!="New" else f'<span style="font-size:11px; color:{MU}; font-weight:700">New</span>'
    return f'<button type="button" style="background:{SF}; border:1px solid {LINE}; border-radius:14px; padding:12px; min-height:44px; text-align:left; cursor:pointer; display:flex; flex-direction:column; gap:8px">{row(ibox(ic)+f"<div style=\"min-width:0\"><div style=\"{F}; font-weight:800; font-size:14px; color:{TX}\">{name}</div>{sub}</div>",10)}{bar(pc,3)}</button>'
def grid(items): return f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">{"".join(tile(*i) for i in items)}</div>'
S["Topics.dc.html"]=("Topics", page("Topics",
 row(h("Topics",24)+f'<div style="margin-left:auto; font-size:12px; color:{MU}; font-weight:700">32 topics</div>')
 + f'<label style="display:flex; flex-direction:column; gap:6px; font-size:11px; color:{MU}; font-weight:700; letter-spacing:0.14em; text-transform:uppercase">Search topics<input type="search" placeholder="Try &quot;Olympics&quot;" style="background:{SF}; border:1px solid {LINE}; border-radius:12px; min-height:48px; padding:0 14px; color:{TX}; font-size:15px; font-family:Manrope,sans-serif; letter-spacing:0; text-transform:none"></label>'
 + row(chip("All",True)+chip("Knowledge")+chip("Culture")+chip("Sports"),8,"overflow:hidden")
 + card(label("Featured this week",GD)+row(ibox("space")+f'<div style="flex:1">{h("Space",18)}{p("Planets, missions and the first 60 years of spaceflight")}</div>',12)+row(f'<div style="font-size:12px; color:{GD2}; font-weight:700">Level 5 · 70% to Level 6</div>',8)+bar(70,4), "gap:10px", SF2, GDB)
 + label("Recently played") + grid([("Cinema","cinema","Level 3",40),("Football","football","Level 6",85)])
 + label("Favourites") + grid([("World History","history","Level 3",35),("Flags &amp; Capitals","globe","Level 4",55)])
 + label("Explore") + grid([("Music","music","Level 1",10),("Video Games","games","New",0)]),
 nav("Topics")))

# 4 Duels
def drow(av, name, topic, score, status, action):
    return card(row(avatar(av,40,False,SF2)+f'<div style="flex:1; min-width:0">{h(name,15)}{p(topic,MU,12)}</div>'+f'<div style="text-align:right"><div style="{F}; font-weight:800; font-size:18px; color:{TX}">{score}</div><div style="font-size:11px; color:{MU}">{status}</div></div>'+action,10),"padding:10px 12px")
S["Duels.dc.html"]=("Duels", page("Duels",
 row(h("Duels",24)+f'<div style="margin-left:auto">{sbtn("+ New duel","goldline")}</div>')
 + row(chip("Active · 4",True)+chip("Challenges")+chip("Finished"),8)
 + label("Your move · 2",GD)
 + drow("M","maya_r","Space · Round 2 of 3","5–4","You lead",sbtn("Play","gold"))
 + drow("T","tom_88","Football · Round 1 of 3","1–2","Behind",sbtn("Play","gold"))
 + label("Waiting for opponent · 1")
 + drow("L","leo_k","Cinema · Round 3 of 3","7–6","Their move",sbtn("Nudge","ghost"))
 + label("Finished")
 + card(row(avatar("S",40,False,SF2)+f'<div style="flex:1; min-width:0">{h("sara.m",15)}{p("World History",MU,12)}</div>'+f'<div style="text-align:right"><div style="{F}; font-weight:800; font-size:13px; color:{GD}">WON</div><div style="{F}; font-weight:800; font-size:16px; color:{TX}">9–7</div></div>'+sbtn("Rematch"),10),"padding:10px 12px",SF,GDB)
 + card(row(avatar("L",40,False,SF2)+f'<div style="flex:1; min-width:0">{h("leo_k",15)}{p("Flags &amp; Capitals",MU,12)}</div>'+f'<div style="text-align:right"><div style="{F}; font-weight:800; font-size:13px; color:{MU}">LOST</div><div style="{F}; font-weight:800; font-size:16px; color:{TX}">6–8</div></div>'+sbtn("Rematch"),10),"padding:10px 12px")
 + label("Open challenges")
 + card(row(f'<div style="flex:1">{h("90s Movies Marathon",14)}{p("by sara.m · 20 questions",MU,12)}</div>'+sbtn("Join"),10),"padding:10px 12px"),
 nav("Duels")))

# 5 Question
def ans(letter, t, st="idle"):
    cfg={
     "idle":    (SF, LINE, TX, SF2, GD, ""),
     "selected":(GDA, GD, TX, GD, BG, ""),
     "correct": ("rgba(76,195,138,.16)", OK, TX, OK, BG, "Correct"),
     "wrong":   ("rgba(226,109,109,.14)", ER, TX, ER, BG, "Your answer"),
     "off":     (SF, "transparent", MU, SF2, MU, ""),
    }[st]
    bgc,bd,tc,bb,bt,tail=cfg
    op = "opacity:.6;" if st=="off" else ""
    tl = f'<span style="font-size:12px; font-weight:800; color:{OK if st=="correct" else ER}">{tail}</span>' if tail else ""
    return f'<button type="button" style="background:{bgc}; border:1.5px solid {bd}; color:{tc}; {op} min-height:56px; border-radius:14px; padding:0 14px; {F}; font-size:16px; font-weight:700; text-align:left; cursor:pointer; display:flex; align-items:center; gap:12px"><span style="width:30px; height:30px; border-radius:50%; background:{bb}; color:{bt}; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex:none">{letter}</span><span style="flex:1">{t}</span>{tl}</button>'
def ring(sec=7, total=10, s=72):
    r=30; c=2*3.14159*r; off=c*(1-sec/total)
    return f'<div role="img" aria-label="Time left: {sec} of {total} seconds" style="position:relative; width:{s}px; height:{s}px; flex:none"><svg width="{s}" height="{s}" viewBox="0 0 72 72" style="transform:rotate(-90deg)"><circle cx="36" cy="36" r="{r}" stroke="{SF2}" stroke-width="5" fill="none"/><circle cx="36" cy="36" r="{r}" stroke="{GD}" stroke-width="5" fill="none" stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}"/></svg><div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; {F}; font-weight:800; font-size:24px; color:{TX}">{sec}</div></div>'
def seg(done, total, cur):
    return '<div style="display:flex; gap:6px">'+"".join(f'<div style="flex:1; height:4px; border-radius:2px; background:{GD if i<done else (GD2 if i==cur else SF2)}"></div>' for i in range(total))+'</div>'
S["Question.dc.html"]=("Question", page("Question",
 row(f'<button type="button" aria-label="Leave duel" style="background:transparent; border:none; color:{MU}; min-width:44px; min-height:44px; cursor:pointer; margin-left:-10px"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>'
     +label("Space · Round 2",GD2)+f'<div style="margin-left:auto; background:{GDA}; border:1px solid {GDB}; color:{GD2}; font-size:12px; font-weight:800; border-radius:14px; padding:5px 10px">+25 XP</div>',6)
 + row(f'<div style="display:flex; align-items:center; gap:10px; flex:1">{avatar("A",40,True)}<div style="{F}; font-weight:800; font-size:26px; color:{TX}">6</div></div>'+ring(7,10)+f'<div style="display:flex; align-items:center; gap:10px; flex:1; justify-content:flex-end"><div style="{F}; font-weight:800; font-size:26px; color:{MU}">5</div>{avatar("M",40)}</div>',8)
 + f'<div>{seg(2,4,2)}<div style="font-size:11px; color:{MU}; font-weight:700; margin-top:6px; letter-spacing:0.1em">QUESTION 3 OF 4</div></div>'
 + f'<div style="{F}; font-weight:800; font-size:23px; line-height:1.25; color:{TX}; margin:4px 0 2px">Which planet takes longer to rotate once on its axis than to orbit the Sun?</div>'
 + f'<div style="display:flex; flex-direction:column; gap:10px">{ans("A","Mercury","off")}{ans("B","Venus","correct")}{ans("C","Mars","wrong")}{ans("D","Uranus","off")}</div>'
 + card(p("Venus rotates once in about 243 Earth days and orbits the Sun in about 225.",TX,13)+row(p('Sources: <a href="https://ntrs.nasa.gov/api/citations/19790012783/downloads/19790012783.pdf">NASA</a> · <a href="https://eso.org/public/outreach/eduoff/vt-2004/Background/Infol2/EIS-D3.html">ESO</a>',MU,12)+f'<div style="margin-left:auto">{sbtn("Report","ghost")}</div>',8),"gap:6px; padding:10px 12px")
 ))

# 6 Answer states
S["States.dc.html"]=("Answer states", page("Answer states",
 label("Answer states",GD) + h("One component, five states",20)
 + f'<div style="display:flex; flex-direction:column; gap:12px">'
 + f'<div>{label("Unselected")}<div style="margin-top:6px">{ans("A","The Nile")}</div></div>'
 + f'<div>{label("Selected — gold, before the reveal")}<div style="margin-top:6px">{ans("B","The Amazon","selected")}</div></div>'
 + f'<div>{label("Correct — green + word")}<div style="margin-top:6px">{ans("C","The Nile","correct")}</div></div>'
 + f'<div>{label("Incorrect — red + word")}<div style="margin-top:6px">{ans("D","The Yangtze","wrong")}</div></div>'
 + f'<div>{label("Disabled — after the reveal")}<div style="margin-top:6px">{ans("A","The Congo","off")}</div></div>'
 + '</div>'
 + label("Timer")
 + row(ring(10,10,60)+ring(7,10,60)+ring(3,10,60)+ring(0,10,60),12)
 + p("State is never colour alone: Correct and Your answer are written out, and the letter badge changes.",MU,12)
 ))

# 7 Result
def stat3(n,l): return f'<div style="flex:1; text-align:center">{h(n,20)}<div style="font-size:11px; color:{MU}; font-weight:600; margin-top:2px">{l}</div></div>'
S["Result.dc.html"]=("Duel result", page("Duel result",
 f'<div style="text-align:center">{label("Victory",GD)}</div>'
 + f'<div style="display:flex; align-items:center; justify-content:center; gap:16px; padding:14px 0; border-radius:20px; background:radial-gradient(circle at 50% 50%, rgba(198,164,90,.14), rgba(198,164,90,0) 70%)">{avatar("A",60,True)}<div style="{F}; font-weight:800; font-size:54px; color:{TX}; line-height:1">9<span style="color:{MU}"> – </span>7</div>{avatar("M",60)}</div>'
 + f'<div style="text-align:center">{h("You beat maya_r",20)}{p("Head-to-head: you 4 · maya_r 2")}</div>'
 + card(row(f'<div style="{F}; font-weight:800; font-size:22px; color:{GD}">+120 XP</div><div style="margin-left:auto; font-size:12px; color:{MU}; font-weight:700">Level 7</div>',8)+bar(82,6)+row(f'<div style="font-size:12px; color:{GD2}; font-weight:700">2,460 / 2,800 XP</div><div style="margin-left:auto; font-size:12px; color:{MU}">Level 8 next</div>',8),"gap:8px",SF2,GDB)
 + f'<div style="display:flex; background:{SF}; border-radius:16px; padding:14px 8px">{stat3("9 / 12","Correct")}{stat3("6.2 s","Avg. time")}{stat3("5","Best streak")}</div>'
 + row(p("Space rating",MU,12)+f'<div style="margin-left:auto; font-size:13px; font-weight:800; color:{GD2}">1486 → 1500 (+14)</div>',8)
 + f'<div style="display:flex; flex-direction:column; gap:10px; margin-top:auto">{btn("Rematch")}{btn("Play again","line")}{btn("Back to home","ghost","min-height:44px")}</div>'
 ))

# 8 Profile
def trow(t, ic, lvl, pc): return f'<div style="display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid {LINE}">{ibox(ic)}<div style="flex:1"><div style="{F}; font-weight:800; font-size:14px; color:{TX}">{t}</div><div style="font-size:11px; color:{GD2}; font-weight:700; margin-bottom:4px">{lvl}</div>{bar(pc,3)}</div></div>'
def medal(t, on=True):
    c = GD if on else LINE
    return f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; gap:6px"><div style="width:48px; height:48px; border-radius:50%; border:2px solid {c}; background:{GDA if on else "transparent"}; display:flex; align-items:center; justify-content:center"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg></div><div style="font-size:10px; color:{MU if on else LINE}; font-weight:700; text-align:center">{t}</div></div>'
def hist(res, opp, topic, sc):
    c = GD if res=="W" else MU
    return f'<div style="display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid {LINE}"><div style="width:26px; height:26px; border-radius:8px; border:1px solid {c}; color:{c}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800">{res}</div><div style="flex:1; font-size:13px; color:{TX}"><b>{opp}</b> · {topic}</div><div style="{F}; font-weight:800; font-size:14px; color:{TX}">{sc}</div></div>'
S["Profile.dc.html"]=("Profile", page("Profile",
 row(avatar("A",64,True)+f'<div style="flex:1">{h("alex_q",22)}{p("Level 7 · Space specialist",GD2,13)}{p("31 followers · 24 following",MU,12)}</div>',16,"padding-left:4px")
 + card(row(f'<div style="font-size:12px; color:{MU}; font-weight:700">Level 7</div><div style="margin-left:auto; font-size:12px; color:{GD2}; font-weight:700">2,340 / 2,800 XP</div>',8)+bar(83,6),"gap:8px;padding:12px 14px")
 + f'<div style="display:flex; background:{SF}; border-radius:16px; padding:12px 6px">{stat3("18,420","Total XP")}{stat3("62%","Win rate")}{stat3("61","Games")}{stat3("12","Day streak")}</div>'
 + label("Favourite topics")
 + card(trow("Space","space","Level 5",70)+trow("Football","football","Level 6",85),"gap:0; padding:2px 14px")
 + label("Achievements")
 + f'<div style="display:flex; gap:8px">{medal("7-day streak")}{medal("100 duels")}{medal("Space Lv 5")}{medal("Perfect round",False)}</div>'
 + label("Match history")
 + card(hist("W","maya_r","Space","9–7")+hist("L","leo_k","Flags","6–8")+hist("W","sara.m","History","9–7"),"gap:0; padding:0 14px"),
 nav("Profile")))

# 9 Create
def field(lbl, inner): return f'<div style="display:flex; flex-direction:column; gap:8px">{label(lbl)}{inner}</div>'
S["CreateChallenge.dc.html"]=("Create a challenge", page("Create a challenge",
 row(f'<button type="button" aria-label="Back" style="background:transparent; border:none; color:{TX}; min-width:44px; min-height:44px; cursor:pointer; margin-left:-10px"><svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>'+h("Create a challenge",22),6)
 + p("Build your own quiz from verified questions and dare people to beat your score.")
 + f'<label style="display:flex; flex-direction:column; gap:6px; font-size:11px; color:{MU}; font-weight:700; letter-spacing:0.14em; text-transform:uppercase">Challenge name<input type="text" value="Solar System Sprint" style="background:{SF}; border:1px solid {LINE}; border-radius:12px; min-height:48px; padding:0 14px; color:{TX}; font-size:15px; font-family:Manrope,sans-serif; text-transform:none; letter-spacing:0"></label>'
 + field("Topics (up to 3)", row(chip("Space",True)+chip("Science",True)+chip("World History")+chip("+ More"),8,"flex-wrap:wrap"))
 + field("Questions", row(chip("10")+chip("20",True)+chip("30")))
 + field("Difficulty", row(chip("Mixed",True)+chip("Hard only")+chip("Rising")))
 + field("Who can play", row(chip("Friends")+chip("Followers",True)+chip("Everyone")))
 + field("Open for", row(chip("24 hours")+chip("7 days",True)+chip("No limit")))
 + f'<div style="display:flex; flex-direction:column; gap:10px; margin-top:auto">{btn("Play first, then publish")}{p("You set the score to beat. Players see the ranking when they finish.",MU,12)}</div>'
 ))

order=["Brand.dc.html","Splash.dc.html","Main.dc.html","Topics.dc.html","Duels.dc.html","Question.dc.html","States.dc.html","Result.dc.html","Profile.dc.html","CreateChallenge.dc.html"]
titles={"Brand.dc.html":"Brand","Splash.dc.html":"Splash","Main.dc.html":"Home","Topics.dc.html":"Topics","Duels.dc.html":"Duels","Question.dc.html":"Gameplay","States.dc.html":"Answer states","Result.dc.html":"Result","Profile.dc.html":"Profile","CreateChallenge.dc.html":"Create a challenge"}
boards={k:{"x":i*470,"y":0,"w":390,"h":844,"title":f"{i}. {titles[k]}" if i else "Brand"} for i,k in enumerate(order)}
canvas={"v":3,"createdOnFiles":{"v":1,"at":datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")},"title":"QUIZLUX — main screens (v2)","launch":{"view":"canvas"},"pages":[],"boards":boards,"order":order,
 "notes":{"t1":{"x":0,"y":-300,"text":"QUIZLUX · The game of knowledge · v2","kind":"title1","maxW":4700},
          "n1":{"x":4720,"y":0,"w":360,"text":"Working draft v2. Midnight blue + champagne gold, Manrope. One gold action per screen. Names, levels and scores are sample data. The question shown passed the fact pipeline (sources: NASA, ESO). The QUIZLUX name still needs a domain and trademark check."}},
 "designSystems":[]}
json.dump(canvas, open("project/canvas.json","w"), ensure_ascii=False, indent=1)
for k,(t,html) in S.items(): open("project/"+k,"w").write(html)
print(len(S), "files")

#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

def r0(x): return math.floor(x + 0.5)
def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def burnPlan(lengthCm, minPerCm, packCount):
    bad = pos([lengthCm, minPerCm, packCount], "length, burn rate and pack count must be positive")
    if bad: return bad
    minutes = r0(lengthCm * minPerCm)
    hours = r1(packCount * lengthCm * minPerCm / 60)
    return {"minutes": minutes, "hours": jsnum(hours)}

def roomPlan(roomM2, m2PerStick, packSize):
    bad = pos([roomM2, m2PerStick, packSize], "room, coverage and pack size must be positive")
    if bad: return bad
    sticks = math.ceil(roomM2 / m2PerStick)
    sessions = math.floor(packSize / sticks)
    return {"sticks": sticks, "sessions": sessions}

def yearPlan(sessionsWeek, sticksEach, packPrice, packSize):
    bad = pos([sessionsWeek, sticksEach, packPrice, packSize], "pace, sticks, price and pack size must be positive")
    if bad: return bad
    sticksYear = sessionsWeek * sticksEach * 52
    packsYear = sticksYear / packSize
    return {"sticksYear": r0(sticksYear), "packsYear": jsnum(r2(packsYear)), "costYear": jsnum(r2(packsYear * packPrice))}

def plural(n, w): return fmt(n) + " " + w + ("" if n == 1 else "s")

def renderBurn(r, lengthCm, minPerCm, packCount):
    return "A " + fmt(lengthCm) + " cm stick burns about " + plural(r["minutes"], "minute") + " at a labeled " + fmt(minPerCm) + " minutes per centimeter - a pack of " + fmt(packCount) + " is about " + plural(r["hours"], "hour") + "."

def renderRoom(r, roomM2, m2PerStick, packSize):
    base = "Scenting a " + fmt(roomM2) + " m² room takes " + plural(r["sticks"], "stick") + " at a labeled " + fmt(m2PerStick) + " m² each"
    if r["sessions"] == 0: return base + " - a " + fmt(packSize) + "-stick pack covers no full sessions."
    return base + " - a " + fmt(packSize) + "-stick pack covers " + plural(r["sessions"], "session") + "."

def renderYear(r, sessionsWeek, sticksEach):
    return plural(sessionsWeek, "session") + " a week of " + plural(sticksEach, "stick") + " is " + plural(r["sticksYear"], "stick") + " a year - about " + plural(r["packsYear"], "pack") + ", " + fmt(r["costYear"]) + " at your price."

cases = []
burn_args = [(21,2,20),(15,2,20),(21,2.5,30),(25,2,40),(21,1.5,20),(10,2,15),
             (21,2,1),(30,2.2,50),(18,1.8,25),(21,3,20),(12,2,10),(27,2.4,35),
             (0,2,20),(21,0,20),(21,2,0)]
for a in burn_args:
    r = burnPlan(*a)
    case = {"fn": "burnPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderBurn(r, a[0], a[1], a[2])
    cases.append(case)
room_args = [(30,15,20),(20,15,20),(45,15,30),(25,10,20),(60,15,20),(15,15,20),
             (35,12,40),(50,15,10),(28,14,20),(40,15,25),(22,11,30),(55,15,45),
             (100,15,5),(0,15,20),(30,0,20),(30,15,0)]
for a in room_args:
    r = roomPlan(*a)
    case = {"fn": "roomPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderRoom(r, a[0], a[1], a[2])
    cases.append(case)
year_args = [(3,2,3,20),(2,1,4,20),(5,2,2.5,30),(1,1,3,20),(7,3,2,20),(4,2,3.5,25),
             (1,2,3,20),(6,2,4,40),(3,3,2.8,20),(2,2,5,15),(5,1,3,30),(4,4,3.2,24),
             (0,2,3,20),(3,0,3,20),(3,2,0,20),(3,2,3,0)]
for a in year_args:
    r = yearPlan(*a)
    case = {"fn": "yearPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderYear(r, a[0], a[1])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")

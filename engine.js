// Incense math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r0(x){ return Math.round(x); }
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function burnPlan(lengthCm, minPerCm, packCount){
  var bad = pos([lengthCm, minPerCm, packCount], "length, burn rate and pack count must be positive");
  if (bad) return bad;
  var minutes = r0(lengthCm * minPerCm);
  var hours = r1(packCount * lengthCm * minPerCm / 60);
  return { minutes: minutes, hours: hours };
}
function roomPlan(roomM2, m2PerStick, packSize){
  var bad = pos([roomM2, m2PerStick, packSize], "room, coverage and pack size must be positive");
  if (bad) return bad;
  var sticks = Math.ceil(roomM2 / m2PerStick);
  var sessions = Math.floor(packSize / sticks);
  return { sticks: sticks, sessions: sessions };
}
function yearPlan(sessionsWeek, sticksEach, packPrice, packSize){
  var bad = pos([sessionsWeek, sticksEach, packPrice, packSize], "pace, sticks, price and pack size must be positive");
  if (bad) return bad;
  var sticksYear = sessionsWeek * sticksEach * 52;
  var packsYear = sticksYear / packSize;
  return { sticksYear: r0(sticksYear), packsYear: r2(packsYear), costYear: r2(packsYear * packPrice) };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderBurn(r, lengthCm, minPerCm, packCount){
  return "A " + lengthCm + " cm stick burns about " + plural(r.minutes, "minute") + " at a labeled " + minPerCm + " minutes per centimeter - a pack of " + packCount + " is about " + plural(r.hours, "hour") + ".";
}
function renderRoom(r, roomM2, m2PerStick, packSize){
  var base = "Scenting a " + roomM2 + " m² room takes " + plural(r.sticks, "stick") + " at a labeled " + m2PerStick + " m² each";
  if (r.sessions === 0) return base + " - a " + packSize + "-stick pack covers no full sessions.";
  return base + " - a " + packSize + "-stick pack covers " + plural(r.sessions, "session") + ".";
}
function renderYear(r, sessionsWeek, sticksEach){
  return plural(sessionsWeek, "session") + " a week of " + plural(sticksEach, "stick") + " is " + plural(r.sticksYear, "stick") + " a year - about " + plural(r.packsYear, "pack") + ", " + r.costYear + " at your price.";
}
var api = { burnPlan: burnPlan, roomPlan: roomPlan, yearPlan: yearPlan,
  renderBurn: renderBurn, renderRoom: renderRoom, renderYear: renderYear };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.IncenseMath = api;
})(typeof window !== "undefined" ? window : globalThis);

#!/usr/bin/env python3
"""PokéRadar: authorized JSON feed -> profitability filter -> Telegram notifications.
No Vinted scraping. Credentials are read only from environment variables.
"""
import json, os, urllib.request, urllib.parse, datetime, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
STATE = ROOT / "alerted.json"
def request(url, data=None, token=None):
    headers={"User-Agent":"PokeRadar/1.3 (+authorized feed)","Accept":"application/json"}
    if token: headers["Authorization"]="Bearer "+token
    if data is not None: headers["Content-Type"]="application/x-www-form-urlencoded"
    req=urllib.request.Request(url,data=data,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as r:
        return r.read(3_000_000)

def validate(x):
    if not isinstance(x,dict): return False
    try:
        u=urllib.parse.urlsplit(x["url"])
        host=u.hostname or ""
        if u.scheme!="https" or not (host=="vinted.fr" or host.endswith(".vinted.fr") or host.startswith("vinted.") or ".vinted." in host): return False
        if not u.path.startswith("/items/"): return False
        if not isinstance(x["title"],str) or not x["title"].strip():return False
        keys=["ask_price","purchase_fees","shipping","market_value","selling_fee_rate","resale_shipping","other_costs"]
        return all(isinstance(x.get(k),(int,float)) and not isinstance(x.get(k),bool) and 0<=x[k]<1e8 for k in keys) and x["selling_fee_rate"]<=1
    except (KeyError,ValueError,TypeError):return False

def metrics(x):
    cost=x["ask_price"]+x["purchase_fees"]+x["shipping"]
    profit=x["market_value"]*(1-x["selling_fee_rate"])-x["resale_shipping"]-x["other_costs"]-cost
    return profit,profit/cost*100 if cost else 0

def main():
    feed=os.getenv("AUTHORIZED_FEED_URL","").strip()
    if not feed:
        print("No AUTHORIZED_FEED_URL configured; no monitoring possible.")
        return
    if not feed.startswith("https://"):raise ValueError("Feed URL must use HTTPS")
    content=request(feed,token=os.getenv("AUTHORIZED_FEED_TOKEN") or None)
    obj=json.loads(content)
    if not isinstance(obj,dict) or not isinstance(obj.get("items"),list):raise ValueError("Invalid feed schema")
    items=[x for x in obj["items"] if validate(x)][:2000]
    out={"updated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_status":"connected","items":items}
    (ROOT/"feed.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Received",len(items),"valid items")
    token=os.getenv("TELEGRAM_BOT_TOKEN","")
    chat=os.getenv("TELEGRAM_CHAT_ID","")
    if not token or not chat:
        print("Telegram not configured; feed updated without notifications.")
        return
    try: seen=json.loads(STATE.read_text(encoding="utf-8"))
    except (FileNotFoundError,ValueError):seen=[]
    if not isinstance(seen,list):seen=[]
    seen=set(str(x) for x in seen)
    threshold=float(os.getenv("MIN_PROFIT_EUR","20"))
    roi_min=float(os.getenv("MIN_ROI_PERCENT","25"))
    eligible=sorted((x for x in items if metrics(x)[0]>=threshold and metrics(x)[1]>=roi_min),key=lambda x:metrics(x)[0],reverse=True)
    fresh=[x for x in eligible if x["url"] not in seen]
    for x in fresh[:15]:
        profit,roi=metrics(x)
        msg=f"📡 PokéRadar : opportunité à vérifier\n{x['title'][:120]}\nPrix : {x['ask_price']:.2f} €\nMarge indicative : {profit:.2f} € · ROI {roi:.0f}%\n⚠️ Authenticité et cote non certifiées\n{x['url']}"
        request("https://api.telegram.org/bot"+token+"/sendMessage",data=urllib.parse.urlencode({"chat_id":chat,"text":msg,"disable_web_page_preview":"true"}).encode())
        seen.add(x["url"])
    STATE.write_text(json.dumps(sorted(seen)[-5000:],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Sent",min(len(fresh),15),"Telegram notifications")
if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("Radar error:",type(exc).__name__,str(exc)[:200],file=sys.stderr)
        sys.exit(1)

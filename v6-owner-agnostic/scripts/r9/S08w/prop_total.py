import collections
exec(open("val62p2_b_prop3.py").read().split("province_power_sum")[0])
total_qual = 0
miss2 = 0
eng_ches = None
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]: continue
        pred=sum(info.get(m2,{}).get(c,{}).get("province_power",0.0)/DIV
                 for m2 in OUT.get(n,[]) if info.get(m2,{}).get(c,{}).get("province_power",0.0)>=RAWTHR)
        got=d.get("max_pow",0.0)
        if pred>0:
            total_qual+=1
            if got==0.0:
                miss2+=1
                if n=="chesapeake_bay" and c=="ENG":
                    eng_ches=(pred,got)
print("total qualifying pairs:", total_qual)
print("missing:", miss2)
print("eng chesapeake_bay pred/got:", eng_ches)
# check england's power in english_channel
print("ENG in english_channel:", info.get("english_channel",{}).get("ENG"))

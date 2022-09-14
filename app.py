import sys
import csv

known = {
  "Gehalt": ["DYNATRACE AUSTRIA GMBH", "NUKI", "Dynatrace Austria GmbH"],
  "Miete": ["Lydia und Gerhard Burgstaller"],
  "Lebensmittel": ["SPAR DANKT", "BILLA DANKT", "LIDL DANKT", "ADEG", "AGM", "PENNY", "BASIC AUSTRIA"],
  "Drogerie": ["DM-FIL", "BIPA", "MUELLER"],
  "Technik": ["MEDIA MARKT"],
  "Kleidung und Sport": ["KIK", "INTERSPORT", "H&M", "RABATTZ", "DEICHMANN"],
  "Einrichtung": ["XXXLUTZ", "IKEA", "JYSK", "THALIA.AT"],
  "Tanken": ["TANKSTELLE", "ENI", "OMV", "TURMOEL", "SHELL", "PP ROSENTRALER"],
  "Hygiene": ["KLIPP"],
  "Essen Firma": ["HOTSPOT"], 
  "Trafik": ["TRAFIK"],
  "Versicherung": ["Wiener Staedtische Versicherung AG", "Allianz Elementar", "UNIQA", "Zürich/Unfall", "MAND-ID 00260000000000000000000000000415708"],
  "Internet und Mobil": ["Oja.at", "HOT TELEKOM"],
  "Paypal": ["PAYPAL"],
  "Bar": ["FOYER-BEHEB", "BANKOMAT", "AUTOMAT"],
  "Kredit": ["KREDITRATE"],
  "Amazon": ["AMAZON.DE", "AMZN MKTP"],
  "Fastfood": ["MCDONALDS", "SUBWAY", "DUNKIN DONUTS"],
  "Apotheke": ["APOTHEKE"],
  "Parken": ["PARKEN", "PARKHAUS", "WIPARK", "PARKGARAGE"],
  "Optiker": ["Wutscher Optik KG", "SEHEN WUTSCHER"],
  "Freizeit": ["HAUS DES MEE", "PARKBAD DOBRIACH"],
  "Strafe": ["BH Hermagor"],
  "Öffentl. Verkehr": ["WIENER LINIEN"],
  "Arzt": ["DR CHRISTIAN EBNER"],
  "Überweisung": ["UEBERWEISUNG"],
  "Konto": ["Kontoführung", "Sollzinssatz", "Wird der vereinbarte Rahmen überzogen"],
  "Energie Graz GmbH": ["Energie Graz GmbH"],
  "Kreditkarte": ["Ihre MasterCard Abrechnung"],
  "Autoversicherung": ["MAND-ID 0706MG78142"]
}


if len(sys.argv) <= 1:
  print("Please specify a file")
  exit()

cur_index = -1
per_month = {}

# print("File is: " + sys.argv[1])
with open(sys.argv[1], mode ='r') as file:
  csvFile = csv.reader(file, delimiter=';')
  for lines in csvFile:
    cur_index = cur_index + 1
    if cur_index == 0:
      continue
    months = lines[0].split(".")
    month = months[2] + "_" + months[1]
    value = float(lines[2].replace(",", "."))
    text = lines[10]
    found = False
    for key in known:
      for knowns in known[key]:
        if knowns in text:
          text = key
          found = True
          continue
      if found:
        continue    
    
    if not month in per_month:
      per_month[month] = {}
    if not text in per_month[month]:
      per_month[month][text]  = 0
      
    per_month[month][text] = per_month[month][text] + value

    
for m in per_month:
  print("---------------------- " + m + " ----------------------")
  saldo = 0
  for kn in known:
    if kn in per_month[m]:
      v = round(per_month[m][kn], 2)
      saldo = saldo + v
    else:
      v = 0.0
    print(f"{kn}: {v}")
  unk_v = 0
  for unk in per_month[m]:
    if not unk in known:
      print(f"{unk}: {per_month[m][unk]}")
      unk_v = unk_v + per_month[m][unk]
    
  vx = round(unk_v, 2)
  saldo = saldo + vx
  print(f"Unknown: {vx}")
  saldo = round(saldo, 2)
  print(f"SALDO: {saldo}")
  print("\n\n")
   

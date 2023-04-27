import sys
import csv

def format_number(number, precision=2):
    # build format string
    number = round(number, 2)
    format_str = '{{:,.{}f}}'.format(precision)
    # make number string
    number_str = format_str.format(number)
    # replace chars
    return number_str.replace(',', 'X').replace('.', ',').replace('X', '.')

known = {
  "Gehalt": ["DYNATRACE AUSTRIA GMBH", "NUKI", "Dynatrace Austria GmbH", ", GEHALT", "Gehalt", "WOCHENGELD", "Familienbeihilfe", "Kinderbetreuungsgeld"],
  "Miete": ["Lydia und Gerhard Burgstaller"],
  "Lebensmittel": ["TOOGOODTOG", "SPAR DANKT", "Spar dankt", "BILLA DANKT", "LIDL DANKT", "ADEG", "AGM", "PENNY", "BASIC AUSTRIA", "FRESSNAPF", "BAECKEREI", "BACKEREI", "HOFER DANKT"],
  "Drogerie": ["DM-FIL", "BIPA", "MUELLER", "Wild Cosmetics", "DRLUFT.DE"],
  "Technik": ["MEDIA MARKT", "MEDIAMARKT"],
  "Kleidung und Sport": ["KIK", "INTERSPORT", "H&M", "RABATTZ", "DEICHMANN", "WERKSKAUFHAUS", "HM AT0154", "ASOS", "C&A", "Walz", "BLUETOMATO", "Calzedonia"],
  "Einrichtung": ["DEHNER", "HORNBACH", "XXXLUTZ", "IKEA", "JYSK", "THALIA.AT", "DEPOT HANDELSGESELL", "LAGERHAUS", "S' KAEFERLE", "OBI", "WILLHABEN", "TJX OESTERREICH PARN", "K.Smyths Toys"],
  "Wilhaben": ["willhaben"],
  "Tanken": ["TANKSTELLE", "ENI", "OMV", "TURMOEL", "SHELL", "PP ROSENTRALER"],
  "Hygiene": ["KLIPP"],
  "Essen Firma": ["HOTSPOT"], 
  "Trafik": ["TRAFIK"],
  "Versicherung": ["Wiener Staedtische Versicherung AG", "Allianz Elementar", "UNIQA", "Zürich/Unfall", "MAND-ID 00260000000000000000000000000415708"],
  "Internet und Mobil": ["Oja.at", "HOT TELEKOM"],
  "Bar": ["FOYER-BEHEB", "BANKOMAT", "AUTOMAT", "SB-Ausz."],
  "Kredit": ["KREDITRATE"],
  "Amazon": ["AMAZON.DE", "AMZN MKTP", "AMZ*", "Amazon.de", "AMZN Mktp DE", "AMZ BestChoice"],
  "Fastfood": ["MCDONALDS", "SUBWAY", "DUNKIN DONUTS", "PIZZERIA LA STRADA", "HOTEL ZUR POST", "DUNKINDONUTS", "FRANZ - STREETFOOD"],
  "Apotheke": ["APOTHEKE"],
  "Parken und Maut": ["PARKEN", "PARKHAUS", "WIPARK", "PARKGARAGE", "MAUTSTELLE", "PARKPLATZ"],
  "Optiker": ["Wutscher Optik KG", "SEHEN WUTSCHER", "IWEAR DIRECT LTD"],
  "Freizeit": ["HAUS DES MEE", "PARKBAD DOBRIACH", "METZGERWIRT", "BADEHAUS", "AUSTRIAN TICKETS"],
  "Strafe": ["BH Hermagor"],
  "Öffentl. Verkehr": ["WIENER LINIEN", "STRASSENBAHN GRAZ"],
  "Arzt": ["DR CHRISTIAN EBNER"],
  "Überweisung": ["UEBERWEISUNG"],
  "Konto": ["Kontoführung", "Sollzinssatz", "Wird der vereinbarte Rahmen überzogen", "Entgeltanpassung"],
  "Energie Graz GmbH": ["Energie Graz GmbH"],
  "Kreditkarte": ["Ihre MasterCard Abrechnung"],
  "Autoversicherung": ["MAND-ID 0706MG78142"],
  "Spotify/Netflix/Prime/Nintendo": ["PAYPAL *SPOTIFY", "SPOTIFY", "NETFLIX", "AMZNPRIME", "AMAZON PRIME", "NINTENDO", "DISNEY PLUS"],
  "Paypal": ["PAYPAL"],
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
  unkown_list = {}
  for kn in known:
    if kn in per_month[m]:
      v = round(per_month[m][kn], 2)
      saldo = saldo + v
    else:
      v = 0.0
    print(f"{kn}\t{format_number(v)}")
  unk_v = 0
  for unk in per_month[m]:
    if not unk in known:
      # print(f"{unk}: {per_month[m][unk]}")
      unkown_list[unk] = per_month[m][unk]
      unk_v = unk_v + per_month[m][unk]
    
  vx = round(unk_v, 2)
  saldo = saldo + vx
  print(f"Unknown\t{format_number(vx)}")
  saldo = round(saldo, 2)
  print(f"SALDO:\t{format_number(saldo)}")
  print("\n")
  for s in unkown_list:
    print(f"{s}\t{unkown_list[s]}")
  print("\n\n\n")

rows = [""] 
for kn in known:
  rows.append(kn)
rows.append("Unbekannt")
rows.append("SALDO")

index_unknown = len(known) + 1
 
for m in per_month:
  rows[0] = rows[0] + "\t" + m
  unk_v = 0.0
  saldo = 0.0
  for a in per_month[m]:
    saldo = saldo + per_month[m][a]
    if not a in known:
      unk_v = unk_v + per_month[m][a]
  rows[index_unknown] = rows[index_unknown] + "\t" + format_number(unk_v)
  rows[index_unknown + 1] = rows[index_unknown + 1] + "\t" + format_number(saldo)
  
ri = 1
for kn in known:
  for m in per_month:
    v = 0.0
    if kn in per_month[m]:
      v = per_month[m][kn]
    rows[ri] = rows[ri] + "\t" + format_number(v) 
  ri = ri + 1  


for r in rows:
  print(r)  

   

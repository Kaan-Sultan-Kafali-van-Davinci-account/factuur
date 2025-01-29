import json, os
from reportlab.pdfgen import canvas

dir = os.listdir("JSON_ORDER/test_set_PC/")

orders = []

for file in dir:
    with open("JSON_ORDER/test_set_PC/" + file) as f:
        data = json.load(f)
        orders.append((file, data))

for order in orders:

    producten = ""
    prijs = 0
    prijs_met_btw = 0
    aantal = 0
    productomschrijvingen = []
    for index, product in enumerate(order[1]["factuur"]["producten"]):
        producten += product["productnaam"]
        if index != len(order[1]["factuur"]["producten"]) - 1: producten += ", "
        prijs += product["aantal"] * product["prijs_per_stuk_excl_btw"]
        prijs_met_btw += product["aantal"] * product["prijs_per_stuk_excl_btw"] * (1 + product["btw_per_stuk"] / 100)
        aantal += product["aantal"]
        productomschrijvingen.append(product["productnaam"] + "     PRIJS: " + str(product["aantal"]) + "x " + str(round(product["prijs_per_stuk_excl_btw"], 2)) + "     BTW: " + str(product["btw_per_stuk"]) + "%     TOTAAL: " + str(round(product["aantal"] * product["prijs_per_stuk_excl_btw"], 2)) )
    
    factuurdatum = order[1]["factuur"]["factuurdatum"]
    betaaltermijn = int(order[1]["factuur"]["betaaltermijn"][:-6])

    dag, maand, jaar = map(int, factuurdatum.split('-'))

    for _ in range(betaaltermijn):
        dag += 1
        if dag > [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][maand - 1]:
            dag = 1
            maand += 1
            if maand > 12:
                maand = 1
                jaar += 1

    text = ["Tunari",
    "Romboutslaan 34",
    "3312 KP, Dordrecht","",
    "Kvk: " + order[1]["factuur"]["klant"]["KVK-nummer"],
    "Btw: NL123456789B01", "",
    "Aan:",
    order[1]["factuur"]["klant"]["naam"],
    order[1]["factuur"]["klant"]["adres"],
    order[1]["factuur"]["klant"]["postcode"] + " " + order[1]["factuur"]["klant"]["stad"], "",
    order[0][:-9],
    "Factuurnummer: " + order[1]["factuur"]["factuurnummer"],
    "Factuurdatum: " + order[1]["factuur"]["factuurdatum"],
    "Einddatum betaling:", f"{dag:02d}-{maand:02d}-{jaar}", "",
    "Omschrijving Aantal Bedrag BTW Totaal",
    "Producten: ", "  " + producten, ""
    ]

    for productomschrijving in productomschrijvingen:
        text.append(productomschrijving)
    
    text += ["",
    "TOTAAL EXCL. BTW",
    "€" + str(round(prijs, 2)), "",
    "Btw: 21% Bedrag: " + str(round(prijs, 2)), "",
    "Totaal Btw: " + str(round(prijs_met_btw - prijs, 2)), "",
    "Te betalen:",
    "€" + str(round(prijs_met_btw, 2))]

    c = canvas.Canvas("JSON_PROCESSED/" + order[0][:-5] + ".pdf")
    c.setFont("Helvetica", 9)
    for index, line in enumerate(text):
        c.drawString(20, 750 - (index * 13), line)
    #c.drawImage("logo.png", 2, 790, 150, 50, mask=[0, 0, 0])
    c.save()
import json, os
from reportlab.pdfgen import canvas

dir = os.listdir("json/")

orders = []

for file in dir:
    with open("json/" + file) as f:
        data = json.load(f)
        orders.append((file, data))

most_products = (0, "")

for order in orders:

    producten = ""
    prijs = 0
    prijs_met_btw = 0
    aantal = 0
    productomschrijvingen = []
    for index, product in enumerate(order[1]["order"]["producten"]):
        producten += product["productnaam"]
        if index != len(order[1]["order"]["producten"]) - 1: producten += ", "
        prijs += product["aantal"] * product["prijs_per_stuk_excl_btw"]# * (1 + product["btw_percentage"] / 100)
        prijs_met_btw += product["aantal"] * product["prijs_per_stuk_excl_btw"] * (1 + product["btw_percentage"] / 100)
        aantal += product["aantal"]
        productomschrijvingen.append(product["productnaam"] + "     PRIJS: " + str(product["aantal"]) + "x " + str(round(product["prijs_per_stuk_excl_btw"], 2)) + "     BTW: " + str(product["btw_percentage"]) + "%     TOTAAL: " + str(round(product["aantal"] * product["prijs_per_stuk_excl_btw"], 2)) )

    if most_products[0] < len(producten):
        most_products = (len(producten), order[0])
    
    text = ["Tunari",
    "Romboutslaan 34",
    "3312 KP, Dordrecht","",
    "Kvk: " + order[1]["order"]["klant"]["KVK-nummer"],
    "Btw: NL123456789B01", "",
    "Aan:",
    order[1]["order"]["klant"]["naam"],
    order[1]["order"]["klant"]["adres"],
    order[1]["order"]["klant"]["postcode"] + " " + order[1]["order"]["klant"]["stad"], "",
    order[0][:-9],
    "Factuurnummer: " + order[1]["order"]["ordernummer"],
    "Factuurdatum: " + order[1]["order"]["orderdatum"],
    "Betaaltermijn: " + order[1]["order"]["betaaltermijn"], "",
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

    c = canvas.Canvas("json_to_pdf/" + order[0][:-5] + ".pdf")
    c.setFont("Helvetica", 9)
    for index, line in enumerate(text):
        c.drawString(20, 750 - (index * 13), line)
    #c.drawImage("logo.png", 2, 790, 150, 50, mask=[0, 0, 0])
    c.save()
import json, os
from reportlab.pdfgen import canvas

dir = os.listdir("order/")

orders = []

for file in dir:
    with open("order/" + file) as f:
        data = json.load(f)
        orders.append((file, data))

most_products = (0, "")

for file_index, order in enumerate(orders):
    begin_text = ["Tunari",
        "Romboutslaan 34",
        "3312 KP, Dordrecht","",
        "Kvk: " + order[1]["order"]["klant"]["KVK-nummer"],
        "Btw: NL123456789B01"]
    aantal_text = ["AANTAL", ""]
    btw_text = ["BTW", ""]
    excl_btw_text = ["EXCL. BTW", ""]

    try:
        producten = []
        prijs = 0
        prijs_met_btw = 0
        aantal = 0
        productomschrijvingen = []
        try:
            for index, product in enumerate(order[1]["order"]["producten"]):
                producten.append(product["productnaam"])
                prijs += product["aantal"] * product["prijs_per_stuk_excl_btw"]# * (1 + product["btw_percentage"] / 100)
                prijs_met_btw += product["aantal"] * product["prijs_per_stuk_excl_btw"] * (1 + product["btw_per_stuk"] / 100)
                aantal += product["aantal"]
                productomschrijvingen.append(product["productnaam"] + "     PRIJS: " + str(product["aantal"]) + "x " + str(round(product["prijs_per_stuk_excl_btw"], 2)) + "     BTW: " + str(product["btw_per_stuk"]) + "%     TOTAAL: " + str(round(product["aantal"] * product["prijs_per_stuk_excl_btw"], 2)) )
                aantal_text.append(str(product["aantal"]))
                btw_text.append(str(product["btw_per_stuk"]) + "%")
                excl_btw_text.append("€" + str(round(product["prijs_per_stuk_excl_btw"], 2)))
        except:
            for index, product in enumerate(order[1]["order"]["producten"]):
                producten.append(product["productnaam"])
                prijs += product["aantal"] * product["prijs_per_stuk_excl_btw"]# * (1 + product["btw_percentage"] / 100)
                prijs_met_btw += product["aantal"] * product["prijs_per_stuk_excl_btw"] * (1 + product["btw_percentage"] / 100)
                aantal += product["aantal"]
                productomschrijvingen.append(product["productnaam"] + "     PRIJS: " + str(product["aantal"]) + "x " + str(round(product["prijs_per_stuk_excl_btw"], 2)) + "     BTW: " + str(product["btw_percentage"]) + "%     TOTAAL: " + str(round(product["aantal"] * product["prijs_per_stuk_excl_btw"], 2)) )
                aantal_text.append(str(product["aantal"]))
                btw_text.append(str(product["btw_percentage"]) + "%")
                excl_btw_text.append("€" + str(round(product["prijs_per_stuk_excl_btw"], 2)))

        if most_products[0] < len(producten):
            most_products = (len(producten), order[0])

        try:
            factuurdatum = order[1]["factuur"]["factuurdatum"]
            betaaltermijn = int(order[1]["factuur"]["betaaltermijn"][:-6])
        except:
            factuurdatum = order[1]["order"]["orderdatum"]
            betaaltermijn = int(order[1]["order"]["betaaltermijn"][:-6])

        dag, maand, jaar = map(int, factuurdatum.split('-'))

        for _ in range(betaaltermijn):
            dag += 1
            if dag > [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][maand - 1]:
                dag = 1
                maand += 1
                if maand > 12:
                    maand = 1
                    jaar += 1
        
        text = ["Aan:",
        order[1]["order"]["klant"]["naam"],
        order[1]["order"]["klant"]["adres"],
        order[1]["order"]["klant"]["postcode"] + " " + order[1]["order"]["klant"]["stad"], "",
        order[0][:-9],
        "Factuurnummer: " + order[1]["order"]["ordernummer"],
        "Factuurdatum: " + order[1]["order"]["orderdatum"],
        "Einddatum betaling: " + f"{dag:02d}-{maand:02d}-{jaar}", "", "",
        "Producten: ",
        "-------------------------------------------------------------------------------------------------------------------------------"
        ]

        for product in producten:
            text.append(product)
        
        text += ["",
        "TOTAAL EXCL. BTW",
        "€" + str(round(prijs, 2)), "",
        "Bedrag: " + str(round(prijs, 2)), "",
        "Totaal Btw: " + str(round(prijs_met_btw - prijs, 2)), "",
        "Te betalen:",
        "€" + str(round(prijs_met_btw, 2))]

        c = canvas.Canvas("JSON_INVOICE/" + order[0][:-5] + ".pdf")
        c.setFont("Helvetica", 9)
        for index, line in enumerate(text):
            c.drawString(20, 750 - (index * 13), line)
        for index, line in enumerate(begin_text):
            c.drawString(400, 800 - (index * 13), line)
        for index, line in enumerate(aantal_text):
            c.drawString(180, 607 - (index * 13), line)
        for index, line in enumerate(btw_text):
            c.drawString(250, 607 - (index * 13), line)
        for index, line in enumerate(excl_btw_text):
            c.drawString(300, 607 - (index * 13), line)
        c.drawImage("logo.png", 2, 790, 150, 50, mask=[0, 0, 0])
        c.save()

    except Exception as e:
        c = canvas.Canvas("JSON_ORDER_ERROR/" + order[0][:-5] + ".pdf")
        c.setFont("Helvetica", 9)
        c.drawString(20, 750, "Error in order: " + order[0] + ", " + str(e))
        c.save()

    print("Order " + order[0] + " is verwerkt.", str(file_index))

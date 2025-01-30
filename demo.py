import json, os
from reportlab.pdfgen import canvas

dir = os.listdir("demo_json/")

fruiten = []

for file in dir:
    if file.endswith(".json"):
        with open("demo_json/" + file) as f:
            data = json.load(f)
            fruiten.append((file, data))

for file_index, fruit in enumerate(fruiten):
    text = ["Fruit: " + fruit[1]["fruit"], "Kleur: " + fruit[1]["kleur"], "Soort: " + fruit[1]["soort"]]

    c = canvas.Canvas("demo_pdf/" + fruit[0][:-5] + ".pdf")
    c.setFont("Helvetica", 15)
    for index, line in enumerate(text):
        c.drawString(20, 750 - (index * 40), line)

    c.drawImage("demo_json/" + fruit[0][:-5] + ".png", 250, 700, 100, 100, mask=[0, 0, 0])
    
    c.save()

    print("Fruit " + fruit[0] + " is verwerkt.", str(file_index))
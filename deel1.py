from reportlab.pdfgen import canvas

text = input("Enter text: ")

c = canvas.Canvas("PDF_INVOICE/factuur.pdf")
c.setFont("Helvetica", 12)
c.drawString(20, 750, text)
#c.drawImage("logo.png", 2, 790, 150, 50, mask=[0, 0, 0])
#c.circle(100, 100, 50, stroke=1, fill=1)
c.save()


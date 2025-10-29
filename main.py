import PySimpleGUI as sg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import qrcode
import os

# Cria pasta output se não existir
if not os.path.exists("output"):
    os.makedirs("output")

# Layout GUI
layout = [
    [sg.Text("Nome do Pagador"), sg.Input(key="nome")],
    [sg.Text("CPF/CNPJ"), sg.Input(key="cpf")],
    [sg.Text("Valor (R$)"), sg.Input(key="valor")],
    [sg.Text("Vencimento (dd/mm/yyyy)"), sg.Input(key="vencimento")],
    [sg.Text("Favorecido"), sg.Input(key="favorecido")],
    [sg.Button("Gerar Boleto"), sg.Button("Sair")]
]

window = sg.Window("Gerador de Boletos - Profissional", layout, size=(400,250))

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Sair"):
        break
    elif event == "Gerar Boleto":
        nome = values["nome"]
        cpf = values["cpf"]
        valor = values["valor"]
        vencimento = values["vencimento"]
        favorecido = values["favorecido"]

        # QR Code
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(f"PIX: {favorecido} | Valor: {valor}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"output/qrcode_{nome}.png"
        img.save(qr_path)

        # PDF profissional
        pdf_path = f"output/boleto_{nome}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # Fundo
        c.setFillColor(colors.whitesmoke)
        c.rect(20, 20, width-40, height-40, fill=1, stroke=0)

        # Cabeçalho
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(colors.darkblue)
        c.drawString(50, height-50, f"Boleto - {favorecido}")

        # Dados do pagador
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawString(50, height-80, f"Nome: {nome}")
        c.drawString(50, height-100, f"CPF/CNPJ: {cpf}")
        c.drawString(50, height-120, f"Valor: R$ {valor}")
        c.drawString(50, height-140, f"Vencimento: {vencimento}")

        # QR Code
        c.drawImage(qr_path, width-150, height-200, width=120, height=120)

        # Rodapé
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors.grey)
        c.drawString(50, 30, "Boleto gerado com Python | Projeto de portfólio")

        c.save()
        sg.popup(f"Boleto gerado com sucesso!\nPDF: {pdf_path}")

window.close()

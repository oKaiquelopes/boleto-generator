import PySimpleGUI as sg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
import qrcode
from PIL import Image
import os

# Cria pasta output se não existir
if not os.path.exists("output"):
    os.makedirs("output")

# Layout da GUI
layout = [
    [sg.Text("Nome do Pagador"), sg.Input(key="nome")],
    [sg.Text("CPF/CNPJ"), sg.Input(key="cpf")],
    [sg.Text("Valor (R$)"), sg.Input(key="valor")],
    [sg.Text("Vencimento (dd/mm/yyyy)"), sg.Input(key="vencimento")],
    [sg.Text("Favorecido"), sg.Input(key="favorecido")],
    [sg.Button("Gerar Boleto"), sg.Button("Sair")]
]

window = sg.Window("Gerador de Boletos PDF - Profissional", layout, size=(400,250))

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

        # Gera QR Code estilizado
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(f"PIX: {favorecido} | Valor: {valor}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"output/qrcode_{nome}.png"
        img.save(qr_path)

        # Cria PDF com layout mais profissional
        pdf_path = f"output/boleto_{nome}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # Fundo opcional
        c.setFillColor(colors.lightgrey)
        c.rect(20*mm, 20*mm, width-40*mm, height-40*mm, fill=1, stroke=0)

        # Cabeçalho
        c.setFillColor(colors.darkblue)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(25*mm, height-30*mm, f"Boleto - {favorecido}")

        # Dados do pagador
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawString(25*mm, height-50*mm, f"Nome: {nome}")
        c.drawString(25*mm, height-65*mm, f"CPF/CNPJ: {cpf}")
        c.drawString(25*mm, height-80*mm, f"Valor: R$ {valor}")
        c.drawString(25*mm, height-95*mm, f"Vencimento: {vencimento}")

        # QR Code
        c.drawImage(qr_path, width-70*mm, height-100*mm, width=50*mm, height=50*mm)

        # Rodapé
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(25*mm, 30*mm, "Boleto gerado com Python | Projeto de portfólio")

        c.save()

        sg.popup(f"Boleto gerado com sucesso!\n\nPDF: {pdf_path}\nQR Code: {qr_path}")

window.close()

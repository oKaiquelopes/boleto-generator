import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import qrcode
import os

# Pasta output
if not os.path.exists("output"):
    os.makedirs("output")

st.title("Gerador de Boletos - Web App Profissional")

# Inputs
nome = st.text_input("Nome do Pagador")
cpf = st.text_input("CPF/CNPJ")
valor = st.text_input("Valor (R$)")
vencimento = st.text_input("Vencimento (dd/mm/yyyy)")
favorecido = st.text_input("Favorecido")

if st.button("Gerar Boleto"):
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

    st.success("Boleto gerado com sucesso!")
    st.download_button("Download PDF", data=open(pdf_path, "rb").read(), file_name=f"boleto_{nome}.pdf")

import json
import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from fpdf import FPDF

# ЗАМЕНИТЕ НА ВАШ ТОКЕН
TOKEN = "7870765503:AAETy6lau_YlGF-UpRjpw1z5GRGehEiMFzI"
bot = Bot(token=TOKEN)
dp = Dispatcher()

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Положите файл DejaVuSans.ttf в папку с ботом
        font_path = "DejaVuSans.ttf"
        if os.path.exists(font_path):
            self.add_font('DejaVu', '', font_path, uni=True)
            self.font_name = 'DejaVu'
        else:
            self.font_name = 'Arial'

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font(pdf.font_name, size=14)
    
    def fmt(n): return f"{int(n):,}".replace(",", " ") + " UZS"

    pdf.cell(200, 10, txt=f"Ҳисобот санаси: {data['date']}", ln=True, align='C')
    pdf.ln(10)

    # Порядок строк строго по вашему запросу
    lines = [
        f"Нахт: {fmt(data['naxit'])}",
        f"Клик: {fmt(data['click'])}",
        f"Касса ойлик: {fmt(data['kassa_oylik'])}",
        "",
        f"Зарплата: {fmt(data['salary'])}",
        f"Йўлкира: {fmt(data['yulkira'])}",
        "",
        f"Ойлидан ташқари Расход: {fmt(data['extra'])}",
        "--------------------------------------------------",
        f"Общий касса: {fmt(data['grand_total'])}",
        f"Нахт қолди: {fmt(data['naxit_qoldi'])}"
    ]

    for line in lines:
        if line == "":
            pdf.ln(5)
        else:
            pdf.cell(0, 10, txt=line, ln=True)
    
    return pdf.output(dest='S')

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        pdf_content = create_pdf(data)
        
        report = types.BufferedInputFile(pdf_content, filename=f"Report_{data['date']}.pdf")
        await message.answer_document(report, caption="✅ Ҳисобот тайёр!")
    except Exception as e:
        await message.answer(f"Хатолик: {e}")

async def main():
    print("Бот ишга тушди...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
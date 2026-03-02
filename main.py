import requests
import json
from telegram import Update, constants
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# --- ضع معلوماتك هنا ---
TELEGRAM_TOKEN = "8272974282:AAHE6CuJbMUWKg2FJdlF7mQiPXAbOATkFXY"
GROQ_API_KEY = "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"
BOT_NAME = "الغزالي"

def ask_ai(question):
    """دالة التواصل مع ذكاء Groq الاصطناعي"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile", # موديل قوي جداً وسريع
        "messages": [
            {
                "role": "system", 
                "content": f"أنت مساعد تعليمي ذكي واسمك {BOT_NAME}. أجب باللغة العربية بأسلوب تعليمي مبسط."
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=25)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"⚠️ خطأ من الخادم (كود {response.status_code}). تأكد من صحة مفتاح API."
    except Exception as e:
        return f"❌ فشل الاتصال: تأكد من تشغيل الإنترنت في هاتفك."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التأكد من وجود نص في الرسالة
    if not update.message or not update.message.text:
        return

    text = update.message.text

    # التحقق إذا كانت الرسالة تحتوي على اسم البوت
    if BOT_NAME in text:
        # استخلاص السؤال وحذف اسم البوت من النص
        question = text.replace(BOT_NAME, "").strip()
        
        if not question:
            await update.message.reply_text(f"نعم، أنا {BOT_NAME}.. كيف يمكنني مساعدتك؟")
            return

        # إظهار حالة "جاري الكتابة" في التلغرام
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        
        # جلب الجواب
        answer = ask_ai(question)
        
        # إرسال الجواب (مع تقسيم الرسائل الطويلة)
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await update.message.reply_text(answer[i:i+4000])
        else:
            await update.message.reply_text(answer)

def main():
    print(f"✅ تم تشغيل بوت {BOT_NAME} بنجاح عبر Groq!")
    print("انتظر رسائل الطلاب في التلجرام...")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()


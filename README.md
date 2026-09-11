# الخطيب المترجم — Al-Khateeb Translator

موقع Django لترجمة الخطبة نصيًا إلى لغات متعددة، بدون إخراج صوتي.

## التشغيل المحلي
Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:OPENAI_API_KEY="ضع_مفتاحك_هنا"
python manage.py migrate
python manage.py runserver
```
ثم افتح http://127.0.0.1:8000

## النشر على Render المجاني
1. ارفع المشروع إلى GitHub.
2. في Render: New → Blueprint.
3. اختر مستودع GitHub.
4. Render يقرأ render.yaml.
5. عند طلب `OPENAI_API_KEY` ضع مفتاح OpenAI في Environment Variables. لا تضع المفتاح داخل GitHub.
6. بعد نجاح البناء افتح رابط `onrender.com`.

## ملاحظات مهمة
- الموقع يستخدم SpeechRecognition في Chrome/Edge للترجمة الحية النصية من كلام الخطيب؛ مصدر الكلام عربي.
- بعد ظهور كل مقطع عربي، يرسله الموقع إلى Django لترجمته إلى اللغة المختارة.
- العربية تعرض النص العربي مباشرة، وهي مناسبة للصم وضعاف السمع.
- لا يوجد Text-to-Speech ولا صوت صادر من الموقع.
- إذا لم يدعم المتصفح SpeechRecognition، يظهر للمستخدم خيار استخدام تسجيل الصوت للـ backend في التطوير، ويمكن لاحقًا تحويله إلى WebSocket/Realtime للترجمة الفورية.
- Render Free مناسب للتجربة وليس للاستخدام الإنتاجي؛ الخدمة قد تتوقف بعد 15 دقيقة من عدم النشاط.

الحقوق: جميع الحقوق محفوظة لأسرة الصناديد® 2026

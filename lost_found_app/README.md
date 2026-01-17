# Lost & Found API Prototype

هذا مجرّد نموذج أولي بسيط يوفّر واجهة برمجية (API) يمكن استخدامها لاحقًا من تطبيق أندرويد.

## تشغيل محلي (عند توفر المتطلبات)
```bash
pip install fastapi uvicorn
uvicorn lost_found_app.main:app --reload
```

## ملاحظات
- التخزين هنا في الذاكرة فقط (In-Memory) لأغراض البداية.
- يمكن لاحقًا استبدال التخزين بـ Firebase أو قاعدة بيانات حقيقية.

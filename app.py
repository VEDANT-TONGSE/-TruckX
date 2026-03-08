"""
TruckX Logistics Platform v4.0 — Multilingual Real-Time Edition
Run: pip install streamlit pandas plotly && streamlit run app.py
"""

import streamlit as st
import sqlite3, pandas as pd, random, math, hashlib, time, json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="TruckX – Logistics",
    page_icon="🚛", layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
#  TRANSLATIONS  (10 languages)
# ═══════════════════════════════════════════════════════════
LANGUAGES = {
    "English":    "en",
    "हिंदी":      "hi",
    "मराठी":      "mr",
    "தமிழ்":      "ta",
    "తెలుగు":     "te",
    "ਪੰਜਾਬੀ":     "pa",
    "বাংলা":      "bn",
    "ગુજરાતી":    "gu",
    "Español":    "es",
    "العربية":    "ar",
}

LANG_FLAGS = {
    "en":"🇬🇧","hi":"🇮🇳","mr":"🇮🇳","ta":"🇮🇳","te":"🇮🇳",
    "pa":"🇮🇳","bn":"🇮🇳","gu":"🇮🇳","es":"🇪🇸","ar":"🇸🇦",
}

T = {
    # ── General ──────────────────────────────────────────────────────────
    "app_name":       {"en":"TruckX","hi":"ट्रकX","mr":"ट्रकX","ta":"டிரக்X","te":"ట్రక్X","pa":"ਟਰੱਕX","bn":"ট্রাকX","gu":"ટ્રકX","es":"TruckX","ar":"TruckX"},
    "tagline":        {"en":"India's Smartest Logistics Platform","hi":"भारत का सबसे स्मार्ट लॉजिस्टिक्स प्लेटफॉर्म","mr":"भारताचे सर्वात स्मार्ट लॉजिस्टिक्स प्लॅटफॉर्म","ta":"இந்தியாவின் மிகவும் புத்திசாலி லாஜிஸ்டிக்ஸ் தளம்","te":"భారతదేశపు అత్యంత తెలివైన లాజిస్టిక్స్ ప్లాట్‌ఫారమ్","pa":"ਭਾਰਤ ਦਾ ਸਭ ਤੋਂ ਸਮਾਰਟ ਲੌਜਿਸਟਿਕਸ ਪਲੇਟਫਾਰਮ","bn":"ভারতের স্মার্টেস্ট লজিস্টিক্স প্ল্যাটফর্ম","gu":"ભારતનું સૌથી સ્માર્ટ લોજિસ્ટિક્સ પ્લેટફોર્મ","es":"La plataforma logística más inteligente de India","ar":"أذكى منصة لوجستية في الهند"},
    "live":           {"en":"LIVE","hi":"लाइव","mr":"लाइव","ta":"நேரடி","te":"లైవ్","pa":"ਲਾਈਵ","bn":"লাইভ","gu":"લાઈવ","es":"EN VIVO","ar":"مباشر"},
    "login":          {"en":"Login","hi":"लॉगिन","mr":"लॉगिन","ta":"உள்நுழைவு","te":"లాగిన్","pa":"ਲੌਗਿਨ","bn":"লগইন","gu":"લૉગઇન","es":"Iniciar sesión","ar":"تسجيل الدخول"},
    "register":       {"en":"Register","hi":"रजिस्टर","mr":"नोंदणी","ta":"பதிவு","te":"నమోదు","pa":"ਰਜਿਸਟਰ","bn":"নিবন্ধন","gu":"નોંધણી","es":"Registrarse","ar":"تسجيل"},
    "logout":         {"en":"Logout","hi":"लॉगआउट","mr":"लॉगआउट","ta":"வெளியேறு","te":"లాగ్‌అవుట్","pa":"ਲੌਗਆਊਟ","bn":"লগআউট","gu":"લૉગઆઉટ","es":"Cerrar sesión","ar":"تسجيل الخروج"},
    "phone":          {"en":"Phone Number","hi":"फ़ोन नंबर","mr":"फोन नंबर","ta":"தொலைபேசி எண்","te":"ఫోన్ నంబర్","pa":"ਫ਼ੋਨ ਨੰਬਰ","bn":"ফোন নম্বর","gu":"ફોન નંબર","es":"Número de teléfono","ar":"رقم الهاتف"},
    "password":       {"en":"Password","hi":"पासवर्ड","mr":"पासवर्ड","ta":"கடவுச்சொல்","te":"పాస్‌వర్డ్","pa":"ਪਾਸਵਰਡ","bn":"পাসওয়ার্ড","gu":"પાસવર્ડ","es":"Contraseña","ar":"كلمة المرور"},
    "name":           {"en":"Full Name","hi":"पूरा नाम","mr":"पूर्ण नाव","ta":"முழு பெயர்","te":"పూర్తి పేరు","pa":"ਪੂਰਾ ਨਾਮ","bn":"পুরো নাম","gu":"પૂર્ણ નામ","es":"Nombre completo","ar":"الاسم الكامل"},
    "email":          {"en":"Email","hi":"ईमेल","mr":"ईमेल","ta":"மின்னஞ்சல்","te":"ఇమెయిల్","pa":"ਈਮੇਲ","bn":"ইমেইল","gu":"ઈમેઈલ","es":"Correo electrónico","ar":"البريد الإلكتروني"},
    "submit":         {"en":"Submit","hi":"जमा करें","mr":"सबमिट करा","ta":"சமர்ப்பி","te":"సమర్పించు","pa":"ਜਮ੍ਹਾਂ ਕਰੋ","bn":"জমা দিন","gu":"સબમિટ કરો","es":"Enviar","ar":"إرسال"},
    "cancel":         {"en":"Cancel","hi":"रद्द करें","mr":"रद्द करा","ta":"ரத்துசெய்","te":"రద్దు చేయి","pa":"ਰੱਦ ਕਰੋ","bn":"বাতিল করুন","gu":"રદ કરો","es":"Cancelar","ar":"إلغاء"},
    "save":           {"en":"Save","hi":"सहेजें","mr":"जतन करा","ta":"சேமி","te":"సేవ్ చేయి","pa":"ਸੁਰੱਖਿਅਤ ਕਰੋ","bn":"সংরক্ষণ করুন","gu":"સાચવો","es":"Guardar","ar":"حفظ"},
    "language":       {"en":"Language","hi":"भाषा","mr":"भाषा","ta":"மொழி","te":"భాష","pa":"ਭਾਸ਼ਾ","bn":"ভাষা","gu":"ભાષા","es":"Idioma","ar":"اللغة"},
    "select_language":{"en":"Choose your language","hi":"अपनी भाषा चुनें","mr":"तुमची भाषा निवडा","ta":"உங்கள் மொழியை தேர்ந்தெடுங்கள்","te":"మీ భాష ఎంచుకోండి","pa":"ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ","bn":"আপনার ভাষা বেছে নিন","gu":"તમારી ભાષા પસંદ કરો","es":"Elige tu idioma","ar":"اختر لغتك"},
    "welcome":        {"en":"Welcome to TruckX!","hi":"TruckX में आपका स्वागत है!","mr":"TruckX मध्ये आपले स्वागत आहे!","ta":"TruckX-க்கு வரவேற்கிறோம்!","te":"TruckX కి స్వాగతం!","pa":"TruckX ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!","bn":"TruckX-এ স্বাগতম!","gu":"TruckX માં આપનું સ્વાગત છે!","es":"¡Bienvenido a TruckX!","ar":"مرحباً بك في TruckX!"},
    "demo_creds":     {"en":"Demo credentials","hi":"डेमो क्रेडेंशियल","mr":"डेमो क्रेडेन्शियल","ta":"டெமோ நற்சான்றிதழ்கள்","te":"డెమో క్రెడెన్షియల్స్","pa":"ਡੈਮੋ ਕ੍ਰੇਡੈਂਸ਼ੀਅਲ","bn":"ডেমো ক্রেডেনশিয়াল","gu":"ડેમો ક્રેડેન્શિયલ","es":"Credenciales de demo","ar":"بيانات الاعتماد التجريبية"},

    # ── Navigation ──
    "nav_home":       {"en":"Home","hi":"होम","mr":"मुख्यपृष्ठ","ta":"முகப்பு","te":"హోమ్","pa":"ਹੋਮ","bn":"হোম","gu":"હોમ","es":"Inicio","ar":"الرئيسية"},
    "nav_driver":     {"en":"Driver Portal","hi":"ड्राइवर पोर्टल","mr":"ड्राइव्हर पोर्टल","ta":"டிரைவர் போர்டல்","te":"డ్రైవర్ పోర్టల్","pa":"ਡਰਾਈਵਰ ਪੋਰਟਲ","bn":"ড্রাইভার পোর্টাল","gu":"ડ્રાઈવર પોર્ટલ","es":"Portal del conductor","ar":"بوابة السائق"},
    "nav_customer":   {"en":"Customer Portal","hi":"ग्राहक पोर्टल","mr":"ग्राहक पोर्टल","ta":"வாடிக்கையாளர் போர்டல்","te":"కస్టమర్ పోర్టల్","pa":"ਗਾਹਕ ਪੋਰਟਲ","bn":"কাস্টমার পোর্টাল","gu":"ગ્રાહક પોર્ટલ","es":"Portal del cliente","ar":"بوابة العميل"},
    "nav_admin":      {"en":"Admin","hi":"एडमिन","mr":"प्रशासक","ta":"நிர்வாகி","te":"అడ్మిన్","pa":"ਐਡਮਿਨ","bn":"অ্যাডমিন","gu":"એડમિન","es":"Admin","ar":"المشرف"},

    # ── KPI / Stats ──
    "online_drivers": {"en":"Online Drivers","hi":"ऑनलाइन ड्राइवर","mr":"ऑनलाइन ड्राइव्हर","ta":"ஆன்லைன் டிரைவர்கள்","te":"ఆన్‌లైన్ డ్రైవర్లు","pa":"ਔਨਲਾਈਨ ਡਰਾਈਵਰ","bn":"অনলাইন ড্রাইভার","gu":"ઓનલાઈન ડ્રાઈવર","es":"Conductores en línea","ar":"السائقون المتصلون"},
    "avail_trucks":   {"en":"Available Trucks","hi":"उपलब्ध ट्रक","mr":"उपलब्ध ट्रक","ta":"கிடைக்கும் ட்ரக்குகள்","te":"అందుబాటులో ఉన్న ట్రక్కులు","pa":"ਉਪਲਬਧ ਟਰੱਕ","bn":"উপলব্ধ ট্রাক","gu":"ઉપલબ્ધ ટ્રક","es":"Camiones disponibles","ar":"الشاحنات المتاحة"},
    "active_trips":   {"en":"Active Trips","hi":"सक्रिय यात्राएं","mr":"सक्रिय ट्रिप्स","ta":"செயல்பாட்டு பயணங்கள்","te":"యాక్టివ్ ట్రిప్స్","pa":"ਕਿਰਿਆਸ਼ੀਲ ਯਾਤਰਾਵਾਂ","bn":"সক্রিয় ট্রিপ","gu":"સક્રિય ટ્રિપ","es":"Viajes activos","ar":"الرحلات النشطة"},
    "total_revenue":  {"en":"Total Revenue","hi":"कुल राजस्व","mr":"एकूण महसूल","ta":"மொத்த வருவாய்","te":"మొత్తం ఆదాయం","pa":"ਕੁੱਲ ਮਾਲੀਆ","bn":"মোট রাজস্ব","gu":"કુલ આવક","es":"Ingresos totales","ar":"إجمالي الإيرادات"},
    "pending_orders": {"en":"Pending Orders","hi":"लंबित ऑर्डर","mr":"प्रलंबित ऑर्डर","ta":"நிலுவையிலுள்ள ஆர்டர்கள்","te":"పెండింగ్ ఆర్డర్లు","pa":"ਲੰਬਿਤ ਆਰਡਰ","bn":"পেন্ডিং অর্ডার","gu":"પ્રતીક્ષિત ઓર્ડર","es":"Pedidos pendientes","ar":"الطلبات المعلقة"},

    # ── Booking ──
    "book_truck":     {"en":"Book a Truck","hi":"ट्रक बुक करें","mr":"ट्रक बुक करा","ta":"ட்ரக்கை முன்பதிவு செய்யுங்கள்","te":"ట్రక్ బుక్ చేయండి","pa":"ਟਰੱਕ ਬੁੱਕ ਕਰੋ","bn":"ট্রাক বুক করুন","gu":"ટ્રક બુક કરો","es":"Reservar un camión","ar":"احجز شاحنة"},
    "pickup_city":    {"en":"Pickup City","hi":"पिकअप शहर","mr":"पिकअप शहर","ta":"பிக்அப் நகரம்","te":"పికప్ సిటీ","pa":"ਪਿਕਅੱਪ ਸ਼ਹਿਰ","bn":"পিকআপ শহর","gu":"પિકઅપ શહેર","es":"Ciudad de recogida","ar":"مدينة الاستلام"},
    "drop_city":      {"en":"Drop City","hi":"डेस्टिनेशन शहर","mr":"ड्रॉप शहर","ta":"இறக்கும் நகரம்","te":"డ్రాప్ సిటీ","pa":"ਡਰਾਪ ਸ਼ਹਿਰ","bn":"ড্রপ শহর","gu":"ડ્રોપ શહેર","es":"Ciudad de destino","ar":"مدينة التسليم"},
    "goods_type":     {"en":"Goods Type","hi":"माल का प्रकार","mr":"मालाचा प्रकार","ta":"பொருட்களின் வகை","te":"వస్తువుల రకం","pa":"ਮਾਲ ਦੀ ਕਿਸਮ","bn":"পণ্যের ধরন","gu":"માલ પ્રકાર","es":"Tipo de mercancía","ar":"نوع البضائع"},
    "truck_type":     {"en":"Truck Type","hi":"ट्रक प्रकार","mr":"ट्रकचा प्रकार","ta":"ட்ரக் வகை","te":"ట్రక్ రకం","pa":"ਟਰੱਕ ਦੀ ਕਿਸਮ","bn":"ট্রাকের ধরন","gu":"ટ્રક પ્રકાર","es":"Tipo de camión","ar":"نوع الشاحنة"},
    "weight":         {"en":"Weight (tons)","hi":"वजन (टन)","mr":"वजन (टन)","ta":"எடை (டன்)","te":"బరువు (టన్నులు)","pa":"ਵਜ਼ਨ (ਟਨ)","bn":"ওজন (টন)","gu":"વજન (ટન)","es":"Peso (toneladas)","ar":"الوزن (طن)"},
    "priority":       {"en":"Priority","hi":"प्राथमिकता","mr":"प्राधान्य","ta":"முன்னுரிமை","te":"ప్రాధాన్యత","pa":"ਤਰਜੀਹ","bn":"অগ্রাধিকার","gu":"અগ્રતા","es":"Prioridad","ar":"الأولوية"},
    "search_trucks":  {"en":"Search Available Trucks","hi":"उपलब्ध ट्रक खोजें","mr":"उपलब्ध ट्रक शोधा","ta":"கிடைக்கும் ட்ரக்குகளை தேடுங்கள்","te":"అందుబాటులో ఉన్న ట్రక్కులు శోధించండి","pa":"ਉਪਲਬਧ ਟਰੱਕ ਖੋਜੋ","bn":"উপলব্ধ ট্রাক খুঁজুন","gu":"ઉપલબ્ધ ટ્રક શોધો","es":"Buscar camiones disponibles","ar":"البحث عن شاحنات متاحة"},
    "book_now":       {"en":"Book Now","hi":"अभी बुक करें","mr":"आत्ता बुक करा","ta":"இப்போது முன்பதிவு செய்யுங்கள்","te":"ఇప్పుడే బుక్ చేయండి","pa":"ਹੁਣੇ ਬੁੱਕ ਕਰੋ","bn":"এখনই বুক করুন","gu":"હમણાં બુક કરો","es":"Reservar ahora","ar":"احجز الآن"},
    "est_fare":       {"en":"Estimated Fare","hi":"अनुमानित किराया","mr":"अंदाजे भाडे","ta":"மதிப்பிடப்பட்ட கட்டணம்","te":"అంచనా ఛార్జ్","pa":"ਅਨੁਮਾਨਿਤ ਕਿਰਾਇਆ","bn":"আনুমানিক ভাড়া","gu":"અંદાજિત ભાડું","es":"Tarifa estimada","ar":"الأجرة التقديرية"},
    "distance":       {"en":"Distance","hi":"दूरी","mr":"अंतर","ta":"தூரம்","te":"దూరం","pa":"ਦੂਰੀ","bn":"দূরত্ব","gu":"અંતર","es":"Distancia","ar":"المسافة"},
    "eta":            {"en":"ETA","hi":"अनुमानित समय","mr":"अंदाजे वेळ","ta":"வருகை நேரம்","te":"ETA","pa":"ਆਉਣ ਦਾ ਸਮਾਂ","bn":"আসার সময়","gu":"ETA","es":"Hora estimada","ar":"الوقت المقدر"},
    "notes":          {"en":"Special Instructions","hi":"विशेष निर्देश","mr":"विशेष सूचना","ta":"சிறப்பு வழிமுறைகள்","te":"ప్రత్యేక సూచనలు","pa":"ਵਿਸ਼ੇਸ਼ ਨਿਰਦੇਸ਼","bn":"বিশেষ নির্দেশনা","gu":"ખાસ સૂચनाઓ","es":"Instrucciones especiales","ar":"تعليمات خاصة"},

    # ── Trip actions ──
    "accept":         {"en":"Accept Trip","hi":"ट्रिप स्वीकार करें","mr":"ट्रिप स्वीकारा","ta":"பயணத்தை ஏற்கவும்","te":"ట్రిప్ అంగీకరించండి","pa":"ਯਾਤਰਾ ਸਵੀਕਾਰ ਕਰੋ","bn":"ট্রিপ গ্রহণ করুন","gu":"ટ્રિપ સ્વીકારો","es":"Aceptar viaje","ar":"قبول الرحلة"},
    "reject":         {"en":"Reject","hi":"अस्वीकार करें","mr":"नकार द्या","ta":"நிராகரி","te":"తిరస్కరించు","pa":"ਰੱਦ ਕਰੋ","bn":"প্রত্যাখ্যান করুন","gu":"અસ્વીકાર કરો","es":"Rechazar","ar":"رفض"},
    "start_loading":  {"en":"Start Loading","hi":"लोडिंग शुरू करें","mr":"लोडिंग सुरू करा","ta":"ஏற்றலைத் தொடங்குங்கள்","te":"లోడింగ్ ప్రారంభించు","pa":"ਲੋਡਿੰਗ ਸ਼ੁਰੂ ਕਰੋ","bn":"লোডিং শুরু করুন","gu":"લોડિંગ શરૂ કરો","es":"Comenzar carga","ar":"بدء التحميل"},
    "dispatch":       {"en":"Dispatch Truck","hi":"ट्रक भेजें","mr":"ट्रक पाठवा","ta":"ட்ரக்கை அனுப்புங்கள்","te":"ట్రక్ పంపండి","pa":"ਟਰੱਕ ਭੇਜੋ","bn":"ট্রাক পাঠান","gu":"ટ્રક મોકલો","es":"Despachar camión","ar":"إرسال الشاحنة"},
    "complete":       {"en":"Complete Trip","hi":"ट्रिप पूरी करें","mr":"ट्रिप पूर्ण करा","ta":"பயணத்தை முடிக்கவும்","te":"ట్రిప్ పూర్తి చేయండి","pa":"ਯਾਤਰਾ ਪੂਰੀ ਕਰੋ","bn":"ট্রিপ সম্পন্ন করুন","gu":"ટ્રિપ પૂર્ણ કરો","es":"Completar viaje","ar":"إتمام الرحلة"},
    "track_live":     {"en":"Track Live","hi":"लाइव ट्रैक करें","mr":"लाइव ट्रॅक करा","ta":"நேரடியாக கண்காணி","te":"లైవ్ ట్రాక్ చేయండి","pa":"ਲਾਈਵ ਟ੍ਰੈਕ ਕਰੋ","bn":"লাইভ ট্র্যাক করুন","gu":"લાઈવ ટ્ર track કરો","es":"Rastrear en vivo","ar":"تتبع مباشر"},
    "history":        {"en":"History","hi":"इतिहास","mr":"इतिहास","ta":"வரலாறு","te":"చరిత్ర","pa":"ਇਤਿਹਾਸ","bn":"ইতিহাস","gu":"ઇતિહાસ","es":"Historial","ar":"السجل"},

    # ── Driver ──
    "my_fleet":       {"en":"My Fleet","hi":"मेरा बेड़ा","mr":"माझा ताफा","ta":"என் வாகன பூல்","te":"నా ఫ్లీట్","pa":"ਮੇਰਾ ਫਲੀਟ","bn":"আমার বহর","gu":"મારો ફ્લીટ","es":"Mi flota","ar":"أسطولي"},
    "trip_requests":  {"en":"Trip Requests","hi":"ट्रिप अनुरोध","mr":"ट्रिप विनंत्या","ta":"பயண கோரிக்கைகள்","te":"ట్రిప్ అభ్యర్థనలు","pa":"ਯਾਤਰਾ ਬੇਨਤੀਆਂ","bn":"ট্রিপ রিকোয়েস্ট","gu":"ટ્રિપ વિનંતીઓ","es":"Solicitudes de viaje","ar":"طلبات الرحلة"},
    "earnings":       {"en":"Earnings","hi":"कमाई","mr":"कमाई","ta":"வருமானம்","te":"సంపాదన","pa":"ਕਮਾਈ","bn":"উপার্জন","gu":"કમાણી","es":"Ganancias","ar":"الأرباح"},
    "notifications":  {"en":"Notifications","hi":"सूचनाएं","mr":"सूचना","ta":"அறிவிப்புகள்","te":"నోటిఫికేషన్లు","pa":"ਸੂਚਨਾਵਾਂ","bn":"বিজ্ঞপ্তি","gu":"સૂચनाઓ","es":"Notificaciones","ar":"الإشعارات"},
    "total_trips":    {"en":"Total Trips","hi":"कुल यात्राएं","mr":"एकूण ट्रिप्स","ta":"மொத்த பயணங்கள்","te":"మొత్తం ట్రిప్స్","pa":"ਕੁੱਲ ਯਾਤਰਾਵਾਂ","bn":"মোট ট্রিপ","gu":"કુલ ટ્રિપ","es":"Viajes totales","ar":"إجمالي الرحلات"},
    "rating":         {"en":"Rating","hi":"रेटिंग","mr":"रेटिंग","ta":"மதிப்பீடு","te":"రేటింగ్","pa":"ਰੇਟਿੰਗ","bn":"রেটিং","gu":"રેટિંગ","es":"Calificación","ar":"التقييم"},
    "experience":     {"en":"Experience","hi":"अनुभव","mr":"अनुभव","ta":"அனுபவம்","te":"అనుభవం","pa":"ਤਜ਼ਰਬਾ","bn":"অভিজ্ঞতা","gu":"અનુભવ","es":"Experiencia","ar":"الخبرة"},
    "license":        {"en":"License No","hi":"लाइसेंस नं.","mr":"लायसन्स नं.","ta":"உரிம எண்","te":"లైసెన్స్ నం.","pa":"ਲਾਇਸੈਂਸ ਨੰ.","bn":"লাইসেন্স নং","gu":"લાઇસન્સ નં.","es":"Número de licencia","ar":"رقم الرخصة"},
    "reg_truck":      {"en":"Register Truck","hi":"ट्रक रजिस्टर करें","mr":"ट्रक नोंदणी करा","ta":"ட்ரக்கை பதிவு செய்யுங்கள்","te":"ట్రక్ నమోదు చేయండి","pa":"ਟਰੱਕ ਰਜਿਸਟਰ ਕਰੋ","bn":"ট্রাক নিবন্ধন করুন","gu":"ટ્રક નોંધો","es":"Registrar camión","ar":"تسجيل الشاحنة"},
    "vehicle_no":     {"en":"Vehicle Number","hi":"वाहन नंबर","mr":"वाहन क्रमांक","ta":"வாகன எண்","te":"వాహన నంబర్","pa":"ਵਾਹਨ ਨੰਬਰ","bn":"যানবাহন নম্বর","gu":"વાહન નંબર","es":"Número de vehículo","ar":"رقم المركبة"},
    "capacity":       {"en":"Capacity (tons)","hi":"क्षमता (टन)","mr":"क्षमता (टन)","ta":"திறன் (டன்)","te":"సామర్థ్యం (టన్నులు)","pa":"ਸਮਰੱਥਾ (ਟਨ)","bn":"ধারণক্ষমতা (টন)","gu":"ક્ષમતા (ટન)","es":"Capacidad (toneladas)","ar":"السعة (طن)"},
    "model":          {"en":"Model","hi":"मॉडल","mr":"मॉडेल","ta":"மாடல்","te":"మోడల్","pa":"ਮਾਡਲ","bn":"মডেল","gu":"મૉડલ","es":"Modelo","ar":"الموديل"},
    "year":           {"en":"Year","hi":"वर्ष","mr":"वर्ष","ta":"ஆண்டு","te":"సంవత్సరం","pa":"ਸਾਲ","bn":"বছর","gu":"વર્ষ","es":"Año","ar":"السنة"},
    "city":           {"en":"City","hi":"शहर","mr":"शहर","ta":"நகரம்","te":"నగరం","pa":"ਸ਼ਹਿਰ","bn":"শহর","gu":"શહેર","es":"Ciudad","ar":"المدينة"},
    "set_available":  {"en":"Set Available","hi":"उपलब्ध सेट करें","mr":"उपलब्ध करा","ta":"கிடைக்கும் என்று அமை","te":"అందుబాటులో సెట్ చేయండి","pa":"ਉਪਲਬਧ ਸੈੱਟ ਕਰੋ","bn":"উপলব্ধ সেট করুন","gu":"ઉપলબ્ધ સેટ કરો","es":"Marcar disponible","ar":"تعيين متاح"},
    "set_busy":       {"en":"Set Busy","hi":"व्यस्त सेट करें","mr":"व्यस्त करा","ta":"பிஸியாக அமை","te":"బిజీగా సెట్ చేయండి","pa":"ਵਿਅਸਤ ਸੈੱਟ ਕਰੋ","bn":"ব্যস্ত সেট করুন","gu":"વ્યસ્ત સેટ કરો","es":"Marcar ocupado","ar":"تعيين مشغول"},

    # ── Status labels ──
    "status_pending":   {"en":"Pending","hi":"प्रतीक्षारत","mr":"प्रलंबित","ta":"நிலுவையில்","te":"పెండింగ్","pa":"ਲੰਬਿਤ","bn":"অপেক্ষারত","gu":"પ્રતીક્ષિત","es":"Pendiente","ar":"قيد الانتظار"},
    "status_accepted":  {"en":"Accepted","hi":"स्वीकृत","mr":"स्वीकारले","ta":"ஏற்றுக்கொள்ளப்பட்டது","te":"అంగీకరించబడింది","pa":"ਸਵੀਕਾਰ ਕੀਤਾ","bn":"গৃহীত","gu":"સ્વીકૃત","es":"Aceptado","ar":"مقبول"},
    "status_loading":   {"en":"Loading","hi":"लोडिंग","mr":"लोडिंग","ta":"ஏற்றுதல்","te":"లోడింగ్","pa":"ਲੋਡਿੰਗ","bn":"লোডিং","gu":"લોડિંગ","es":"Cargando","ar":"جارٍ التحميل"},
    "status_transit":   {"en":"In Transit","hi":"परिवहन में","mr":"प्रवासात","ta":"போக்குவரத்தில்","te":"ట్రాన్సిట్‌లో","pa":"ਆਵਾਜਾਈ ਵਿੱਚ","bn":"পরিবহনে","gu":"ट्रांзिटमां","es":"En tránsito","ar":"في العبور"},
    "status_completed": {"en":"Completed","hi":"पूर्ण","mr":"पूर्ण झाले","ta":"முடிந்தது","te":"పూర్తయింది","pa":"ਪੂਰਾ ਹੋਇਆ","bn":"সম্পন্ন","gu":"પૂર્ણ","es":"Completado","ar":"مكتمل"},
    "status_cancelled": {"en":"Cancelled","hi":"रद्द","mr":"रद्द","ta":"ரத்து","te":"రద్దు","pa":"ਰੱਦ","bn":"বাতিল","gu":"રદ","es":"Cancelado","ar":"ملغى"},

    # ── Onboarding ──
    "onboard_title":  {"en":"Get Started in 3 Easy Steps","hi":"3 आसान चरणों में शुरू करें","mr":"3 सोप्या चरणांमध्ये सुरू करा","ta":"3 எளிய படிகளில் தொடங்குங்கள்","te":"3 సులభ దశలలో ప్రారంభించండి","pa":"3 ਆਸਾਨ ਕਦਮਾਂ ਵਿੱਚ ਸ਼ੁਰੂ ਕਰੋ","bn":"৩টি সহজ ধাপে শুরু করুন","gu":"3 સરળ પગલામાં શરૂ કરો","es":"Comienza en 3 pasos","ar":"ابدأ في 3 خطوات بسيطة"},
    "onboard_1":      {"en":"Choose your city & destination","hi":"अपना शहर और गंतव्य चुनें","mr":"तुमचे शहर आणि गंतव्य निवडा","ta":"உங்கள் நகரம் மற்றும் இலக்கை தேர்ந்தெடுங்கள்","te":"మీ నగరం మరియు గమ్యాన్ని ఎంచుకోండి","pa":"ਆਪਣਾ ਸ਼ਹਿਰ ਅਤੇ ਮੰਜ਼ਿਲ ਚੁਣੋ","bn":"আপনার শহর ও গন্তব্য বেছে নিন","gu":"તમારું શહેર અને ગંતવ્ય પસંદ કરો","es":"Elige tu ciudad y destino","ar":"اختر مدينتك ووجهتك"},
    "onboard_2":      {"en":"Pick a truck & confirm fare","hi":"ट्रक चुनें और किराया कन्फर्म करें","mr":"ट्रक निवडा आणि भाडे कन्फर्म करा","ta":"ட்ரக்கை தேர்ந்தெடுத்து கட்டணத்தை உறுதிப்படுத்துங்கள்","te":"ట్రక్ ఎంచుకుని ఛార్జ్ కన్ఫర్మ్ చేయండి","pa":"ਟਰੱਕ ਚੁਣੋ ਅਤੇ ਕਿਰਾਇਆ ਕਨਫਰਮ ਕਰੋ","bn":"ট্রাক বেছে ভাড়া নিশ্চিত করুন","gu":"ટ્રક પ✏️ and ભાડું &#x2714; કરો","es":"Elige camión y confirma tarifa","ar":"اختر الشاحنة وأكد الأجرة"},
    "onboard_3":      {"en":"Track your shipment live","hi":"अपने शिपमेंट को लाइव ट्रैक करें","mr":"तुमची शिपमेंट लाइव ट्रॅक करा","ta":"உங்கள் ஏற்றுமதியை நேரடியாக கண்காணிக்கவும்","te":"మీ షిప్‌మెంట్‌ను లైవ్‌లో ట్రాక్ చేయండి","pa":"ਆਪਣੀ ਸ਼ਿਪਮੈਂਟ ਨੂੰ ਲਾਈਵ ਟਰੈਕ ਕਰੋ","bn":"আপনার শিপমেন্ট লাইভ ট্র্যাক করুন","gu":"તમારી શિપ ment &#x1F4CD; ライブ ট্র্যাক કরো","es":"Rastrea tu envío en vivo","ar":"تتبع شحنتك مباشرة"},

    # ── Misc ──
    "fare":           {"en":"Fare","hi":"किराया","mr":"भाडे","ta":"கட்டணம்","te":"ఛార్జ్","pa":"ਕਿਰਾਇਆ","bn":"ভাড়া","gu":"ভাদu","es":"Tarifa","ar":"الأجرة"},
    "no_data":        {"en":"No data available","hi":"कोई डेटा उपलब्ध नहीं","mr":"कोणताही डेटा उपलब्ध नाही","ta":"தரவு எதுவும் இல்லை","te":"డేటా అందుబాటులో లేదు","pa":"ਕੋਈ ਡੇਟਾ ਉਪਲਬਧ ਨਹੀਂ","bn":"কোনো তথ্য নেই","gu":"કોઈ ડેટа ઉपलब्ध नथी","es":"Sin datos disponibles","ar":"لا توجد بيانات"},
    "login_driver":   {"en":"Login as Driver","hi":"ड्राइवर के रूप में लॉगिन करें","mr":"ड्राइव्हर म्हणून लॉगिन करा","ta":"டிரைவராக உள்நுழைவு","te":"డ్రైవర్‌గా లాగిన్ చేయండి","pa":"ਡਰਾਈਵਰ ਵਜੋਂ ਲੌਗਇਨ ਕਰੋ","bn":"ড্রাইভার হিসেবে লগইন করুন","gu":"ড্রাઇవর தரীகে লॉগ ইন করো","es":"Entrar como conductor","ar":"تسجيل الدخول كسائق"},
    "login_customer": {"en":"Login as Customer","hi":"ग्राहक के रूप में लॉगिन करें","mr":"ग्राहक म्हणून लॉगिन करा","ta":"வாடிக்கையாளராக உள்நுழைவு","te":"కస్టమర్‌గా లాగిన్ చేయండి","pa":"ਗਾਹਕ ਵਜੋਂ ਲੌਗਇਨ ਕਰੋ","bn":"কাস্টমার হিসেবে লগইন","gu":"ग्राহক தரीகে লॉগ ইন করো","es":"Entrar como cliente","ar":"تسجيل الدخول كعميل"},
    "i_am_driver":    {"en":"I am a Driver","hi":"मैं एक ड्राइवर हूं","mr":"मी ड्राइव्हर आहे","ta":"நான் ஒரு டிரைவர்","te":"నేను డ్రైవర్ని","pa":"ਮੈਂ ਡਰਾਈਵਰ ਹਾਂ","bn":"আমি একজন ড্রাইভার","gu":"हु ड्राइवर छु","es":"Soy conductor","ar":"أنا سائق"},
    "i_am_customer":  {"en":"I need to ship goods","hi":"मुझे माल भेजना है","mr":"मला माल पाठवायचा आहे","ta":"எனக்கு பொருட்களை அனுப்ப வேண்டும்","te":"నాకు వస్తువులు పంపాలి","pa":"ਮੈਨੂੰ ਮਾਲ ਭੇਜਣਾ ਹੈ","bn":"আমাকে পণ্য পাঠাতে হবে","gu":"मारे माल मোকলवानो छे","es":"Necesito enviar mercancía","ar":"أحتاج لشحن بضائع"},

    # ── Admin ──
    "admin_center":   {"en":"Admin Command Center","hi":"एडमिन कमांड सेंटर","mr":"प्रशासक कमांड सेंटर","ta":"நிர்வாக கட்டளை மையம்","te":"అడ్మిన్ కమాండ్ సెంటర్","pa":"ਐਡਮਿਨ ਕਮਾਂਡ ਸੈਂਟਰ","bn":"অ্যাডমিন কমান্ড সেন্টার","gu":"एड्मिन कमांड सेन्टर","es":"Centro de administración","ar":"مركز إدارة الأوامر"},
    "analytics":      {"en":"Analytics","hi":"विश्लेषण","mr":"विश्लेषण","ta":"பகுப்பாய்வு","te":"అనలిటిక్స్","pa":"ਵਿਸ਼ਲੇਸ਼ਣ","bn":"বিশ্লেষণ","gu":"Analytics","es":"Análisis","ar":"التحليلات"},
    "operations":     {"en":"Operations","hi":"संचालन","mr":"ऑपरेशन","ta":"செயல்பாடுகள்","te":"ఆపరేషన్స్","pa":"ਸੰਚਾਲਨ","bn":"অপারেশন","gu":"Operations","es":"Operaciones","ar":"العمليات"},
}

def t(key, lang=None):
    if lang is None:
        lang = st.session_state.get("lang","en")
    return T.get(key,{}).get(lang, T.get(key,{}).get("en", key))

# ═══════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #050911;
  --bg2:       #09101e;
  --bg3:       #0e1929;
  --card:      #0d1828;
  --card2:     #111f33;
  --card3:     #162438;
  --amber:     #f59e0b;
  --amber-dim: rgba(245,158,11,.12);
  --blue:      #3b82f6;
  --blue-dim:  rgba(59,130,246,.12);
  --green:     #10b981;
  --green-dim: rgba(16,185,129,.12);
  --red:       #ef4444;
  --red-dim:   rgba(239,68,68,.12);
  --purple:    #8b5cf6;
  --purple-dim:rgba(139,92,246,.12);
  --pink:      #ec4899;
  --text:      #f1f5f9;
  --muted:     #64748b;
  --soft:      #94a3b8;
  --border:    #1a2d44;
  --border2:   #243d58;
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

html,body,[data-testid="stAppViewContainer"]{
  background:var(--bg)!important;
  color:var(--text)!important;
  font-family:'DM Sans',sans-serif!important;
}

/* Grid background */
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;inset:0;
  background-image:radial-gradient(circle at 20% 20%,rgba(245,158,11,.04) 0%,transparent 50%),
    radial-gradient(circle at 80% 80%,rgba(59,130,246,.04) 0%,transparent 50%),
    linear-gradient(rgba(245,158,11,.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(245,158,11,.018) 1px,transparent 1px);
  background-size:100% 100%,100% 100%,64px 64px,64px 64px;
  pointer-events:none;z-index:0;
}

[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#030710 0%,#06101e 100%)!important;
  border-right:1px solid var(--border)!important;
}
[data-testid="stSidebar"] *{color:var(--text)!important;}

h1,h2,h3,h4{font-family:'Syne',sans-serif!important;letter-spacing:-.3px;}

/* ── HERO ── */
.hero-badge{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.25);
  border-radius:99px;padding:.22rem .9rem;
  font-size:.68rem;font-weight:700;color:#10b981;
  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.8rem;
}
.hero-title{
  font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
  background:linear-gradient(135deg,#f59e0b 0%,#fbbf24 35%,#60a5fa 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  line-height:1;margin-bottom:.4rem;
}
.hero-sub{font-size:1rem;color:var(--soft);line-height:1.5;}

/* ── KPI CARDS ── */
.kpi-card{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:1.3rem 1.4rem;position:relative;overflow:hidden;
  transition:transform .25s,box-shadow .25s,border-color .25s;cursor:default;
}
.kpi-card:hover{transform:translateY(-5px);border-color:var(--border2);box-shadow:0 16px 48px rgba(0,0,0,.5);}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.kpi-a::before{background:linear-gradient(90deg,#f59e0b,#fbbf24);}
.kpi-b::before{background:linear-gradient(90deg,#3b82f6,#60a5fa);}
.kpi-g::before{background:linear-gradient(90deg,#10b981,#34d399);}
.kpi-p::before{background:linear-gradient(90deg,#8b5cf6,#a78bfa);}
.kpi-r::before{background:linear-gradient(90deg,#ec4899,#f472b6);}
.kpi-card::after{content:'';position:absolute;bottom:-20px;right:-20px;width:80px;height:80px;border-radius:50%;opacity:.04;}
.kpi-a::after{background:#f59e0b;}.kpi-b::after{background:#3b82f6;}.kpi-g::after{background:#10b981;}
.kpi-icon{font-size:1.5rem;margin-bottom:.5rem;opacity:.85;}
.kpi-label{font-size:.68rem;text-transform:uppercase;letter-spacing:1.8px;color:var(--muted);margin-bottom:.3rem;font-weight:600;}
.kpi-val{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:700;line-height:1;}
.kpi-a .kpi-val{color:#f59e0b;}.kpi-b .kpi-val{color:#3b82f6;}.kpi-g .kpi-val{color:#10b981;}
.kpi-p .kpi-val{color:#8b5cf6;}.kpi-r .kpi-val{color:#ec4899;}
.kpi-delta{font-size:.72rem;color:var(--green);margin-top:.35rem;display:flex;align-items:center;gap:3px;}

/* ── SECTION CARD ── */
.scard{
  background:var(--card);border:1px solid var(--border);border-radius:18px;
  padding:1.6rem;margin-bottom:1.1rem;position:relative;overflow:hidden;
}
.scard::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--border2),transparent);}
.stitle{
  font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;
  color:var(--amber);margin-bottom:1.1rem;display:flex;align-items:center;gap:.5rem;
  padding-bottom:.7rem;border-bottom:1px solid var(--border);
}

/* ── TRIP CARD ── */
.tcard{
  background:var(--card2);border:1px solid var(--border);border-radius:14px;
  padding:1.1rem 1.3rem;margin-bottom:.7rem;transition:border-color .2s,box-shadow .2s;
}
.tcard:hover{border-color:var(--border2);box-shadow:0 4px 20px rgba(0,0,0,.3);}
.tcard.urgent{border-left:3px solid var(--red);}
.tcard.active{border-left:3px solid var(--green);}

/* ── BADGES ── */
.bd{display:inline-flex;align-items:center;gap:4px;padding:.2rem .72rem;
  border-radius:99px;font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.9px;}
.bd-ok{background:rgba(16,185,129,.12);color:#10b981;border:1px solid rgba(16,185,129,.22);}
.bd-go{background:rgba(139,92,246,.12);color:#8b5cf6;border:1px solid rgba(139,92,246,.22);}
.bd-wait{background:rgba(245,158,11,.12);color:#f59e0b;border:1px solid rgba(245,158,11,.22);}
.bd-done{background:rgba(59,130,246,.12);color:#3b82f6;border:1px solid rgba(59,130,246,.22);}
.bd-no{background:rgba(100,116,139,.12);color:#64748b;border:1px solid rgba(100,116,139,.22);}
.bd-red{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.22);}
.bd-exp{background:rgba(236,72,153,.12);color:#ec4899;border:1px solid rgba(236,72,153,.22);}

/* ── STEPPER ── */
.stepper{display:flex;align-items:flex-start;margin:1rem 0;position:relative;}
.stepper::before{content:'';position:absolute;top:14px;left:5%;right:5%;height:2px;background:var(--border);z-index:0;}
.step{flex:1;display:flex;flex-direction:column;align-items:center;position:relative;z-index:1;}
.sdot{width:28px;height:28px;border-radius:50%;background:var(--card2);border:2px solid var(--border);
  display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:700;margin-bottom:.3rem;transition:all .3s;}
.step.done .sdot{background:var(--green);border-color:var(--green);color:#fff;}
.step.active .sdot{background:var(--amber);border-color:var(--amber);color:#050911;box-shadow:0 0 14px rgba(245,158,11,.55);}
.slabel{font-size:.62rem;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);text-align:center;}
.step.done .slabel{color:var(--green);}.step.active .slabel{color:var(--amber);}

/* ── INPUTS ── */
.stTextInput>div>div>input,.stSelectbox>div>div,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{
  background:#080f1c!important;border:1px solid var(--border)!important;border-radius:12px!important;
  color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:.9rem!important;
  transition:border-color .2s,box-shadow .2s!important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
  border-color:var(--amber)!important;box-shadow:0 0 0 3px rgba(245,158,11,.1)!important;}
.stSelectbox label,.stTextInput label,.stNumberInput label,.stTextArea label{
  color:var(--soft)!important;font-size:.75rem!important;font-weight:600!important;
  text-transform:uppercase!important;letter-spacing:.9px!important;}

/* ── BUTTONS ── */
.stButton>button{
  background:linear-gradient(135deg,#f59e0b,#d97706)!important;
  color:#050911!important;font-family:'Syne',sans-serif!important;
  font-weight:700!important;font-size:.95rem!important;border:none!important;
  border-radius:12px!important;padding:.6rem 1.5rem!important;
  transition:all .2s!important;letter-spacing:.3px!important;
}
.stButton>button:hover{opacity:.9!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(245,158,11,.3)!important;}
.stButton>button:active{transform:translateY(0)!important;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{
  background:#07101e!important;border-radius:14px!important;padding:4px!important;
  border:1px solid var(--border)!important;gap:3px!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;color:var(--muted)!important;
  border-radius:10px!important;font-family:'DM Sans',sans-serif!important;
  font-weight:600!important;font-size:.85rem!important;border:none!important;
}
.stTabs [aria-selected="true"]{background:rgba(245,158,11,.13)!important;color:var(--amber)!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1.2rem!important;}

/* ── Dataframes ── */
.stDataFrame,[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:14px!important;}
div[data-testid="metric-container"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:1rem!important;}
.stAlert{border-radius:12px!important;}

/* ── Live dot ── */
.ldot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;margin-right:5px;animation:blink 1.5s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.3;transform:scale(.65);}}

/* ── Notification banner ── */
.notif{
  background:linear-gradient(135deg,rgba(245,158,11,.08),rgba(59,130,246,.05));
  border:1px solid rgba(245,158,11,.2);border-radius:12px;
  padding:.75rem 1.1rem;display:flex;align-items:center;gap:.7rem;
  margin-bottom:.8rem;font-size:.88rem;
}

/* ── Timeline ── */
.timeline{position:relative;padding-left:1.8rem;}
.timeline::before{content:'';position:absolute;left:.45rem;top:0;bottom:0;width:2px;background:var(--border);}
.tlitem{position:relative;margin-bottom:.9rem;padding:.7rem .9rem;background:var(--card2);border-radius:11px;border:1px solid var(--border);}
.tlitem::before{content:'';position:absolute;left:-1.5rem;top:50%;transform:translateY(-50%);width:10px;height:10px;border-radius:50%;background:var(--amber);border:2px solid var(--bg);box-shadow:0 0 8px rgba(245,158,11,.5);}
.tltime{font-size:.68rem;color:var(--muted);font-family:'JetBrains Mono',monospace;}
.tltext{font-size:.84rem;margin-top:.12rem;}

/* ── Fare box ── */
.farebox{background:linear-gradient(135deg,rgba(245,158,11,.07),rgba(59,130,246,.05));
  border:1px solid rgba(245,158,11,.18);border-radius:14px;padding:1rem 1.2rem;text-align:center;}
.fareamt{font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:700;color:var(--amber);line-height:1;}
.farelabel{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:.3rem;}

/* ── Progress bar ── */
.progwrap{background:var(--border);border-radius:99px;height:6px;overflow:hidden;margin:.4rem 0;}
.progfill{height:100%;border-radius:99px;background:linear-gradient(90deg,#f59e0b,#3b82f6);transition:width .5s ease;}

/* ── Onboarding steps ── */
.onboard-step{
  background:var(--card);border:1px solid var(--border);border-radius:18px;
  padding:1.4rem;text-align:center;position:relative;overflow:hidden;
  transition:transform .2s,border-color .2s;
}
.onboard-step:hover{transform:translateY(-4px);border-color:var(--border2);}
.onboard-num{
  font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;
  -webkit-text-fill-color:transparent;background:linear-gradient(135deg,#f59e0b,#3b82f6);
  -webkit-background-clip:text;line-height:1;margin-bottom:.5rem;
}
.onboard-icon{font-size:2rem;margin-bottom:.5rem;}
.onboard-title{font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;margin-bottom:.3rem;}
.onboard-desc{font-size:.8rem;color:var(--soft);line-height:1.4;}

/* ── ROLE SELECTOR ── */
.role-btn{
  background:var(--card);border:2px solid var(--border);border-radius:18px;
  padding:2rem 1.5rem;text-align:center;cursor:pointer;
  transition:all .25s;position:relative;overflow:hidden;
}
.role-btn:hover,.role-btn.selected{border-color:var(--amber);background:linear-gradient(135deg,var(--card2),rgba(245,158,11,.06));}
.role-btn::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--amber),transparent);opacity:0;transition:opacity .2s;}
.role-btn:hover::before,.role-btn.selected::before{opacity:1;}
.role-icon{font-size:3rem;margin-bottom:.8rem;}
.role-title{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:.4rem;}
.role-desc{font-size:.82rem;color:var(--soft);}

/* ── LANGUAGE GRID ── */
.lang-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.5rem;margin-bottom:1.2rem;}
.lang-btn{
  background:var(--card2);border:1px solid var(--border);border-radius:10px;
  padding:.55rem .4rem;text-align:center;cursor:pointer;font-size:.8rem;
  transition:all .2s;font-family:'DM Sans',sans-serif;
}
.lang-btn:hover,.lang-btn.sel{background:var(--amber-dim);border-color:var(--amber);color:var(--amber);}

/* ── Fuel bar ── */
.fuelbar{display:flex;align-items:center;gap:8px;font-size:.78rem;}
.fuelwrap{flex:1;background:var(--border);border-radius:99px;height:4px;overflow:hidden;}
.fuelfill{height:100%;border-radius:99px;transition:width .3s;}

/* ── SIDEBAR ── */
.sb-logo{text-align:center;padding:1.2rem 0 .9rem;border-bottom:1px solid var(--border);margin-bottom:.7rem;}
.sb-logo-text{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;
  background:linear-gradient(135deg,#f59e0b,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.sb-stat{display:flex;justify-content:space-between;align-items:center;padding:.32rem 0;font-size:.77rem;}
.sb-stat-label{color:var(--muted);}
.sb-stat-val{font-weight:700;}
.sb-section{font-size:.62rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.8px;padding:.4rem 0 .2rem;font-weight:600;}
.sb-user{background:var(--card);border:1px solid var(--border);border-radius:11px;padding:.7rem .8rem;margin:.3rem 0;}

/* ── Quick action buttons in customer ── */
.qa-card{
  background:var(--card2);border:1px solid var(--border);border-radius:14px;
  padding:1.2rem;text-align:center;cursor:pointer;transition:all .2s;
}
.qa-card:hover{border-color:var(--border2);transform:translateY(-3px);}
.qa-icon{font-size:2rem;margin-bottom:.5rem;}
.qa-title{font-size:.85rem;font-weight:600;}

/* hide branding */
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
.block-container{padding-top:1.5rem!important;}
</style>
"""

# ═══════════════════════════════════════════════════════════
#  GEO
# ═══════════════════════════════════════════════════════════
CITY_COORDS={
    "Pune":(18.5204,73.8567),"Mumbai":(19.0760,72.8777),"Delhi":(28.7041,77.1025),
    "Bangalore":(12.9716,77.5946),"Chennai":(13.0827,80.2707),"Hyderabad":(17.3850,78.4867),
    "Kolkata":(22.5726,88.3639),"Ahmedabad":(23.0225,72.5714),"Jaipur":(26.9124,75.7873),
    "Surat":(21.1702,72.8311),"Lucknow":(26.8467,80.9462),"Nagpur":(21.1458,79.0882),
    "Indore":(22.7196,75.8577),"Bhopal":(23.2599,77.4126),"Chandigarh":(30.7333,76.7794),
    "Kochi":(9.9312,76.2673),"Coimbatore":(11.0168,76.9558),"Visakhapatnam":(17.6868,83.2185),
}
def get_coords(city): return CITY_COORDS.get(city,(18.5204,73.8567))

def haversine(a,b,c,d):
    R=6371; p1,p2=math.radians(a),math.radians(c)
    dp=math.radians(c-a); dl=math.radians(d-b)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))

def calc_fare(dist,ttype,weight,priority="normal"):
    base={"Mini Truck":12,"Medium Truck":18,"Heavy Truck":28,"Flatbed":22,"Container":32}
    rate=base.get(ttype,20); wf=1+(weight/100)
    mult={"normal":1.0,"express":1.35,"urgent":1.65}.get(priority,1.0)
    return round(dist*rate*wf*mult+200,2)

def eta_str(dist):
    h=dist/65
    return f"{int(h*60)} min" if h<1 else f"{h:.1f} hrs"

# ═══════════════════════════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════════════════════════
DB="truckx_v4.db"
def get_conn():
    c=sqlite3.connect(DB,check_same_thread=False); c.row_factory=sqlite3.Row; return c
def _hash(p): return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    c=get_conn(); cur=c.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS drivers(id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,phone TEXT UNIQUE,email TEXT,password TEXT,license_no TEXT,
      experience_years INTEGER DEFAULT 0,rating REAL DEFAULT 4.5,
      total_trips INTEGER DEFAULT 0,total_earnings REAL DEFAULT 0,
      is_online INTEGER DEFAULT 0,created_at TEXT DEFAULT(datetime('now')));
    CREATE TABLE IF NOT EXISTS trucks(id INTEGER PRIMARY KEY AUTOINCREMENT,
      driver_id INTEGER,vehicle_no TEXT UNIQUE,truck_type TEXT,capacity_tons REAL,
      model TEXT,year INTEGER,is_available INTEGER DEFAULT 1,
      current_lat REAL DEFAULT 18.5204,current_lng REAL DEFAULT 73.8567,
      city TEXT DEFAULT 'Pune',fuel_level INTEGER DEFAULT 80,odometer_km INTEGER DEFAULT 0,
      created_at TEXT DEFAULT(datetime('now')));
    CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,phone TEXT UNIQUE,email TEXT,password TEXT,
      total_bookings INTEGER DEFAULT 0,created_at TEXT DEFAULT(datetime('now')));
    CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,
      customer_id INTEGER,truck_id INTEGER,driver_id INTEGER,
      pickup_location TEXT,drop_location TEXT,
      pickup_lat REAL,pickup_lng REAL,drop_lat REAL,drop_lng REAL,
      truck_type TEXT,goods_type TEXT,weight_tons REAL,
      distance_km REAL,fare REAL,status TEXT DEFAULT 'pending',
      driver_accepted INTEGER DEFAULT 0,priority TEXT DEFAULT 'normal',
      created_at TEXT DEFAULT(datetime('now')),
      accepted_at TEXT,started_at TEXT,completed_at TEXT,notes TEXT);
    CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_type TEXT,user_id INTEGER,message TEXT,type TEXT DEFAULT 'info',
      is_read INTEGER DEFAULT 0,created_at TEXT DEFAULT(datetime('now')));
    """)
    c.commit(); _seed(c); c.close()

def _seed(c):
    cur=c.cursor()
    cur.execute("SELECT COUNT(*) FROM drivers")
    if cur.fetchone()[0]>0: return
    drv=[("Rajesh Kumar","9876543210","rajesh@truckx.in","MH12AB1234",8,4.8,142,385000),
         ("Suresh Patel","9876543211","suresh@truckx.in","MH14CD5678",5,4.5,87,220000),
         ("Anil Singh","9876543212","anil@truckx.in","MH01EF9012",12,4.9,198,560000),
         ("Mohan Yadav","9876543213","mohan@truckx.in","GJ05GH3456",3,4.2,45,95000),
         ("Vijay Sharma","9876543214","vijay@truckx.in","RJ14IJ7890",7,4.7,115,310000),
         ("Deepak Tiwari","9876543215","deepak@truckx.in","UP32KL2345",9,4.6,160,420000),
         ("Sanjay Gupta","9876543216","sanjay@truckx.in","MP09MN6789",4,4.3,62,140000)]
    for d in drv:
        cur.execute("INSERT INTO drivers(name,phone,email,password,license_no,experience_years,rating,total_trips,total_earnings,is_online) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (d[0],d[1],d[2],_hash("pass123"),d[3],d[4],d[5],d[6],d[7],random.randint(0,1)))
    trk=[(1,"MH12TR001","Mini Truck",1.5,"Tata Ace",2021,1,18.5204,73.8567,"Pune",85,12500),
         (2,"MH14TR002","Medium Truck",5.0,"Ashok Leyland",2020,1,19.0760,72.8777,"Mumbai",60,34200),
         (3,"MH01TR003","Heavy Truck",15.0,"Tata Prima",2019,0,28.7041,77.1025,"Delhi",40,89000),
         (4,"GJ05TR004","Flatbed",10.0,"Mahindra Blazo",2022,1,23.0225,72.5714,"Ahmedabad",90,22100),
         (5,"RJ14TR005","Container",20.0,"BharatBenz",2021,1,26.9124,75.7873,"Jaipur",70,55600),
         (6,"UP32TR006","Mini Truck",2.0,"Maruti Super Carry",2023,1,26.8467,80.9462,"Lucknow",95,8900),
         (7,"MP09TR007","Medium Truck",7.0,"Eicher Pro",2022,1,22.7196,75.8577,"Indore",55,41300),
         (1,"MH12TR008","Heavy Truck",12.0,"Volvo FMX",2020,1,19.0760,72.8777,"Mumbai",45,67800)]
    for t in trk:
        cur.execute("INSERT INTO trucks(driver_id,vehicle_no,truck_type,capacity_tons,model,year,is_available,current_lat,current_lng,city,fuel_level,odometer_km) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",t)
    cust=[("Amit Desai","9111111111","amit@gmail.com"),("Priya Nair","9222222222","priya@gmail.com"),
          ("Rahul Mehta","9333333333","rahul@gmail.com"),("Sneha Joshi","9444444444","sneha@gmail.com"),
          ("Kiran Shah","9555555555","kiran@gmail.com")]
    for cu in cust:
        cur.execute("INSERT INTO customers(name,phone,email,password) VALUES(?,?,?,?)",(cu[0],cu[1],cu[2],_hash("pass123")))
    cities=list(CITY_COORDS.keys())
    sts=["completed","completed","completed","in_transit","pending","accepted","cancelled"]
    gds=["Electronics","FMCG","Chemicals","Machinery","Textiles","Furniture","Perishables","Pharmaceuticals"]
    prs=["normal","normal","normal","urgent","express"]
    for _ in range(35):
        cid=random.randint(1,5); tid=random.randint(1,8)
        dist=round(random.uniform(60,900),1); fare=round(dist*random.uniform(30,60),2)
        pu=random.choice(cities); dr=random.choice([x for x in cities if x!=pu])
        plat,plng=get_coords(pu); dlat,dlng=get_coords(dr)
        cur.execute("""INSERT INTO bookings(customer_id,truck_id,driver_id,pickup_location,drop_location,
            pickup_lat,pickup_lng,drop_lat,drop_lng,truck_type,goods_type,weight_tons,
            distance_km,fare,status,driver_accepted,priority,created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now',?))""",
            (cid,tid,tid,pu,dr,plat,plng,dlat,dlng,
             random.choice(["Mini Truck","Medium Truck","Heavy Truck","Flatbed","Container"]),
             random.choice(gds),round(random.uniform(0.5,18),1),dist,fare,
             random.choice(sts),1,random.choice(prs),f"-{random.randint(1,90)} days"))
    c.commit()

# ── DB helpers ──────────────────────────────────────────────────────────────
def driver_login(ph,pw):
    c=get_conn(); r=c.execute("SELECT * FROM drivers WHERE phone=? AND password=?",(ph,_hash(pw))).fetchone(); c.close(); return dict(r) if r else None
def customer_login(ph,pw):
    c=get_conn(); r=c.execute("SELECT * FROM customers WHERE phone=? AND password=?",(ph,_hash(pw))).fetchone(); c.close(); return dict(r) if r else None

def reg_driver(name,phone,email,pwd,lic,exp):
    c=get_conn()
    try:
        c.execute("INSERT INTO drivers(name,phone,email,password,license_no,experience_years) VALUES(?,?,?,?,?,?)",(name,phone,email,_hash(pwd),lic,exp))
        c.commit(); c.close(); return True,t("welcome")
    except: c.close(); return False,"Phone already registered."

def reg_customer(name,phone,email,pwd):
    c=get_conn()
    try:
        c.execute("INSERT INTO customers(name,phone,email,password) VALUES(?,?,?,?)",(name,phone,email,_hash(pwd)))
        c.commit(); c.close(); return True,t("welcome")
    except: c.close(); return False,"Phone already registered."

def reg_truck(did,vno,ttype,cap,model,year,city):
    c=get_conn()
    try:
        lat,lng=get_coords(city)
        c.execute("INSERT INTO trucks(driver_id,vehicle_no,truck_type,capacity_tons,model,year,current_lat,current_lng,city) VALUES(?,?,?,?,?,?,?,?,?)",(did,vno,ttype,cap,model,year,lat,lng,city))
        c.commit(); c.close(); return True,"Truck registered!"
    except: c.close(); return False,"Vehicle number exists."

def find_trucks(ttype,pickup,weight):
    c=get_conn()
    q="SELECT t.*,d.name as dname,d.rating,d.phone as dphone,d.total_trips FROM trucks t JOIN drivers d ON t.driver_id=d.id WHERE t.is_available=1"
    params=[]
    if ttype!="Any": q+=" AND t.truck_type=?"; params.append(ttype)
    if weight: q+=" AND t.capacity_tons>=?"; params.append(weight)
    rows=c.execute(q,params).fetchall(); c.close()
    if not rows: return []
    plat,plng=get_coords(pickup)
    result=[dict(r) for r in rows]
    for r in result: r["d2p"]=round(haversine(r["current_lat"],r["current_lng"],plat,plng),1)
    return sorted(result,key=lambda x:x["d2p"])

def create_booking(cid,tid,did,pu,dr,ttype,goods,weight,priority,notes):
    c=get_conn()
    plat,plng=get_coords(pu); dlat,dlng=get_coords(dr)
    dist=haversine(plat,plng,dlat,dlng); fare=calc_fare(dist,ttype,weight,priority)
    c.execute("""INSERT INTO bookings(customer_id,truck_id,driver_id,pickup_location,drop_location,
        pickup_lat,pickup_lng,drop_lat,drop_lng,truck_type,goods_type,weight_tons,
        distance_km,fare,priority,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (cid,tid,did,pu,dr,plat,plng,dlat,dlng,ttype,goods,round(weight,2),round(dist,1),fare,priority,notes))
    c.execute("UPDATE trucks SET is_available=0 WHERE id=?",(tid,))
    c.execute("UPDATE customers SET total_bookings=total_bookings+1 WHERE id=?",(cid,))
    push("driver",did,f"New {priority} booking: {pu} → {dr}","booking")
    c.commit(); c.close(); return fare,round(dist,1)

def update_status(bid,status,driver_id=None):
    c=get_conn()
    ts={"accepted":"accepted_at","in_transit":"started_at","completed":"completed_at"}.get(status)
    if ts: c.execute(f"UPDATE bookings SET status=?,driver_accepted=1,{ts}=datetime('now') WHERE id=?",(status,bid))
    else: c.execute("UPDATE bookings SET status=?,driver_accepted=1 WHERE id=?",(status,bid))
    if status=="completed" and driver_id:
        r=c.execute("SELECT fare,truck_id,distance_km FROM bookings WHERE id=?",(bid,)).fetchone()
        if r:
            c.execute("UPDATE drivers SET total_earnings=total_earnings+?,total_trips=total_trips+1 WHERE id=?",(r["fare"],driver_id))
            c.execute("UPDATE trucks SET is_available=1,odometer_km=odometer_km+? WHERE id=?",(int(r["distance_km"]),r["truck_id"]))
    if status in("rejected","cancelled"):
        r=c.execute("SELECT truck_id,customer_id FROM bookings WHERE id=?",(bid,)).fetchone()
        if r:
            c.execute("UPDATE trucks SET is_available=1 WHERE id=?",(r["truck_id"],))
            push("customer",r["customer_id"],f"Booking #{bid} {status}.","alert")
    c.commit(); c.close()

def push(utype,uid,msg,ntype="info"):
    c=get_conn(); c.execute("INSERT INTO notifications(user_type,user_id,message,type) VALUES(?,?,?,?)",(utype,uid,msg,ntype)); c.commit(); c.close()

def get_notifs(utype,uid,limit=15):
    c=get_conn(); rows=c.execute("SELECT * FROM notifications WHERE user_type=? AND user_id=? ORDER BY created_at DESC LIMIT ?",(utype,uid,limit)).fetchall(); c.close(); return [dict(r) for r in rows]

def mark_read(utype,uid):
    c=get_conn(); c.execute("UPDATE notifications SET is_read=1 WHERE user_type=? AND user_id=?",(utype,uid)); c.commit(); c.close()

def unread_count(utype,uid):
    c=get_conn(); n=c.execute("SELECT COUNT(*) FROM notifications WHERE user_type=? AND user_id=? AND is_read=0",(utype,uid)).fetchone()[0]; c.close(); return n

def driver_bookings(did):
    c=get_conn()
    rows=c.execute("""SELECT b.*,cu.name as cname,cu.phone as cphone FROM bookings b
        JOIN customers cu ON b.customer_id=cu.id WHERE b.driver_id=? ORDER BY b.created_at DESC""",(did,)).fetchall()
    c.close(); return [dict(r) for r in rows]

def customer_bookings(cid):
    c=get_conn()
    rows=c.execute("""SELECT b.*,d.name as dname,d.phone as dphone,d.rating as drating,
        t.vehicle_no,t.model,t.fuel_level FROM bookings b
        LEFT JOIN drivers d ON b.driver_id=d.id LEFT JOIN trucks t ON b.truck_id=t.id
        WHERE b.customer_id=? ORDER BY b.created_at DESC""",(cid,)).fetchall()
    c.close(); return [dict(r) for r in rows]

def platform_stats():
    c=get_conn()
    def q(sql): return c.execute(sql).fetchone()[0]
    s={
        "drivers":q("SELECT COUNT(*) FROM drivers"),
        "trucks":q("SELECT COUNT(*) FROM trucks"),
        "avail":q("SELECT COUNT(*) FROM trucks WHERE is_available=1"),
        "online":q("SELECT COUNT(*) FROM drivers WHERE is_online=1"),
        "bookings":q("SELECT COUNT(*) FROM bookings"),
        "transit":q("SELECT COUNT(*) FROM bookings WHERE status='in_transit'"),
        "pending":q("SELECT COUNT(*) FROM bookings WHERE status='pending'"),
        "completed":q("SELECT COUNT(*) FROM bookings WHERE status='completed'"),
        "cancelled":q("SELECT COUNT(*) FROM bookings WHERE status='cancelled'"),
        "revenue":c.execute("SELECT COALESCE(SUM(fare),0) FROM bookings WHERE status='completed'").fetchone()[0],
        "avg_fare":c.execute("SELECT COALESCE(AVG(fare),0) FROM bookings WHERE status='completed'").fetchone()[0],
    }
    c.close(); return s

# ═══════════════════════════════════════════════════════════
#  MAP
# ═══════════════════════════════════════════════════════════
def render_map(markers=None,route=None,height=340,zoom=5):
    clat,clng=20.5937,78.9629
    if markers:
        clat=sum(m["lat"] for m in markers)/len(markers)
        clng=sum(m["lng"] for m in markers)/len(markers)
    COLS={"amber":"#f59e0b","blue":"#3b82f6","green":"#10b981","red":"#ef4444","purple":"#8b5cf6"}
    mjs=""
    if markers:
        for m in markers:
            col=COLS.get(m.get("color","amber"),"#f59e0b")
            popup=f"<b style=\\'font-family:Syne;font-size:13px\\'>{m.get('label','')}</b><br><small style=\\'color:#888\\'>{m.get('sub','')}</small>"
            mjs+=f"L.circleMarker([{m['lat']},{m['lng']}],{{radius:11,fillColor:'{col}',color:'#fff',weight:2.5,opacity:1,fillOpacity:.92}}).addTo(map).bindPopup('{popup}');\n"
    rjs=""
    if route and len(route)>=2:
        pts=",".join(f"[{r[0]},{r[1]}]" for r in route)
        rjs=f"""L.polyline([{pts}],{{color:'#f59e0b',weight:3.5,opacity:.88,dashArray:'10,5'}}).addTo(map);
        L.circleMarker([{route[0][0]},{route[0][1]}],{{radius:10,fillColor:'#10b981',color:'#fff',weight:2,fillOpacity:1}}).addTo(map).bindPopup('<b>📦 PICKUP</b>');
        L.circleMarker([{route[-1][0]},{route[-1][1]}],{{radius:10,fillColor:'#ef4444',color:'#fff',weight:2,fillOpacity:1}}).addTo(map).bindPopup('<b>🏁 DESTINATION</b>');"""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body,html{{margin:0;padding:0;background:#050911;}}#map{{width:100%;height:{height}px;}}
.leaflet-tile{{filter:brightness(.6) saturate(.45) hue-rotate(210deg);}}
.leaflet-container{{background:#0a1422;}}
.leaflet-popup-content-wrapper{{background:#0d1828;color:#f1f5f9;border:1px solid #1a2d44;border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,.6);}}
.leaflet-popup-tip{{background:#0d1828;}}</style></head><body>
<div id="map"></div><script>
var map=L.map('map',{{zoomControl:true,attributionControl:false}}).setView([{clat},{clng}],{zoom});
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
{mjs}{rjs}</script></body></html>"""

# ═══════════════════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════════════════
def kpi_card(label,val,delta="",color="a",icon=""):
    st.markdown(f"""<div class="kpi-card kpi-{color}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-val">{val}</div>
      {"<div class='kpi-delta'>▲ "+str(delta)+"</div>" if delta else ""}
    </div>""",unsafe_allow_html=True)

def section(title,icon=""):
    st.markdown(f'<div class="stitle">{icon} {title}</div>',unsafe_allow_html=True)

def badge(status):
    M={"available":("bd-ok","● Available"),"in_transit":("bd-go","◉ In Transit"),
       "pending":("bd-wait","◌ Pending"),"completed":("bd-done","✓ Completed"),
       "accepted":("bd-ok","● Accepted"),"cancelled":("bd-no","✕ Cancelled"),
       "rejected":("bd-no","✕ Rejected"),"loading":("bd-wait","◌ Loading"),
       "1":("bd-ok","● Available"),"0":("bd-red","◉ Busy"),
       "urgent":("bd-red","🔴 Urgent"),"express":("bd-exp","⚡ Express"),
       "normal":("bd-done","● Normal")}
    cls,lbl=M.get(str(status),("bd-wait",str(status).title()))
    return f'<span class="bd {cls}">{lbl}</span>'

def step_bar(current):
    steps=[("📋","Booked"),("✅","Accepted"),("📦","Loading"),("🚛","Transit"),("🏁","Done")]
    idx={"pending":0,"accepted":1,"loading":2,"in_transit":3,"completed":4}.get(current,0)
    html='<div class="stepper">'
    for i,(icon,lbl) in enumerate(steps):
        cls="done" if i<idx else("active" if i==idx else "")
        dot="✓" if i<idx else icon
        html+=f'<div class="step {cls}"><div class="sdot">{dot}</div><div class="slabel">{lbl}</div></div>'
    html+="</div>"
    st.markdown(html,unsafe_allow_html=True)

def pdef():
    return dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                font_color="#94a3b8",margin=dict(t=35,b=0,l=0,r=0),height=250,
                xaxis=dict(gridcolor="#1a2d44"),yaxis=dict(gridcolor="#1a2d44"))

def fuel_bar(level):
    col="#10b981" if level>60 else "#f59e0b" if level>30 else "#ef4444"
    return f'<div class="fuelbar"><span style="color:#64748b;font-size:.7rem">⛽ {level}%</span><div class="fuelwrap"><div class="fuelfill" style="width:{level}%;background:{col}"></div></div></div>'

# ═══════════════════════════════════════════════════════════
#  LANGUAGE SELECTOR  (shown on first visit)
# ═══════════════════════════════════════════════════════════
def language_picker():
    """Full-screen language picker shown before anything else."""
    lang_code = st.session_state.get("lang","")
    if lang_code: return  # already chosen

    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;padding:2rem 0 1.5rem">
      <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
        background:linear-gradient(135deg,#f59e0b,#3b82f6);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;">🚛 TruckX</div>
      <div style="font-size:1.1rem;color:#94a3b8;margin:.5rem 0 2rem">
        {t('select_language','en')}
      </div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(5)
    for i,(lang_name,code) in enumerate(LANGUAGES.items()):
        with cols[i % 5]:
            flag = LANG_FLAGS.get(code,"🌐")
            if st.button(f"{flag} {lang_name}", key=f"lang_{code}", use_container_width=True):
                st.session_state["lang"] = code
                st.rerun()
    st.stop()

# ═══════════════════════════════════════════════════════════
#  ONBOARDING  (shown to new users once)
# ═══════════════════════════════════════════════════════════
def onboarding_banner():
    if st.session_state.get("onboarded"): return
    st.markdown('<div class="scard">',unsafe_allow_html=True)
    section(t("onboard_title"),"🚀")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown(f"""<div class="onboard-step">
          <div class="onboard-num">1</div>
          <div class="onboard-icon">📍</div>
          <div class="onboard-title">{t("onboard_1")}</div>
        </div>""",unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="onboard-step">
          <div class="onboard-num">2</div>
          <div class="onboard-icon">🚛</div>
          <div class="onboard-title">{t("onboard_2")}</div>
        </div>""",unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="onboard-step">
          <div class="onboard-num">3</div>
          <div class="onboard-icon">📡</div>
          <div class="onboard-title">{t("onboard_3")}</div>
        </div>""",unsafe_allow_html=True)
    st.markdown("<br/>",unsafe_allow_html=True)
    if st.button("✅  Got it — Let's go!", use_container_width=True):
        st.session_state["onboarded"]=True; st.rerun()
    st.markdown("</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  PAGE: HOME
# ═══════════════════════════════════════════════════════════
def page_home():
    stats=platform_stats()
    ts=datetime.now().strftime("%H:%M:%S")

    onboarding_banner()

    st.markdown(f"""<div style="padding:.4rem 0 1rem">
      <div class="hero-badge"><span class="ldot"></span>{t('live')} · {ts}</div>
      <div class="hero-title">{t('app_name')}</div>
      <div class="hero-sub">{t('tagline')}</div>
    </div>""",unsafe_allow_html=True)

    c1,c2,c3,c4,c5=st.columns(5)
    with c1: kpi_card(t("online_drivers"),stats["online"],f"of {stats['drivers']}","g","🟢")
    with c2: kpi_card(t("avail_trucks"),stats["avail"],f"of {stats['trucks']}","b","🚛")
    with c3: kpi_card(t("active_trips"),stats["transit"],"In transit","p","📍")
    with c4: kpi_card(t("pending_orders"),stats["pending"],"Awaiting","a","⏳")
    with c5: kpi_card(t("total_revenue"),f"₹{stats['revenue']:,.0f}","Completed","r","💰")

    st.markdown("<br/>",unsafe_allow_html=True)

    col_map,col_feed=st.columns([3,2])
    with col_map:
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section("Live Fleet Map","🗺️")
        c=get_conn(); trucks=c.execute("SELECT * FROM trucks").fetchall(); c.close()
        markers=[{"lat":dict(t)["current_lat"],"lng":dict(t)["current_lng"],
                  "label":dict(t)["vehicle_no"],
                  "sub":f"{dict(t)['truck_type']} · {dict(t)['city']}",
                  "color":"amber" if dict(t)["is_available"] else "blue"} for t in trucks]
        st.components.v1.html(render_map(markers=markers,height=350,zoom=5),height=360)
        st.markdown("<small style='color:#334155'>🟡 Available &nbsp;·&nbsp; 🔵 On Trip</small>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with col_feed:
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section("Live Activity Feed","⚡")
        c=get_conn()
        recent=c.execute("""SELECT b.id,b.status,b.pickup_location,b.drop_location,
            b.created_at,cu.name as cname,b.priority
            FROM bookings b JOIN customers cu ON b.customer_id=cu.id
            ORDER BY b.created_at DESC LIMIT 12""").fetchall(); c.close()
        icons={"completed":"✅","in_transit":"🚛","pending":"⏳","accepted":"✔️","cancelled":"❌","rejected":"❌"}
        st.markdown('<div class="timeline">',unsafe_allow_html=True)
        for r in recent:
            r=dict(r)
            ic=icons.get(r["status"],"📋")
            st.markdown(f"""<div class="tlitem"><div class="tltime">{r['created_at'][:16]}</div>
              <div class="tltext">{ic} <b>#{r['id']}</b> &nbsp;{r['pickup_location']} → {r['drop_location']}
              &nbsp;{badge(r['status'])}&nbsp;{badge(r['priority'])}</div></div>""",unsafe_allow_html=True)
        st.markdown("</div></div>",unsafe_allow_html=True)

    # Analytics
    st.markdown('<div class="scard">',unsafe_allow_html=True)
    section(t("analytics"),"📊")
    c=get_conn()
    sdf=pd.read_sql("SELECT status,COUNT(*) as n FROM bookings GROUP BY status",c)
    tdf=pd.read_sql("SELECT truck_type,COUNT(*) as n FROM bookings GROUP BY truck_type",c)
    rdf=pd.read_sql("SELECT date(created_at) as d,SUM(fare) as rev,COUNT(*) as trips FROM bookings WHERE status='completed' GROUP BY d ORDER BY d",c)
    gdf=pd.read_sql("SELECT goods_type,COUNT(*) as n FROM bookings GROUP BY goods_type",c)
    c.close()
    ca,cb,cc,cd=st.columns(4)
    with ca:
        if not sdf.empty:
            fig=px.pie(sdf,values="n",names="status",hole=.55,
                color_discrete_sequence=["#f59e0b","#10b981","#3b82f6","#ef4444","#8b5cf6","#64748b"])
            fig.update_layout(**pdef(),title=dict(text="Status",font=dict(color="#f59e0b",size=12)))
            fig.update_traces(textinfo="percent",textfont_color="#f1f5f9")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with cb:
        if not tdf.empty:
            fig=px.bar(tdf,x="truck_type",y="n",color="n",color_continuous_scale=["#1a2d44","#f59e0b"])
            fig.update_layout(**pdef(),coloraxis_showscale=False,title=dict(text="By Type",font=dict(color="#f59e0b",size=12)))
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with cc:
        if not rdf.empty:
            fig=go.Figure(go.Scatter(x=rdf["d"],y=rdf["rev"],mode="lines+markers",
                line=dict(color="#3b82f6",width=2.5),marker=dict(color="#f59e0b",size=5),
                fill="tozeroy",fillcolor="rgba(59,130,246,.07)"))
            fig.update_layout(**pdef(),xaxis_showticklabels=False,title=dict(text="Revenue",font=dict(color="#f59e0b",size=12)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with cd:
        if not gdf.empty:
            fig=px.pie(gdf,values="n",names="goods_type",hole=.55,
                color_discrete_sequence=["#10b981","#3b82f6","#f59e0b","#8b5cf6","#ec4899","#ef4444","#34d399","#60a5fa"])
            fig.update_layout(**pdef(),title=dict(text="Goods",font=dict(color="#f59e0b",size=12)))
            fig.update_traces(textinfo="percent",textfont_color="#f1f5f9")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.markdown("</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  ROLE SELECTOR (home screen for new users)
# ═══════════════════════════════════════════════════════════
def role_selector_if_needed(portal):
    """For driver/customer portals, show role choice if not logged in."""
    pass  # handled inline

# ═══════════════════════════════════════════════════════════
#  PAGE: DRIVER
# ═══════════════════════════════════════════════════════════
def page_driver():
    lang=st.session_state.get("lang","en")
    st.markdown(f'<div class="hero-title" style="font-size:2rem;padding:.3rem 0">🚚 {t("nav_driver")}</div>',unsafe_allow_html=True)
    driver=st.session_state.get("driver")

    if not driver:
        tab1,tab2=st.tabs([f"🔑 {t('login')}",f"📝 {t('register')}"])
        with tab1:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            section(t("login_driver"),"🔑")
            c1,c2=st.columns(2)
            with c1: phone=st.text_input(t("phone"),key="dl_ph")
            with c2: pwd=st.text_input(t("password"),type="password",key="dl_pw")
            if st.button(t("login_driver"),use_container_width=True):
                if phone and pwd:
                    d=driver_login(phone,pwd)
                    if d:
                        st.session_state["driver"]=d
                        c=get_conn(); c.execute("UPDATE drivers SET is_online=1 WHERE id=?",(d["id"],)); c.commit(); c.close()
                        st.success(f"✅ {t('welcome')} {d['name']}!"); st.rerun()
                    else: st.error("❌ Invalid credentials. Please check phone/password.")
                else: st.warning(f"⚠️ Please fill all fields.")
            st.info(f"**{t('demo_creds')}:** 📞 9876543210 · 🔑 pass123")
            st.markdown("</div>",unsafe_allow_html=True)
        with tab2:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            section(t("register")+" — "+t("nav_driver"),"📝")
            c1,c2,c3=st.columns(3)
            with c1: name=st.text_input(t("name"),key="dr_n"); email=st.text_input(t("email"),key="dr_e")
            with c2: phone=st.text_input(t("phone"),key="dr_ph"); lic=st.text_input(t("license"),key="dr_l")
            with c3: pwd=st.text_input(t("password"),type="password",key="dr_pw"); exp=st.number_input(t("experience")+" (yrs)",0,50,1,key="dr_x")
            if st.button(t("register"),use_container_width=True):
                if name and phone and pwd and lic:
                    ok,msg=reg_driver(name,phone,email,pwd,lic,exp)
                    st.success(msg) if ok else st.error(msg)
                else: st.warning("Fill required fields.")
            st.markdown("</div>",unsafe_allow_html=True)
        return

    d=driver
    c=get_conn(); fresh=c.execute("SELECT * FROM drivers WHERE id=?",(d["id"],)).fetchone(); c.close()
    if fresh: d=dict(fresh); st.session_state["driver"]=d

    # Header
    hc,bc=st.columns([5,1])
    with hc:
        ob='<span class="bd bd-ok">🟢 ONLINE</span>' if d.get("is_online") else '<span class="bd bd-no">⚫ OFFLINE</span>'
        st.markdown(f"<h3 style='margin:0;font-family:Syne,sans-serif'>👷 {d['name']}</h3>",unsafe_allow_html=True)
        st.markdown(f"{ob} &nbsp;⭐ {d['rating']} &nbsp;|&nbsp; 📞 {d['phone']} &nbsp;|&nbsp; 🪪 {d.get('license_no','')}",unsafe_allow_html=True)
    with bc:
        if st.button(f"🔓 {t('logout')}"):
            c=get_conn(); c.execute("UPDATE drivers SET is_online=0 WHERE id=?",(d["id"],)); c.commit(); c.close()
            del st.session_state["driver"]; st.rerun()

    # Unread notifs
    notifs=get_notifs("driver",d["id"],3); unread=[n for n in notifs if not n["is_read"]]
    for n in unread[:2]: st.markdown(f'<div class="notif">🔔 &nbsp; {n["message"]}</div>',unsafe_allow_html=True)
    if unread: mark_read("driver",d["id"])

    c1,c2,c3,c4=st.columns(4)
    with c1: kpi_card(t("total_trips"),d["total_trips"],"Completed","g","🚛")
    with c2: kpi_card(t("earnings"),f"₹{d['total_earnings']:,.0f}","Lifetime","a","💰")
    with c3: kpi_card(t("rating"),f"⭐ {d['rating']}","Score","b","🌟")
    with c4: kpi_card(t("experience"),f"{d['experience_years']} yrs","On road","p","📅")

    st.markdown("<br/>",unsafe_allow_html=True)
    tb1,tb2,tb3,tb4=st.tabs([f"🚚 {t('my_fleet')}",f"📋 {t('trip_requests')}",f"📊 {t('earnings')}",f"🔔 {t('notifications')}"])

    with tb1:
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section(t("reg_truck"),"➕")
        c1,c2,c3=st.columns(3)
        with c1:
            vno=st.text_input(t("vehicle_no"),placeholder="e.g. MH12AB0001",key="t_v")
            ttype=st.selectbox(t("truck_type"),["Mini Truck","Medium Truck","Heavy Truck","Flatbed","Container"],key="t_t")
        with c2:
            cap=st.number_input(t("capacity"),0.5,40.0,2.0,.5,key="t_c")
            model=st.text_input(t("model"),placeholder="e.g. Tata Ace",key="t_m")
        with c3:
            year=st.number_input(t("year"),2000,2025,2022,key="t_y")
            city=st.selectbox(t("city"),list(CITY_COORDS.keys()),key="t_city")
        if st.button(f"✅ {t('reg_truck')}",use_container_width=True):
            if vno and model:
                ok,msg=reg_truck(d["id"],vno,ttype,cap,model,year,city)
                st.success(msg) if ok else st.error(msg)
            else: st.warning("Fill vehicle number and model.")
        st.markdown("</div>",unsafe_allow_html=True)

        c=get_conn(); my_trucks=c.execute("SELECT * FROM trucks WHERE driver_id=?",(d["id"],)).fetchall(); c.close()
        if my_trucks:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            section(t("my_fleet"),"🏗️")
            for tr in my_trucks:
                tr=dict(tr)
                c1,c2,c3,c4,c5=st.columns([3,2,2,2,2])
                with c1:
                    st.markdown(f"**{tr['vehicle_no']}** &nbsp; {tr['truck_type']}")
                    st.markdown(f"<small style='color:#64748b'>{tr['model']} ({tr['year']}) · 📍 {tr['city']}</small>",unsafe_allow_html=True)
                with c2:
                    st.markdown(f"⚖️ **{tr['capacity_tons']}T**")
                    st.markdown(f"🛣️ {tr['odometer_km']:,} km")
                with c3: st.markdown(fuel_bar(tr["fuel_level"]),unsafe_allow_html=True)
                with c4: st.markdown(badge(str(tr["is_available"])),unsafe_allow_html=True)
                with c5:
                    ns=1 if not tr["is_available"] else 0
                    lbl=t("set_available") if not tr["is_available"] else t("set_busy")
                    if st.button(lbl,key=f"av_{tr['id']}"):
                        c2x=get_conn(); c2x.execute("UPDATE trucks SET is_available=? WHERE id=?",(ns,tr["id"])); c2x.commit(); c2x.close(); st.rerun()
                st.divider()
            st.markdown("</div>",unsafe_allow_html=True)

    with tb2:
        bookings=driver_bookings(d["id"])
        pending=[b for b in bookings if b["status"]=="pending"]
        active=[b for b in bookings if b["status"] in("accepted","loading","in_transit")]
        others=[b for b in bookings if b["status"] not in("pending","accepted","loading","in_transit")]

        if pending:
            st.markdown(f'<div class="notif">⚡ &nbsp; <b>{len(pending)} {t("trip_requests")} waiting!</b></div>',unsafe_allow_html=True)
        if not bookings: st.info(t("no_data")); return

        r1,r2,r3=st.tabs([f"⏳ {t('status_pending')} ({len(pending)})",f"🚛 Active ({len(active)})",f"📜 {t('history')} ({len(others)})"])

        with r1:
            if not pending: st.info(t("no_data"))
            for b in pending:
                urg="urgent" if b["priority"]=="urgent" else ""
                st.markdown(f'<div class="tcard {urg}">',unsafe_allow_html=True)
                c1,c2,c3=st.columns([4,2,2])
                with c1:
                    st.markdown(f"**#{b['id']}** &nbsp;{badge(b['priority'])}",unsafe_allow_html=True)
                    st.markdown(f"📍 **{b['pickup_location']}** → **{b['drop_location']}**")
                    st.markdown(f"<small>📦 {b['goods_type']} · ⚖️ {b['weight_tons']}T · 📏 {b['distance_km']}km · ⏱ {eta_str(b['distance_km'])}</small>",unsafe_allow_html=True)
                    st.markdown(f"<small style='color:#475569'>👤 {b['cname']} · 📞 {b['cphone']}</small>",unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div class='farebox'><div class='farelabel'>{t('fare')}</div><div class='fareamt'>₹{b['fare']:,.0f}</div></div>",unsafe_allow_html=True)
                with c3:
                    st.markdown("<br/>",unsafe_allow_html=True)
                    if st.button(f"✅ {t('accept')}",key=f"acc_{b['id']}"):
                        update_status(b["id"],"accepted",d["id"])
                        push("customer",b["customer_id"],f"Driver {d['name']} accepted booking #{b['id']}!","success")
                        st.success("Accepted!"); st.rerun()
                    if st.button(f"❌ {t('reject')}",key=f"rej_{b['id']}"):
                        update_status(b["id"],"rejected",d["id"]); st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)

        with r2:
            if not active: st.info(t("no_data"))
            for b in active:
                st.markdown('<div class="tcard active">',unsafe_allow_html=True)
                step_bar(b["status"])
                c1,c2,c3=st.columns([4,2,2])
                with c1:
                    st.markdown(f"**#{b['id']}** · {b['pickup_location']} → {b['drop_location']}")
                    st.markdown(f"<small>₹{b['fare']:,.0f} · {b['distance_km']}km · {eta_str(b['distance_km'])}</small>",unsafe_allow_html=True)
                with c2: st.markdown(badge(b["status"])+"<br/>",unsafe_allow_html=True)
                with c3:
                    if b["status"]=="accepted":
                        if st.button(f"📦 {t('start_loading')}",key=f"ld_{b['id']}"): update_status(b["id"],"loading"); st.rerun()
                    elif b["status"]=="loading":
                        if st.button(f"🚛 {t('dispatch')}",key=f"go_{b['id']}"): update_status(b["id"],"in_transit"); st.rerun()
                    elif b["status"]=="in_transit":
                        if st.button(f"🏁 {t('complete')}",key=f"dn_{b['id']}"): update_status(b["id"],"completed",d["id"]); st.success("✅ Earnings updated!"); st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)

        with r3:
            for b in others[:25]:
                c1,c2,c3=st.columns([5,2,2])
                with c1:
                    st.markdown(f"**#{b['id']}** · {b['pickup_location']} → {b['drop_location']}")
                    st.markdown(f"<small style='color:#475569'>{b['goods_type']} · {b['created_at'][:10]}</small>",unsafe_allow_html=True)
                with c2: st.markdown(f"**₹{b['fare']:,.0f}**")
                with c3: st.markdown(badge(b["status"]),unsafe_allow_html=True)
                st.divider()

    with tb3:
        completed=[b for b in bookings if b["status"]=="completed"]
        c1,c2,c3,c4=st.columns(4)
        avg=d["total_earnings"]/max(d["total_trips"],1)
        c1.metric("Total Earned",f"₹{d['total_earnings']:,.0f}")
        c2.metric("Trips Done",d["total_trips"])
        c3.metric("Avg/Trip",f"₹{avg:,.0f}")
        c4.metric("Rating",f"⭐ {d['rating']}")
        if completed:
            df=pd.DataFrame(completed); df["date"]=df["created_at"].str[:10]
            daily=df.groupby("date")["fare"].sum().reset_index(); daily.columns=["Date","₹"]
            fig=px.area(daily,x="Date",y="₹",color_discrete_sequence=["#f59e0b"])
            fig.update_layout(**pdef(),xaxis_showticklabels=False,title=dict(text="Daily Earnings",font=dict(color="#f59e0b",size=13)))
            fig.update_traces(fillcolor="rgba(245,158,11,.08)",line_width=2.5)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with tb4:
        all_n=get_notifs("driver",d["id"])
        if not all_n: st.info(t("no_data"))
        for n in all_n:
            ic={"booking":"📦","alert":"⚠️","success":"✅"}.get(n["type"],"🔔")
            bg="rgba(245,158,11,.05)" if not n["is_read"] else "transparent"
            st.markdown(f'<div style="background:{bg};border:1px solid #1a2d44;border-radius:11px;padding:.7rem 1rem;margin-bottom:.45rem"><small style="color:#475569;font-family:JetBrains Mono,monospace">{n["created_at"][:16]}</small><br>{ic} {n["message"]}</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  PAGE: CUSTOMER
# ═══════════════════════════════════════════════════════════
def page_customer():
    st.markdown(f'<div class="hero-title" style="font-size:2rem;padding:.3rem 0">📦 {t("nav_customer")}</div>',unsafe_allow_html=True)
    customer=st.session_state.get("customer")

    if not customer:
        tab1,tab2=st.tabs([f"🔑 {t('login')}",f"📝 {t('register')}"])
        with tab1:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            section(t("login_customer"),"🔑")
            c1,c2=st.columns(2)
            with c1: phone=st.text_input(t("phone"),key="cl_ph")
            with c2: pwd=st.text_input(t("password"),type="password",key="cl_pw")
            if st.button(t("login_customer"),use_container_width=True):
                if phone and pwd:
                    cu=customer_login(phone,pwd)
                    if cu: st.session_state["customer"]=cu; st.success(f"✅ {t('welcome')} {cu['name']}!"); st.rerun()
                    else: st.error("❌ Invalid credentials.")
                else: st.warning("Fill all fields.")
            st.info(f"**{t('demo_creds')}:** 📞 9111111111 · 🔑 pass123")
            st.markdown("</div>",unsafe_allow_html=True)
        with tab2:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            section(t("register"),"📝")
            c1,c2=st.columns(2)
            with c1: name=st.text_input(t("name"),key="cr_n"); email=st.text_input(t("email"),key="cr_e")
            with c2: phone=st.text_input(t("phone"),key="cr_ph"); pwd=st.text_input(t("password"),type="password",key="cr_pw")
            if st.button(t("register"),use_container_width=True):
                if name and phone and pwd:
                    ok,msg=reg_customer(name,phone,email,pwd)
                    st.success(msg) if ok else st.error(msg)
                else: st.warning("Fill all fields.")
            st.markdown("</div>",unsafe_allow_html=True)
        return

    cu=customer
    c=get_conn(); fresh=c.execute("SELECT * FROM customers WHERE id=?",(cu["id"],)).fetchone(); c.close()
    if fresh: cu=dict(fresh); st.session_state["customer"]=cu

    hc,bc=st.columns([5,1])
    with hc: st.markdown(f"<h3 style='margin:0;font-family:Syne,sans-serif'>👤 {cu['name']}</h3>",unsafe_allow_html=True)
    with bc:
        if st.button(f"🔓 {t('logout')}"): del st.session_state["customer"]; st.rerun()

    notifs=get_notifs("customer",cu["id"],3); unread=[n for n in notifs if not n["is_read"]]
    for n in unread[:2]: st.markdown(f'<div class="notif">🔔 &nbsp; {n["message"]}</div>',unsafe_allow_html=True)
    if unread: mark_read("customer",cu["id"])

    ct1,ct2,ct3,ct4=st.tabs([f"📦 {t('book_truck')}",f"🗺️ {t('track_live')}",f"📜 {t('history')}",f"🔔 {t('notifications')}"])

    with ct1:
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section(t("book_truck"),"📦")
        cities=list(CITY_COORDS.keys())
        c1,c2=st.columns(2)
        with c1:
            pickup=st.selectbox(f"📍 {t('pickup_city')}",cities,key="b_pu")
            goods=st.selectbox(f"📦 {t('goods_type')}",["Electronics","FMCG","Chemicals","Machinery","Textiles","Furniture","Perishables","Pharmaceuticals","Auto Parts","Other"],key="b_g")
            ttype=st.selectbox(f"🚛 {t('truck_type')}",["Any","Mini Truck","Medium Truck","Heavy Truck","Flatbed","Container"],key="b_t",
                help="Mini=<2T · Medium=2-7T · Heavy=7-15T · Flatbed=machinery · Container=20T+")
        with c2:
            drop=st.selectbox(f"🏁 {t('drop_city')}",[c for c in cities if c!=pickup],key="b_dr")
            weight=st.number_input(f"⚖️ {t('weight')}",0.1,30.0,1.0,0.1,key="b_w")
            priority=st.selectbox(f"⚡ {t('priority')}",["normal","express","urgent"],key="b_p",
                help="Normal=standard · Express=+35% faster · Urgent=+65% highest priority")
        notes=st.text_area(f"📝 {t('notes')}",height=55,key="b_notes")
        st.markdown("</div>",unsafe_allow_html=True)

        # Live fare estimate
        plat,plng=get_coords(pickup); dlat,dlng=get_coords(drop)
        dist=haversine(plat,plng,dlat,dlng)
        est_fare=calc_fare(dist,ttype if ttype!="Any" else "Medium Truck",weight,priority)
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section("Instant Quote","💡")
        fc1,fc2,fc3=st.columns(3)
        with fc1: kpi_card(t("distance"),f"{dist:.0f} km","Estimated","b","📏")
        with fc2: kpi_card(t("est_fare"),f"₹{est_fare:,.0f}",f"{priority} rate","a","💰")
        with fc3: kpi_card(t("eta"),eta_str(dist),"Approx","g","⏱")
        st.markdown("</div>",unsafe_allow_html=True)

        if st.button(f"🔍 {t('search_trucks')}",use_container_width=True):
            trucks=find_trucks(ttype,pickup,weight)
            st.session_state["ft"]=trucks
            st.session_state["bp"]={"pickup":pickup,"drop":drop,"ttype":ttype,"goods":goods,"weight":weight,"priority":priority,"notes":notes}
            if not trucks: st.error(f"❌ {t('no_data')}. Try 'Any' truck type.")

        if "ft" in st.session_state and st.session_state["ft"]:
            trucks=st.session_state["ft"]
            st.markdown(f"<br/>**{len(trucks)} {t('avail_trucks')}** — sorted by proximity:",unsafe_allow_html=False)
            markers=[{"lat":tr["current_lat"],"lng":tr["current_lng"],"label":tr["vehicle_no"],
                       "sub":f"{tr['truck_type']} · {tr['city']}","color":"amber"} for tr in trucks[:5]]
            markers.append({"lat":plat,"lng":plng,"label":f"📍 {pickup}","sub":"Pickup","color":"green"})
            st.components.v1.html(render_map(markers=markers,height=260),height=270)
            st.markdown("<br/>",unsafe_allow_html=False)
            for tr in trucks[:6]:
                fare_t=calc_fare(dist,tr["truck_type"],weight,st.session_state["bp"]["priority"])
                st.markdown('<div class="tcard">',unsafe_allow_html=True)
                c1,c2,c3,c4=st.columns([4,2,2,2])
                with c1:
                    st.markdown(f"**{tr['vehicle_no']}** &nbsp;{badge('available')}",unsafe_allow_html=True)
                    st.markdown(f"🚛 {tr['model']} ({tr['year']}) · 📍 {tr['city']}")
                    st.markdown(f"<small>⚖️ {tr['capacity_tons']}T · ⭐ {tr['rating']} · {tr['total_trips']} trips</small>",unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{t('distance')}:** ~{tr['d2p']} km")
                    st.markdown(f"**ETA:** {eta_str(tr['d2p'])}")
                with c3:
                    st.markdown(f"<div class='farebox' style='padding:.7rem'><div class='farelabel'>{t('fare')}</div><div class='fareamt' style='font-size:1.6rem'>₹{fare_t:,.0f}</div></div>",unsafe_allow_html=True)
                with c4:
                    st.markdown("<br/>",unsafe_allow_html=True)
                    if st.button(f"📦 {t('book_now')}",key=f"bk_{tr['id']}"):
                        bp=st.session_state["bp"]
                        ff,df2=create_booking(cu["id"],tr["id"],tr["driver_id"],
                            bp["pickup"],bp["drop"],tr["truck_type"],bp["goods"],
                            bp["weight"],bp["priority"],bp["notes"])
                        del st.session_state["ft"]
                        st.success(f"✅ Booked! {t('fare')}: ₹{ff:,.0f} · {t('distance')}: {df2} km")
                        st.balloons(); st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)

    with ct2:
        bookings=customer_bookings(cu["id"])
        active=[b for b in bookings if b["status"] in("pending","accepted","loading","in_transit")]
        if not active: st.info(f"📭 {t('no_data')} — all your trips appear here when active.")
        for b in active:
            st.markdown('<div class="scard">',unsafe_allow_html=True)
            st.markdown(f"**Shipment #{b['id']}** &nbsp;{badge(b['status'])}&nbsp;{badge(b['priority'])}",unsafe_allow_html=True)
            step_bar(b["status"])
            pct={"pending":10,"accepted":30,"loading":55,"in_transit":80,"completed":100}.get(b["status"],0)
            st.markdown(f'<div class="progwrap"><div class="progfill" style="width:{pct}%"></div></div>',unsafe_allow_html=True)
            st.markdown(f"<small style='color:#475569'>Progress: {pct}% · ETA: {eta_str(b['distance_km'])}</small>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                st.markdown(f"📍 **{t('pickup_city')}:** {b['pickup_location']}")
                st.markdown(f"🏁 **{t('drop_city')}:** {b['drop_location']}")
                st.markdown(f"📦 **{t('goods_type')}:** {b['goods_type']} · ⚖️ {b['weight_tons']}T")
                st.markdown(f"💰 **{t('fare')}:** ₹{b['fare']:,.0f} · 📏 {b['distance_km']} km")
            with c2:
                st.markdown(f"🚛 **Vehicle:** {b.get('vehicle_no','Assigning...')}")
                st.markdown(f"👷 **Driver:** {b.get('dname','Assigning...')}")
                st.markdown(f"📞 **Contact:** {b.get('dphone','N/A')}")
                st.markdown(f"⭐ **Rating:** {b.get('drating','N/A')}")
            route=[(b["pickup_lat"],b["pickup_lng"]),(b["drop_lat"],b["drop_lng"])]
            st.components.v1.html(render_map(route=route,height=260),height=270)
            st.markdown("</div>",unsafe_allow_html=True)

    with ct3:
        bookings=customer_bookings(cu["id"])
        if not bookings: st.info(t("no_data"))
        ts=sum(b["fare"] for b in bookings if b["status"]=="completed")
        td=sum(b["distance_km"] for b in bookings)
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Total Bookings",len(bookings)); c2.metric("Completed",sum(1 for b in bookings if b["status"]=="completed"))
        c3.metric("Total Spent",f"₹{ts:,.0f}"); c4.metric("Distance",f"{td:,.0f} km")
        st.markdown("<br/>",unsafe_allow_html=False)
        for b in bookings[:30]:
            st.markdown('<div class="tcard">',unsafe_allow_html=True)
            c1,c2,c3,c4=st.columns([5,2,2,2])
            with c1:
                st.markdown(f"**#{b['id']}** &nbsp;{b['pickup_location']} → {b['drop_location']}")
                st.markdown(f"<small style='color:#475569'>📦 {b['goods_type']} · ⚖️ {b['weight_tons']}T · 📏 {b['distance_km']}km · {b['created_at'][:10]}</small>",unsafe_allow_html=True)
            with c2: st.markdown(f"**₹{b['fare']:,.0f}**")
            with c3: st.markdown(badge(b["status"]),unsafe_allow_html=True)
            with c4: st.markdown(badge(b["priority"]),unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)

    with ct4:
        all_n=get_notifs("customer",cu["id"])
        if not all_n: st.info(t("no_data"))
        for n in all_n:
            ic={"booking":"📦","alert":"⚠️","success":"✅"}.get(n["type"],"🔔")
            bg="rgba(245,158,11,.05)" if not n["is_read"] else "transparent"
            st.markdown(f'<div style="background:{bg};border:1px solid #1a2d44;border-radius:11px;padding:.7rem 1rem;margin-bottom:.45rem"><small style="color:#475569;font-family:JetBrains Mono,monospace">{n["created_at"][:16]}</small><br>{ic} {n["message"]}</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  PAGE: ADMIN
# ═══════════════════════════════════════════════════════════
def page_admin():
    st.markdown(f'<div class="hero-title" style="font-size:2rem;padding:.3rem 0">⚙️ {t("admin_center")}</div>',unsafe_allow_html=True)
    if not st.session_state.get("admin_auth"):
        st.markdown('<div class="scard">',unsafe_allow_html=True)
        section("Admin Authentication","🔐")
        c1,_=st.columns([1,2])
        with c1:
            pwd=st.text_input(t("password"),type="password",key="adm_pw")
            if st.button("Authenticate"):
                if pwd=="admin123": st.session_state["admin_auth"]=True; st.rerun()
                else: st.error("Wrong password. Hint: admin123")
        st.markdown("</div>",unsafe_allow_html=True); return

    ch,cb=st.columns([5,1])
    with ch: st.markdown('<span class="bd bd-ok">🟢 ADMIN · FULL ACCESS</span>',unsafe_allow_html=True)
    with cb:
        if st.button(f"🔓 {t('logout')}"): del st.session_state["admin_auth"]; st.rerun()

    stats=platform_stats()
    c1,c2,c3,c4,c5,c6=st.columns(6)
    with c1: kpi_card("Drivers",stats["drivers"],f"{stats['online']} online","g","👷")
    with c2: kpi_card("Fleet",stats["trucks"],f"{stats['avail']} avail","b","🚛")
    with c3: kpi_card("Bookings",stats["bookings"],f"{stats['pending']} pending","a","📋")
    with c4: kpi_card("In Transit",stats["transit"],"Now","p","📍")
    with c5: kpi_card("Completed",stats["completed"],"All time","g","✅")
    with c6: kpi_card("Revenue",f"₹{stats['revenue']:,.0f}",f"Avg ₹{stats['avg_fare']:,.0f}","r","💰")

    st.markdown("<br/>",unsafe_allow_html=True)
    at1,at2,at3,at4,at5=st.tabs(["👷 Drivers","🚛 Fleet","📋 Bookings",f"📊 {t('analytics')}",f"⚙️ {t('operations')}"])

    c=get_conn()
    with at1:
        df=pd.read_sql("SELECT id,name,phone,license_no,experience_years,rating,total_trips,ROUND(total_earnings,0) as earnings,CASE WHEN is_online=1 THEN '🟢' ELSE '⚫' END as online,date(created_at) as joined FROM drivers ORDER BY total_earnings DESC",c)
        st.dataframe(df,use_container_width=True,hide_index=True,
            column_config={"rating":st.column_config.ProgressColumn("⭐Rating",min_value=0,max_value=5,format="%.1f")})

    with at2:
        df=pd.read_sql("""SELECT t.id,t.vehicle_no,t.truck_type,t.capacity_tons,t.model,t.year,
            CASE WHEN t.is_available=1 THEN '✅' ELSE '🔴' END as status,
            t.city,t.fuel_level,t.odometer_km,d.name as driver
            FROM trucks t JOIN drivers d ON t.driver_id=d.id ORDER BY t.id""",c)
        st.dataframe(df,use_container_width=True,hide_index=True,
            column_config={"fuel_level":st.column_config.ProgressColumn("Fuel%",min_value=0,max_value=100,format="%d%%")})

    with at3:
        df=pd.read_sql("""SELECT b.id,cu.name as customer,COALESCE(d.name,'Unassigned') as driver,
            b.pickup_location,b.drop_location,b.goods_type,b.weight_tons,b.distance_km,
            ROUND(b.fare,0) as fare,b.status,b.priority,date(b.created_at) as date
            FROM bookings b JOIN customers cu ON b.customer_id=cu.id
            LEFT JOIN drivers d ON b.driver_id=d.id ORDER BY b.created_at DESC""",c)
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.markdown('<div class="scard">',unsafe_allow_html=True); section("Update Booking","⚙️")
        cx1,cx2,cx3=st.columns(3)
        with cx1: bid=st.number_input("Booking ID",1,9999,1,key="a_bid")
        with cx2: new_st=st.selectbox("New Status",["pending","accepted","loading","in_transit","completed","cancelled"],key="a_st")
        with cx3:
            st.markdown("<br/>",unsafe_allow_html=True)
            if st.button("Update Status"):
                update_status(bid,new_st); st.success(f"Booking #{bid} → {new_st}"); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)

    with at4:
        sdf=pd.read_sql("SELECT status,COUNT(*) as n FROM bookings GROUP BY status",c)
        tdf=pd.read_sql("SELECT truck_type,COUNT(*) as n FROM bookings GROUP BY truck_type",c)
        rdf=pd.read_sql("SELECT date(created_at) as d,SUM(fare) as rev,COUNT(*) as trips FROM bookings WHERE status='completed' GROUP BY d ORDER BY d",c)
        top=pd.read_sql("SELECT name,total_trips,ROUND(total_earnings,0) as earnings,rating FROM drivers ORDER BY total_earnings DESC",c)
        rtdf=pd.read_sql("SELECT pickup_location||' → '||drop_location as route,COUNT(*) as trips,ROUND(SUM(fare),0) as revenue FROM bookings WHERE status='completed' GROUP BY route ORDER BY trips DESC LIMIT 8",c)

        cx1,cx2=st.columns(2)
        with cx1:
            if not sdf.empty:
                fig=px.pie(sdf,values="n",names="status",hole=.52,color_discrete_sequence=["#f59e0b","#10b981","#3b82f6","#ef4444","#8b5cf6","#64748b"])
                fig.update_layout(**pdef(),title=dict(text="Booking Status",font=dict(color="#f59e0b",size=13)))
                fig.update_traces(textfont_color="#f1f5f9")
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        with cx2:
            if not tdf.empty:
                fig=px.bar(tdf,x="truck_type",y="n",color="n",color_continuous_scale=["#1a2d44","#3b82f6"])
                fig.update_layout(**pdef(),coloraxis_showscale=False,title=dict(text="Volume by Type",font=dict(color="#f59e0b",size=13)))
                fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        if not rdf.empty:
            fig=make_subplots(specs=[[{"secondary_y":True}]])
            fig.add_trace(go.Bar(x=rdf["d"],y=rdf["rev"],name="Revenue ₹",marker_color="rgba(59,130,246,.65)",marker_line_width=0),secondary_y=False)
            fig.add_trace(go.Scatter(x=rdf["d"],y=rdf["trips"],name="Trips",line=dict(color="#f59e0b",width=2.5),mode="lines+markers",marker=dict(size=5)),secondary_y=True)
            fig.update_layout(**pdef(),height=260,legend=dict(bgcolor="rgba(0,0,0,0)"),xaxis_showticklabels=False,
                title=dict(text="Revenue & Trips Trend",font=dict(color="#f59e0b",size=13)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        cx1,cx2=st.columns(2)
        with cx1:
            st.markdown('<div class="scard">',unsafe_allow_html=True); section("🏆 Top Drivers")
            st.dataframe(top,use_container_width=True,hide_index=True,
                column_config={"rating":st.column_config.ProgressColumn("Rating",min_value=0,max_value=5,format="%.1f")})
            st.markdown("</div>",unsafe_allow_html=True)
        with cx2:
            if not rtdf.empty:
                st.markdown('<div class="scard">',unsafe_allow_html=True); section("🗺️ Top Routes")
                st.dataframe(rtdf,use_container_width=True,hide_index=True)
                st.markdown("</div>",unsafe_allow_html=True)

    with at5:
        st.markdown('<div class="scard">',unsafe_allow_html=True); section("Fleet Control","🔧")
        cx1,cx2=st.columns(2)
        with cx1:
            st.markdown("**Release All Trucks**")
            if st.button("✅ Set All Available"):
                c2=get_conn(); c2.execute("UPDATE trucks SET is_available=1"); c2.commit(); c2.close(); st.success("Done!")
        with cx2:
            st.markdown("**Cancel All Pending Bookings**")
            if st.button("❌ Cancel All Pending"):
                c2=get_conn()
                tids=c2.execute("SELECT truck_id FROM bookings WHERE status='pending'").fetchall()
                c2.execute("UPDATE bookings SET status='cancelled' WHERE status='pending'")
                for ti in tids: c2.execute("UPDATE trucks SET is_available=1 WHERE id=?",(ti[0],))
                c2.commit(); c2.close(); st.success("Done!")
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown('<div class="scard">',unsafe_allow_html=True); section("System Notifications","🔔")
        ndf=pd.read_sql("SELECT user_type,user_id,message,type,is_read,created_at FROM notifications ORDER BY created_at DESC LIMIT 50",c)
        st.dataframe(ndf,use_container_width=True,hide_index=True)
        st.markdown("</div>",unsafe_allow_html=True)
    c.close()

# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown(f"""<div class="sb-logo">
          <div class="sb-logo-text">🚛 {t('app_name')}</div>
          <div style="font-size:.62rem;color:#334155;letter-spacing:2px;text-transform:uppercase">v4.0 · {t('live')} Multilingual</div>
        </div>""",unsafe_allow_html=True)

        # Clock
        now=datetime.now()
        st.markdown(f"""<div style="text-align:center;padding:.35rem 0;margin-bottom:.5rem">
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.35rem;color:#f59e0b;letter-spacing:2px">{now.strftime("%H:%M:%S")}</div>
          <div style="font-size:.66rem;color:#334155">{now.strftime("%a, %d %b %Y")}</div>
        </div>""",unsafe_allow_html=True)

        # Language switcher in sidebar
        st.markdown(f'<div class="sb-section">🌐 {t("language")}</div>',unsafe_allow_html=True)
        lang_names=list(LANGUAGES.keys()); lang_codes=list(LANGUAGES.values())
        cur_lang_code=st.session_state.get("lang","en")
        cur_lang_name=next((k for k,v in LANGUAGES.items() if v==cur_lang_code),"English")
        chosen=st.selectbox("",lang_names,index=lang_names.index(cur_lang_name),key="lang_sel",label_visibility="collapsed")
        if LANGUAGES[chosen]!=cur_lang_code:
            st.session_state["lang"]=LANGUAGES[chosen]; st.rerun()

        # Live stats
        stats=platform_stats()
        st.markdown(f'<div class="sb-section">📊 Platform Stats</div>',unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#09101e;border:1px solid #1a2d44;border-radius:11px;padding:.8rem;margin-bottom:.7rem">
          <div class="sb-stat"><span class="sb-stat-label">{t("online_drivers")}</span><span class="sb-stat-val" style="color:#10b981">{stats['online']}</span></div>
          <div class="sb-stat"><span class="sb-stat-label">{t("avail_trucks")}</span><span class="sb-stat-val" style="color:#3b82f6">{stats['avail']}</span></div>
          <div class="sb-stat"><span class="sb-stat-label">{t("active_trips")}</span><span class="sb-stat-val" style="color:#f59e0b">{stats['transit']}</span></div>
          <div class="sb-stat"><span class="sb-stat-label">{t("pending_orders")}</span><span class="sb-stat-val" style="color:#ef4444">{stats['pending']}</span></div>
        </div>""",unsafe_allow_html=True)

        # Navigation
        st.markdown(f'<div class="sb-section">🧭 {t("nav_home")}</div>',unsafe_allow_html=True)
        if "page" not in st.session_state: st.session_state["page"]="home"
        for label,key in [(f"🏠 {t('nav_home')}","home"),(f"🚚 {t('nav_driver')}","driver"),(f"📦 {t('nav_customer')}","customer"),(f"⚙️ {t('nav_admin')}","admin")]:
            if st.button(label,key=f"nav_{key}",use_container_width=True):
                st.session_state["page"]=key; st.rerun()

        st.markdown("<br/>",unsafe_allow_html=True)

        # Active sessions
        drv=st.session_state.get("driver"); cst=st.session_state.get("customer"); adm=st.session_state.get("admin_auth")
        if drv or cst or adm:
            st.markdown('<div class="sb-section">Active Sessions</div>',unsafe_allow_html=True)
        if drv:
            nc=unread_count("driver",drv["id"])
            st.markdown(f"""<div class="sb-user">
              <div style="font-size:.66rem;color:#10b981;font-weight:700;text-transform:uppercase">🚛 {t('nav_driver')}</div>
              <div style="font-weight:600;margin:.12rem 0">{drv['name']}</div>
              <div style="font-size:.72rem;color:#64748b">⭐ {drv['rating']} · {drv['total_trips']} trips</div>
              {"<div style='font-size:.7rem;color:#f59e0b'>🔔 "+str(nc)+" unread</div>" if nc else ""}
            </div>""",unsafe_allow_html=True)
        if cst:
            nc=unread_count("customer",cst["id"])
            st.markdown(f"""<div class="sb-user">
              <div style="font-size:.66rem;color:#3b82f6;font-weight:700;text-transform:uppercase">📦 {t('nav_customer')}</div>
              <div style="font-weight:600;margin:.12rem 0">{cst['name']}</div>
              <div style="font-size:.72rem;color:#64748b">{cst['total_bookings']} bookings</div>
              {"<div style='font-size:.7rem;color:#f59e0b'>🔔 "+str(nc)+" unread</div>" if nc else ""}
            </div>""",unsafe_allow_html=True)
        if adm:
            st.markdown("""<div class="sb-user">
              <div style="font-size:.66rem;color:#f59e0b;font-weight:700;text-transform:uppercase">⚙️ Admin</div>
              <div style="font-weight:600;margin:.12rem 0">Administrator</div>
              <div style="font-size:.72rem;color:#10b981">Full access</div>
            </div>""",unsafe_allow_html=True)

        st.markdown("<br/>",unsafe_allow_html=True)
        with st.expander("⚙️ Settings"):
            if st.checkbox("Auto-refresh (30s)",key="auto_r"):
                time.sleep(0.3); st.rerun()
            if st.button("🌐 Reset Language",key="reset_lang"):
                del st.session_state["lang"]; st.session_state.pop("onboarded",None); st.rerun()

        st.markdown(f"<div style='font-size:.6rem;color:#1a2d44;text-align:center;margin-top:.8rem;padding-top:.5rem;border-top:1px solid #09101e'>TruckX v4.0 · {t('tagline')}</div>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════
def main():
    st.markdown(CSS,unsafe_allow_html=True)
    language_picker()   # blocks until language chosen
    init_db()
    sidebar()

    page=st.session_state.get("page","home")
    if   page=="home":     page_home()
    elif page=="driver":   page_driver()
    elif page=="customer": page_customer()
    elif page=="admin":    page_admin()

    st.markdown(f"<div style='text-align:center;color:#1a2d44;font-size:.68rem;padding:1.5rem 0;margin-top:2rem;border-top:1px solid #09101e'>TruckX v4.0 · {t('tagline')} · 2026</div>",unsafe_allow_html=True)

if __name__=="__main__":
    main()

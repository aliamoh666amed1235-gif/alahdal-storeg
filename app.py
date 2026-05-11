import requests
from flask import Flask, request

app = Flask(__name__)

API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDc1OTMzMjAsImlhdCI6MTc3NjA1NzMyMCwicmF5IjoiZDI3NzgzZjZjNzVkOTU2ZWQ2OGUwM2UwMDgyZDY0MWMiLCJzdWIiOjM5NjY2MTN9.rlJ7TV2fciPzHJJuqD8KTBefnuE2q_yBbq5g2r_ZZwypfJKXCPwwg96Tm-Y4JE8-i6XG0zgbkskWXsd_40lWo04pFT-3vNpQSeiuv_Nl4oCDWUi_-x5sgdy6RaWzM3F5dt8kTQidrVMrsv6px4wMdHiflik17y6IRi-HPg_0NjN0EHxezttmov5fvq9JWNUhM68RV74ns4CfZxcf9rdjhhiHDLVGG5Vb0c7sLqjdgsL120FulUq0MGzqQxJkSaAjLfOdXK1HPgFcHZlRoa03lgTHUhjckguuXr3WGHl86Rh4Se_tPxiLFjT5Y5ezh1e-IUFYkwRjBCcdKHzxeNciJw"
MY_PHONE = "737214512"
HEADERS = {'Authorization': f'Bearer {API_TOKEN}', 'Accept': 'application/json'}

def get_balance():
    try:
        r = requests.get('https://5sim.net/v1/user/profile', headers=HEADERS)
        return r.json().get('balance', 0)
    except: return 0

@app.route('/')
def home():
    balance = get_balance()
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الأهدل للأرقام</title>
        <style>
            body {{ font-family: sans-serif; background: #f0f2f5; text-align: center; padding: 20px; }}
            .container {{ background: white; max-width: 500px; margin: auto; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
            .header-box {{ background: #1a237e; color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; }}
            input, select, button {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #ddd; }}
            button {{ background: #27ae60; color: white; border: none; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-box">
                <h1>الأهدل للأرقام الوهمية</h1>
                <p>رصيد النظام: {balance} روبل</p>
            </div>
            <p>حول إلى الحساب: {MY_PHONE}</p>
            <form action="/order" method="post">
                <select name="config">
                    <option value="usa/whatsapp">واتساب - أمريكا (1500 ريال)</option>
                    <option value="russia/telegram">تيليجرام - روسيا (1200 ريال)</option>
                </select>
                <input type="text" name="name" placeholder="اسمك الكريم" required>
                <input type="number" name="ref" placeholder="رقم العملية" required>
                <button type="submit">إرسال الطلب</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/order', methods=['POST'])
def order():
    config = request.form.get('config')
    name = request.form.get('name')
    ref = request.form.get('ref')
    msg = f"طلب رقم جديد:\\nالعميل: {name}\\nالطلب: {config}\\nالمرجع: {ref}"
    whatsapp_url = f"https://wa.me/967{MY_PHONE}?text={msg}"
    return f'<body style="text-align:center; direction:rtl; padding:50px;"><h2>تم استلام طلبك!</h2><a href="{{whatsapp_url}}" style="padding:15px; background:#25D366; color:white; text-decoration:none; border-radius:10px;">تأكيد عبر واتساب</a></body>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

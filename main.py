from flask import Flask, request, render_template_string
import sqlite3

def ዳታቤዙን_አዘምን():
    ግንኙነት = sqlite3.connect("ከተማ_መረጃ.db")
    ጠቋሚ = ግንኙነት.cursor()
    try:
        ጠቋሚ.execute("ALTER TABLE ቦታዎች ADD COLUMN ምድብ TEXT DEFAULT '🏡 መኖሪያ እና ሌሎች ሰፈሮች'")
    except: pass
    try:
        ጠቋሚ.execute("ALTER TABLE ቦታዎች ADD COLUMN ካርታ TEXT")
    except: pass
    
    ጠቋሚ.execute("UPDATE ቦታዎች SET ካርታ = 'https://www.google.com/maps/search/?api=1&query=' || ስም || '+Addis+Ababa' WHERE ካርታ IS NULL")
    ግንኙነት.commit()
    ግንኙነት.close()

ዳታቤዙን_አዘምን()

አፕ = Flask(__name__)

HTML_ዲዛይን = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>የአዲስ አበባን ይወቁ</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
        
        body { 
            font-family: 'Noto Sans Ethiopic', sans-serif; 
            margin: 0; 
            min-height: 100vh; 
            background: linear-gradient(rgba(15, 32, 67, 0.7), rgba(15, 32, 67, 0.85)), url('https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3?q=80&w=1200&auto=format&fit=crop') no-repeat center center fixed;
            background-size: cover;
            display: flex; 
            flex-direction: column;
            align-items: center; 
            padding: 30px 20px;
        }
        
        .container { 
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 40px 30px; 
            border-radius: 24px; 
            box-shadow: 0px 20px 40px rgba(0,0,0,0.4); 
            width: 100%; 
            max-width: 460px;
            text-align: center;
            box-sizing: border-box;
            margin-bottom: 35px;
            color: #ffffff;
        }
        
        .header-icon { font-size: 55px; margin-bottom: 5px; }
        h2 { color: #ffffff; font-size: 28px; margin-bottom: 8px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        p.subtitle { color: #e0e0e0; font-size: 15px; margin-bottom: 30px; }
        
        input[type="text"], textarea, select { 
            font-size: 16px; padding: 14px 18px; width: 100%; border-radius: 14px; 
            border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 18px;
            box-sizing: border-box; font-family: inherit; outline: none;
            background: rgba(255, 255, 255, 0.9); color: #2c3e50;
        }
        
        input:focus, textarea:focus, select:focus { border-color: #00f2fe; box-shadow: 0 0 12px rgba(0, 242, 254, 0.5); background: #ffffff; }
        
        .btn { 
            background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; padding: 16px; 
            border: none; border-radius: 14px; cursor: pointer; font-size: 18px; 
            font-weight: bold; width: 100%; box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4);
        }
        .btn:hover { transform: translateY(-3px); box-shadow: 0px 10px 25px rgba(0, 114, 255, 0.6); }
        
        .btn-admin { background: linear-gradient(45deg, #11998e, #38ef7d); box-shadow: 0 6px 20px rgba(56, 239, 125, 0.3); }
        
        .result { margin-top: 30px; text-align: left; padding: 25px; border-left: 6px solid #00f2fe; background: rgba(15, 32, 67, 0.6); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); }
        .result h3 { margin-top: 0; color: #00f2fe; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; font-size: 22px; }
        .result p { color: #f5f5f5; line-height: 1.8; font-size: 16px;}
        
        .badge { display: inline-block; background: #f1c40f; color: #2c3e50; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 14px; }
        .category-badge { display: inline-block; background: rgba(0, 242, 254, 0.2); color: #00f2fe; border: 1px solid #00f2fe; padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; margin-bottom: 15px; }
        .maps-btn { display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #ea4335, #ff6b6b); color: white; text-decoration: none; padding: 12px 20px; border-radius: 10px; font-weight: bold; font-size: 15px; margin-top: 15px; }
        
        .alert { padding: 15px; border-radius: 14px; margin-top: 20px; font-weight: bold; font-size: 15px; text-align: center; }
        .alert-success { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }

        optgroup { font-weight: bold; color: #1e3c72; font-size: 15px; background-color: #f0f4f8;}
        option { font-weight: normal; color: #333; background-color: #fff;}
    </style>
</head>
<body>

    <div class="container">
        <div class="header-icon">🌆</div>
        <h2>የአዲስ አበባን ይወቁ</h2>
        <p class="subtitle">የከተማዋን ሰፈሮች እና መገኛቸውን ያስሱ</p>
        
        <input type="text" id="መፈለጊያ_ሳጥን" oninput="ቦታ_ፈልግ()" placeholder="🔍 የሰፈር ስም እዚህ ይጻፉ...">
        
        <form method="POST" action="/">
            <input type="hidden" name="ፎርም_አይነት" value="ፈልግ">
            <select name="የተመረጠው_ቦታ" id="የቦታ_ዝርዝር">
                <option value="" disabled selected>እባክዎ ቦታ ይምረጡ...</option>
                {% for ምድብ, ስሞች in ምድቦች.items() %}
                    <optgroup label="{{ ምድብ }}" class="ምድብ-ግሩፕ">
                        {% for ስም in ስሞች %}
                            <option value="{{ ስም }}" class="ቦታ-አማራጭ">{{ ስም }}</option>
                        {% endfor %}
                    </optgroup>
                {% endfor %}
            </select>
            <button type="submit" class="btn">መረጃ አምጣ</button>
        </form>
        
        {% if ውጤት %}
        <div class="result">
            <span class="category-badge">{{ ውጤት[3] }}</span>
            <h3>📍 {{ ውጤት[0] }}</h3>
            <p><strong>📖 ታሪክ:-</strong> {{ ውጤት[1] }}</p>
            <p><strong>⭐️ ደረጃ:-</strong> <span class="badge">{{ ውጤት[2] }}</span></p>
            <a href="{{ ውጤት[4] }}" target="_blank" class="maps-btn">🗺️ ቦታውን በGoogle Maps እይ</a>
        </div>
        {% endif %}
    </div>

    <div class="container" style="border-top: 5px solid #38ef7d;">
        <div class="header-icon" style="font-size: 45px;">➕</div>
        <h2>አዲስ ቦታ መመዝገቢያ</h2>
        <p class="subtitle">የጎደሉ ሰፈሮችን ታሪክ እዚህ ይጨምሩ</p>
        
        <form method="POST" action="/">
            <input type="hidden" name="ፎርም_አይነት" value="መዝግብ">
            <input type="text" name="አዲስ_ስም" placeholder="የሰፈሩ ስም (ምሳሌ፡ ቦሌ)" required>
            <textarea name="አዲስ_ታሪክ" placeholder="የሰፈሩ ታሪክ ወይም መግለጫ..." rows="3" required></textarea>
            
            <select name="አዲስ_ደረጃ" required>
                <option value="" disabled selected>ደረጃ (ኮከብ) ይምረጡ...</option>
                <option value="5 ኮከብ">⭐⭐⭐⭐⭐ (5 ኮከብ)</option>
                <option value="4 ኮከብ">⭐⭐⭐⭐ (4 ኮከብ)</option>
                <option value="3 ኮከብ">⭐⭐⭐ (3 ኮከብ)</option>
            </select>
            
            <select name="አዲስ_ምድብ" required>
                <option value="" disabled selected>የሰፈሩ ምድብ...</option>
                <option value="🛒 የንግድ ማዕከላት እና ገበያ">🛒 የንግድ ማዕከላት እና ገበያ</option>
                <option value="🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች">🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች</option>
                <option value="🚌 የትራንስፖርት መናኸሪያዎች">🚌 የትራንስፖርት መናኸሪያዎች</option>
                <option value="🏡 መኖሪያ እና ሌሎች ሰፈሮች">🏡 መኖሪያ እና ሌሎች ሰፈሮች</option>
            </select>
            
            <button type="submit" class="btn btn-admin">💾 አዲስ ቦታ መዝግብ</button>
        </form>

        {% if መልዕክት %}
            <div class="alert alert-success">🎉 {{ መልዕክት }}</div>
        {% endif %}
    </div>

    <script>
        function ቦታ_ፈልግ() {
            var ፊደል = document.getElementById("መፈለጊያ_ሳጥን").value.trim();
            var ምድቦች = document.getElementsByClassName("ምድብ-ግሩፕ");
            for (var i = 0; i < ምድቦች.length; i++) {
                var ቦታዎች = ምድቦች[i].getElementsByClassName("ቦታ-አማራጭ");
                var የሚታይ_ቦታ_አለ = false;
                for (var j = 0; j < ቦታዎች.length; j++) {
                    if (ቦታዎች[j].text.indexOf(ፊደል) > -1) {
                        ቦታዎች[j].style.display = ""; የሚታይ_ቦታ_አለ = true;
                    } else { ቦታዎች[j].style.display = "none"; }
                }
                if (የሚታይ_ቦታ_አለ) { ምድቦች[i].style.display = ""; } else { ምድቦች[i].style.display = "none"; }
            }
        }
    </script>
</body>
</html>
"""

def የቦታ_ስሞችን_በምድብ_አምጣ():
    ግንኙነት = sqlite3.connect("ከተማ_መረጃ.db")
    ጠቋሚ = ግንኙነት.cursor()
    ጠቋሚ.execute("SELECT ምድብ, ስም FROM ቦታዎች ORDER BY ምድብ, ስም ASC")
    ውጤቶች = ጠቋሚ.fetchall()
    ግንኙነት.close()
    የተደራጀ_መረጃ = {}
    for ምድብ, ስም in ውጤቶች:
        if ምድብ not in የተደራጀ_መረጃ: የተደራጀ_መረጃ[ምድብ] = []
        የተደራጀ_መረጃ[ምድብ].append(ስም)
    return የተደራጀ_መረጃ

@አፕ.route('/', methods=['GET', 'POST'])
def መነሻ_ገጽ():
    ውጤት = None
    መልዕክት = None
    
    if request.method == 'POST':
        ፎርም_አይነት = request.form.get('ፎርም_አይነት')
        if ፎርም_አይነት == 'ፈልግ':
            የተመረጠው_ቦታ = request.form.get('የተመረጠው_ቦታ')
            if የተመረጠው_ቦታ:
                ግንኙነት = sqlite3.connect("ከተማ_መረጃ.db")
                ጠቋሚ = ግንኙነት.cursor()
                ጠቋሚ.execute("SELECT ስም, ታሪክ, ደረጃ, ምድብ, ካርታ FROM ቦታዎች WHERE ስም=?", (የተመረጠው_ቦታ,))
                ውጤት = ጠቋሚ.fetchone()
                ግንኙነት.close()
        elif ፎርም_አይነት == 'መዝግብ':
            ስም = request.form.get('አዲስ_ስም')
            ታሪክ = request.form.get('አዲስ_ታሪክ')
            ደረጃ = request.form.get('አዲስ_ደረጃ')
            ምድብ = request.form.get('አዲስ_ምድብ')
            ዲፎልት_ካርታ = f"https://www.google.com/maps/search/?api=1&query={ስም}+Addis+Ababa"
            
            ግንኙነት = sqlite3.connect("ከተማ_መረጃ.db")
            ጠቋሚ = ግንኙነት.cursor()
            ጠቋሚ.execute("INSERT INTO ቦታዎች (ስም, ታሪክ, ደረጃ, ምድብ, ካርታ) VALUES (?, ?, ?, ?, ?)", (ስм, ታሪክ, ደረጃ, ምድብ, ዲፎልት_ካርታ))
            ግንኙነት.commit()
            ግንኙነት.close()
            መልዕክት = f"'{ስም}' በተሳካ ሁኔታ በዳታቤዝ ውስጥ ተመዝግቧል!"

    ምድቦች = የቦታ_ስሞችን_በምድብ_አምጣ()
    return render_template_string(HTML_ዲዛይን, ምድቦች=comm, ውጤት=ውጤት, መልዕክት=መልዕክት)

if __name__ == '__main__':
    import os
    # Render ሰርቨር ላይ በሰላም እንዲነሳ የሚያስችለው ዋናው ማስተካከያ
    ፖርት = int(os.environ.get("PORT", 5000))
    አፕ.run(host='0.0.0.0', port=ፖርት)

from flask import Flask, request, render_template_string
import sqlite3
import os

አፕ = Flask(__name__)

# ፍጹም አዲስ የዳታቤዝ ፋይል ስም (ስሙን ቀይረነዋል መረጃው ግዴታ እንዲጫን)
DATABASE_NAME = "ከተማ_መረጃ_ጋለሪ_ሪል.db"

def ዳታቤዙን_አዘምን():
    ግንኙነት = sqlite3.connect(DATABASE_NAME)
    ግንኙነት.execute("PRAGMA foreign_keys = ON")
    ጠቋሚ = ግንኙነት.cursor()
    
    # 1. የቦታዎች ዋና ሰንጠረዥ
    ጠቋሚ.execute("""
        CREATE TABLE IF NOT EXISTS ቦታዎች (
            ስም TEXT PRIMARY KEY,
            ታሪክ TEXT,
            ደረጃ TEXT,
            ምድብ TEXT DEFAULT '🏡 መኖሪያ እና ሌሎች ሰፈሮች',
            ካርታ TEXT
        )
    """)
    
    # 2. የፎቶዎች ሰንጠረዥ
    ጠቋሚ.execute("""
        CREATE TABLE IF NOT EXISTS ቦታ_ፎቶዎች (
            ፎቶ_ሊንክ TEXT PRIMARY KEY,
            ቦታ_ስም TEXT,
            FOREIGN KEY (ቦታ_ስም) REFERENCES ቦታዎች(ስም) ON DELETE CASCADE
        )
    """)
    ግንኙነት.commit()
    
    # 60 ዋና ዋና ሰፈሮች
    ዋና_ቦታዎች = [
        ("ፒያሳ", "የአሮጌዋ አዲስ አበባ ማዕከል፣ ታሪካዊ ህንፃዎችና የመጀመሪያው የጣይቱ ሆቴል መገኛ ሰፈር::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("አራት ኪሎ", "የቤተመንግስት፣ የፓርላማ፣ ታሪካዊው የድል ሃውልት እና የአዲስ አበባ ዩኒቨርሲቲ መገኛ ጥንታዊ እምብርት::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ስድስት ኪሎ", "የሰማዕታት ሃውልት፣ የቅድስት ሥላሴ ካቴድራል እና ብሔራዊ ሙዚየም የሚገኙበት የታሪክ ማዕከል::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("አምስት ኪሎ", "ከአራት ኪሎ ወደ ስድስት ኪሎ በሚወስደው መንገድ ላይ የሚገኝ ታሪካዊ የመስቀለኛ መንገድ ሰፈር::", "3 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ጃንሜዳ", "የጥምቀት በዓል በታላቅ ድምቀት የሚከበርበትና የስፖርት ማዘውተሪያ የሆነው ሰፊው የሜዳ ስፍራ::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ምንሊክ", "ዳግማዊ ምኒልክ ሆስፒታልና ጥንታዊ ታሪካዊ ሰፈሮች የሚገኙበት ታዋቂ አካባቢ::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ፈረንሳይ ሌጋሲዮን", "የመጀመሪያው የፈረንሳይ ኤምባሲ ያረፈበትና ወደ እንጦጦ ተራራ መውጫ የሚገኝ አረንጓዴ ሰፈር::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("እንጦጦ", "አዲስ አበባ ከመቆርቆሯ በፊት የዳግማዊ ምኒልክ መቀመጫ የነበረች፣ አሁን ታላቅ የፓርክና የመዝናኛ ስፍራ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ሽሮ ሜዳ", "በባህላዊ አልባሳት ሽያጭና በሽመና ጥበብ የምትታወቅ፣ በእንጦጦ ግርጌ የምትገኝ ደማቅ ሰፈር::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("እስጢፋኖስ", "ታሪካዊው የቅዱስ እስጢፋኖስ ቤተክርስቲያንና ለአብዮት አደባባይ ቅርብ የሆነው ማራኪ አካባቢ::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ቦሌ ፍቅር አደባባይ", "ለወጣቶች መዝናኛና ለፎቶ ቀረጻ የሚመረጥ ውብ የከተማዋ መናፈሻ አካባቢ::", "4 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ወዳጅነት ፓርክ", "በከተማዋ እምብርት ላይ የሚገኝ፣ ሰው ሰራሽ ሐይቅና ዘመናዊ መዝናኛዎች ያሉት ታላቅ ፓርክ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("ሳይንስ ሙዚየም", "በቅርቡ የተገነባ፣ ሳይንስና ቴክኖሎጂን ለህብረተሰብ የሚያሳይ ዘመናዊና ማራኪ የስነ-ህንፃ ጥበብ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("መስቀል አደባባይ", "የመስቀል ደመራ፣ ታላላቅ ህዝባዊ ስብሰባዎችና ስፖርታዊ እንቅስቃሴዎች የሚደረጉበት የከተማዋ ዋና አደባባይ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("መርካቶ", "የአፍሪካ ትልቁና ታዋቂው የውጭ ክፍት የገበያ ቦታ፣ ሁሉንም አይነት የንግድ ዕቃዎች መገኛ::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቦሌ", "ዘመናዊ የገበያ ማዕከላት፣ ታዋቂ ሆቴሎች፣ ካፌዎችና የባንክ ዋና መሥሪያ ቤቶች መገኛ ዘመናዊ ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሀያ ሁለት (22)", "ደማቅ የምሽት ህይወት፣ ዘመናዊ ህንፃዎችና የንግድ ሱቆች የበዙበት የቦሌ አዋሳኝ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቦሌ መድኃኔዓለም", "የመድኃኔዓለም ቤተክርስቲያን፣ ትላልቅ ሞሎች (Malls) እና ሲኒማ ቤቶች የሚገኙበት የንግድ ማክል::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("አትላስ", "በባህላዊና ዘመናዊ ምግብ ቤቶች፣ በከፍተኛ ሆቴሎችና በንግድ እንቅስቃሴ የምትታወቅ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ኦሎምፒያ", "ትላልቅ ቢሮዎችና የውጭ ድርጅቶች መቀመጫ የሆነች፣ በቦሌ መንገድ ላይ የምትገኝ የንግድ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("መገናኛ", "የከተማዋ ትልቁ የትራፊክና የንግድ መገናኛ፣ የገበያ አዳራሾችና የቢሮ ህንፃዎች መዓት የሞሉበት ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ገርጂ", "ሰፊ የመኖሪያ መንደሮች ያሉትና ፈጣን የንግድና የህንፃ ግንባታ የታየበት ታዋቂ አካባቢ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሲኤምሲ (CMC)", "ከፍተኛ ገቢ ያላቸው ነዋሪዎች የሚኖሩበት ዘመናዊ ቪላዎችና የንግድ ሱቆች ያሉበት ቪአይፒ ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("সািরስ", "በፋብሪካዎችና በጅምላ ንግድ መጋዘኖች የምትታወቅ፣ ወደ ደቡብ መውጫ ያለች የንግድ ቀጠና::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቃሊቲ", "የትላልቅ ኢንዱስትሪዎች፣ የጉምሩክ መጋዘኖችና የጭነት መኪናዎች ማረፊያ የሆነች የንግድ ከተማ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ጎተራ", "በትላልቅ ዘመናዊ ኮንዶሚኒየሞችና በኢንተርክንቲኔንታል የልውውጥ ድልድይ የምትታወቅ የንግድ መገናኛ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ላፍቶ", "ለኢንዱስትሪና ለመኖሪያ ምቹ የሆነች፣ የገበያ ማዕከላትና መዝናኛዎች ያሏት ደቡብ ምዕራብ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሳር ቤት", "የአፍሪካ አንድነት ድርጅት (AU) አቅራቢያ የምትገኝ፣ የፈረስ ማጋለጫ ሜዳና የባንኮች መጋዘን ያለባት ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሜክሲኮ", "የንግድ ማዕከላት፣ የፌደራል ፖሊስ ዋና መሥሪያ ቤትና ትላልቅ ኮሌጆች የሚገኙበት የንግድ እምብርት::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ላጋር", "የምድር ባቡር መናኸሪያ የነበረች ታሪካዊ ጣቢያ፣ አሁን ትልቅ የትራንስፖርትና የህንፃ ልማት ቀጠና::", "5 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ቄራ", "ቀጥታ የትራንስፖርት መገናኛ እና የከተማዋ ትልቁ የስጋ አቅርቦት (የቄራዎች) መገኛ ሰፈር::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ቶታል", "በተለያዩ አቅጣጫዎች የሚሄዱ የህዝብ ማመላለሻዎች መነሻ የሆነች ስልታዊ የትራንስፖርት ጣቢያ::", "3 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ዊንጌት", "ወደ ሰሜን አቅጣጫ (ጎጃም/ጎንደር) ለሚሄዱ አውቶቡሶችና መኪናዎች መውጫ የሆነች ሰሜናዊ በር::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("አውቶቡስ ተራ", "ከአዲስ አበባ ወደ ተለያዩ የሀገሪቱ ክፍሎች ለሚጓዙ የረጅም ርቀት አውቶቡሶች ዋና መናኸሪያ ጣቢያ::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ቃሊቲ መናኸሪያ", "ወደ ምስራቅና ደቡብ የሀገሪቱ ክፍሎች ለሚሄዱ አውቶቡሶች የተዘጋጀ ዘመናዊ መናኸሪያ ጣቢያ::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ላምበረት", "ወደ ሰሜን ምስራቅ (ደብረ ብርሃን/ደሴ) ለሚጓዙ የህዝብ ማመላለሻዎች የተመደበች ደማቅ መናኸሪያ::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("አስኮ", "ወደ አምቦና ምዕራብ ኢትዮጵያ ለሚደረጉ ጉዞዎች መነሻ የሆነች ምዕራባዊ የትራንስፖርት በር::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("አያት ባቡር ጣቢያ", "የአዲስ አበባ ቀላል ባቡር ማጠናቀቂያና ለሲኤምሲ/አያት ነዋሪዎች ዋና የትራንስፖርት መስመር::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("ቃሊቲ ባቡር ጣቢያ", "የቀላል ባቡር ደቡባዊ ማቆሚያና የጥገና ማዕከል፣ ለቃሊቲና ሳሪስ ህዝብ ታላቅ የትራንስፖርት ምንጭ::", "4 ኮከብ", "🚌 የትራንስፖርት መናኸሪያዎች"),
        ("አያት", "ሰፊና ፀጥተኛ የመኖሪያ መንደሮች፣ ቪላዎችና ዘመናዊ አፓርታማዎች የበዙባት የምስራቋ ውብ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ኮተቤ", "የአዲስ አበባ ዩኒቨርሲቲ ኮተቤ ካምፓስ የሚገኝበት፣ ሰፊ የመኖሪያና የትምህርት ቀጠና ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ካራሎ", "በኮተቤ አቅራቢያ የሚገኝ፣ ፈጣን የመኖሪያ ቤቶች ግንባታ እየተካሄደበት ያለ ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሲቪል ሰርቪስ", "የኢፌድሪ ሲቪል ሰርቪስ ዩኒቨርሲቲ የሚገኝበትና ለአያት መንገድ ቅርብ የሆነ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሀያ አራት (24)", "በመገናኛና በኮተቤ መካከል የሚገኝ፣ ምቹ መኖሪያዎችና ትናንሽ ሱቆች ያሉት ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("አባዶ", "በከተማዋ ዳርቻ የሚገኝ ታላቅ የኮንዶሚኒየም ከተማ፣ በሺዎች የሚቆጠሩ ነዋሪዎች መኖሪያ::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("የካ አባዶ", "የየካ ክፍለ ከተማ አካል የሆነ፣ አዲስ የተቆረቆሩ ሰፊ የመኖሪያ መንደሮች መገኛ::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ካራንቡላ", "ወደ ሰንዳፋ መውጫ አካባቢ የሚገኝ፣ ለፀጥታና ንፁህ አየር ፈላጊዎች ተመራጭ መኖሪያ ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሰሚት", "ውብ ቪላዎችና ንፁህ አስፋልቶች ያሉት፣ መካከለኛና ከፍተኛ ገቢ ያላቸው ሰዎች መኖሪያ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ቡልቡላ", "በቦሌ ክፍለ ከተማ ስር የሚገኝ፣ በፈጣን ሁኔታ እያደገ የመጣ አዲስ የመኖሪያ መንደር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("አየር ጤና", "በምዕራብ አዲስ አበባ የሚገኝ፣ ሰፊ የመኖሪያ ቪላዎችና ንፁህ አየር ያለው ታዋቂ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("አለም ባንክ", "ከአየር ጤና ቀጥሎ የሚገኝ፣ እጅግ በጣም ሰፊ የሆነ የመኖሪያና የንግድ እንቅስቃሴ ያለበት ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ኮልፌ", "በባህላዊ አልባሳት ሽያጭና በሰፊ ህዝብ ቁጥር የምትታወቅ ጥንታዊ የመኖሪያና የንግድ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ካራቆሬ", "ወደ ጅማ መንገድ መውጫ ላይ የሚገኝ፣ የከተማዋ ማብቂያና ሰፊ የመኖሪያ ቀጠና::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ጀሞ 1", "በትላልቅ የኮንዶሚኒየም ህንፃዎችና በደማቅ የካፌና ሱቆች ንግድ የሚታወቅ የመኖሪያ መንደር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ጀሞ 2", "ከጀሞ 1 ቀጥሎ የለማ፣ ሰፊ አፓርታማዎችና ምቹ መኖሪያዎች ያሉት አዲስ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ጀሞ 3", "የጀሞ መንደሮች ማራዘሚያ፣ አዲስ ለተሰደዱ ነዋሪዎች ሰፊ የመኖሪያ እድል የፈጠረ አካባቢ::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ለቡ", "በዘመናዊ ዲዛይን የተገነቡ ቪላዎችና አፓርታማዎች ያሉት፣ ለኑሮ እጅግ ተመራጭ የሆነ ደቡባዊ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("መካኒሳ", "የውጭ ሀገር ዜጎችና ትላልቅ ትምህርት ቤቶች የሚገኙበት፣ ለኑሮ ምቹና ሰላማዊ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሳር ቤት መኖሪያ", "ከአፍሪካ አንድነት ጀርባ ያሉ ፀጥተኛና አረንጓዴ የሆኑ የመኖሪያ ቪላዎች መገኛ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች")
    ]
    
    for ስም, ታሪክ, ደረጃ, ምድብ in ዋና_ቦታዎች:
        ዲፎልት_ካርታ = f"https://maps.google.com/maps?q={ስም}+Addis+Ababa&output=embed"
        ጠቋሚ.execute("INSERT OR IGNORE INTO ቦታዎች (ስም, ታሪክ, ደረጃ, ምድብ, ካርታ) VALUES (?, ?, ?, ?, ?)", 
                       (ስም, ታሪክ, ደረጃ, ምድብ, ዲፎልት_ካርታ))
        
        if "ታሪካዊ" in ምድብ: ፎቶ_ናሙና = "https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3"
        elif "ንግድ" in ምድብ: ፎቶ_ናሙና = "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a"
        elif "ትራንስፖርት" in ምድብ: ፎቶ_ናሙና = "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957"
        else: ፎቶ_ናሙና = "https://images.unsplash.com/photo-1568605114967-8130f3a36994"
        
        for i in range(3):
            ልዩ_ሊንክ = f"{ፎቶ_ናሙና}?q=80&w=400&auto=format&fit=crop&place={ስም}&num={i}"
            ጠቋሚ.execute("INSERT OR IGNORE INTO ቦታ_ፎቶዎች (ፎቶ_ሊንክ, ቦታ_ስም) VALUES (?, ?)", (ልዩ_ሊንክ, ስም))
            
    ግንኙነት.commit()
    ግንኙነት.close()

HTML_ዲዛይን = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>አዲስ አበባ ከተማ ጋለሪ መመሪያ</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 650px; background: white; margin: 30px auto; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
        h1 { text-align: center; color: #111; }
        h2 { color: #2c3e50; border-bottom: 2px solid #eaeaea; padding-bottom: 8px; }
        .subtitle { text-align: center; color: #666; }
        label { font-weight: bold; display: block; margin-top: 15px; margin-bottom: 5px; }
        select, input, textarea { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; font-size: 16px; }
        .btn { background: linear-gradient(to right, #0072ff, #00c6ff); color: white; padding: 14px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 18px; font-weight: bold; }
        .result-box { background: #f9f9f9; border-left: 5px solid #0072ff; padding: 20px; margin-top: 25px; border-radius: 8px; }
        .gallery { display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }
        .gallery img { width: 31%; min-width: 120px; height: 110px; object-fit: cover; border-radius: 8px; }
        .alert { padding: 15px; background-color: #d4edda; color: #155724; border-radius: 8px; margin-top: 15px; text-align: center; }
        .header-icon { text-align: center; font-size: 50px; }
        body.dark-mode { background: #121212; color: #e0e0e0; }
        body.dark-mode .container { background: #1e1e1e; color: #e0e0e0; }
        body.dark-mode input, body.dark-mode select, body.dark-mode textarea { background: #2d2d2d; color: #ffffff; }
        .dark-toggle-btn { position: fixed; top: 15px; right: 15px; background: #333; color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; z-index: 1000; }
    </style>
</head>
<body>

    <button class="dark-toggle-btn" onclick="የሁነታ_መቀያየሪያ()">🌓 ጨለማ/ብርሃን</button>

    <div class="container">
        <div class="header-icon">🌆</div>
        <h1>አዲስ አበባን ይወቁ</h1>
        <p class="subtitle">የከተማዋን ሰፈሮች እና መገኛቸውን ያስሱ</p>

        <form method="POST" action="/">
            <input type="hidden" name="ፎርም_አይነት" value="ፈልግ">
            <label for="መፈለጊያ_ሳጥን">🔍 የሰፈር ስም እዚህ ይጻፉ...</label>
            <input type="text" id="መፈለጊያ_ሳጥን" onkeyup="ቦታ_ፈልግ()" placeholder="ለምሳሌ፡ ፒያሳ...">
            
            <label for="የቦታ_ዝርዝር">ሰፈር ይምረጡ፦</label>
            <select name="የተመረጠው_ቦታ" id="የቦታ_ዝርዝር" required>
                <option value="">እባክዎ ቦታ ይምረጡ...</option>
                {% for ምድብ, ቦታዎች in ምድቦች.items() %}
                    <optgroup label="{{ ምድብ }}">
                    {% for ቦታ in ቦታዎች %}
                        <option value="{{ ቦታ }}">{{ ቦታ }}</option>
                    {% endfor %}
                    </optgroup>
                {% endfor %}
            </select>
            <button type="submit" class="btn">🔍 መረጃ አምጣ</button>
        </form>

        {% if ውጤት %}
        <div class="result-box">
            <h3>📍 {{ ውጤት[0] }}</h3>
            <p><strong>ታሪክና መረጃ፦</strong> {{ ውጤት[1] }}</p>
            <p><strong>የደረጃ አሰጣጥ፦</strong> ⭐ {{ ውጤት[2] }}</p>
            
            <p><strong>🗺️ የሰፈሩ ቀጥታ ካርታ (Google Maps)፦</strong></p>
            <div style="width: 100%; overflow: hidden; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 15px;">
                <iframe width="100%" height="300" style="border:0;" loading="lazy" allowfullscreen src="https://maps.google.com/maps?q={{ ውጤት[0] | urlencode }}+Addis+Ababa&t=&z=14&ie=UTF8&iwloc=&output=embed"></iframe>
            </div>
            
            <h4>📸 የቦታው ፎቶዎች፦</h4>
            <div class="gallery">
                {% for ፎቶ in ውጤት[5] %}
                    <img src="{{ ፎቶ }}" alt="የሰፈር ፎቶ">
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>

    <div class="container" style="border-top: 5px solid #0072ff;">
        <h2>➕ አዲስ ቦታ መመዝገቢያ</h2>
        <form method="POST" action="/">
            <input type="hidden" name="ፎርም_አይነት" value="መዝግብ">
            <label>የሰፈሩ ስም፦</label>
            <input type="text" name="አዲስ_ስም" required>
            <label>ስለ ሰፈሩ ታሪክ፦</label>
            <textarea name="አዲስ_ታሪክ" rows="3" required></textarea>
            <label>ደረጃ፦</label>
            <select name="አዲስ_ደረጃ">
                <option value="5 ኮከብ">⭐⭐⭐⭐⭐</option>
                <option value="4 ኮከብ">⭐⭐⭐⭐</option>
            </select>
            <label>ምድብ፦</label>
            <select name="አዲስ_ምድብ">
                <option value="🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች">🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች</option>
                <option value="🛒 የንግድ ማዕከላት እና ገበያ">🛒 የንግድ ማዕከላት እና ገበያ</option>
                <option value="🚌 የትራንስፖርት መናኸሪያዎች">🚌 የትራንስፖርት መናኸሪያዎች</option>
                <option value="🏡 መኖሪያ እና ሌሎች ሰፈሮች">🏡 መኖሪያ እና ሌሎች ሰፈሮች</option>
            </select>
            <label>ሚስጥር ቁጥር፦</label>
            <input type="password" name="ሚስጥር_ቁጥር" required>
            <button type="submit" class="btn" style="background:#0072ff;">💾 አዲስ ቦታ መዝግብ</button>
        </form>
        {% if መልዕክት %}
            <div class="alert">{{ መልዕክት }}</div>
        {% endif %}
    </div>

    <script>
        function ቦታ_ፈልግ() {
            var ፊደል = document.getElementById("መፈለጊያ_ሳጥን").value.trim().toLowerCase();
            var ዝርዝር = document.getElementById("የቦታ_ዝርዝር");
            var አማራጮች = ዝርዝር.getElementsByTagName("option");
            for (var i = 0; i < አማራጮች.length; i++) {
                if (አማራጮች[i].text.toLowerCase().indexOf(ፊደል) > -1) { አማራጮች[i].style.display = ""; } 
                else { አማራጮች[i].style.display = "none"; }
            }
        }
        function የሁነታ_መቀያየሪያ() {
            document.body.classList.toggle("dark-mode");
        }
    </script>
</body>
</html>
"""

def የቦታ_ስሞችን_በምድብ_አምጣ():
    ግንኙነት = sqlite3.connect(DATABASE_NAME)
    ጠቋሚ = ግንኙነት.cursor()
    try:
        ጠቋሚ.execute("SELECT ምድብ, ስም FROM ቦታዎች ORDER BY ምድብ, ስም ASC")
        ውጤቶች = ጠቋሚ.fetchall()
    except:
        ውጤቶች = []
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
                ግንኙነት = sqlite3.connect(DATABASE_NAME)
                ጠቋሚ = ግንኙነት.cursor()
                ጠቋሚ.execute("SELECT ስም, ታሪክ, ደረጃ, ምድብ, ካርታ FROM ቦታዎች WHERE ስም=?", (የተመረጠው_ቦታ,))
                ቦታ_መረጃ = ጠቋሚ.fetchone()
                
                ጠቋሚ.execute("SELECT ፎቶ_ሊንክ FROM ቦታ_ፎቶዎች WHERE ቦታ_ስም=?", (የተመረጠው_ቦታ,))
                ፎቶዎች_ኳየሪ = ጠቋሚ.fetchall()
                የፎቶ_ሊንኮች = [ፎቶ[0] for ፎቶ in ፎቶዎች_ኳየሪ]
                ግንኙነት.close()
                
                if ቦታ_መረጃ:
                    ውጤት = (ቦታ_መረጃ[0], ቦታ_መረጃ[1], ቦታ_መረጃ[2], ቦታ_መረጃ[3], ቦታ_መረጃ[4], የፎቶ_ሊንኮች)
                
        elif ፎርም_አይነት == 'መዝግብ':
            ስም = request.form.get('አዲስ_ስም', '').strip()
            ታሪክ = request.form.get('አዲስ_ታሪክ', '').strip()
            ደረጃ = request.form.get('አዲስ_ደረጃ')
            ምድብ = request.form.get('አዲስ_ምድብ')
            የገባው_ፓስወርድ = request.form.get('ሚስጥር_ቁጥር', '').strip()
            
            if የገባው_ፓስወርድ != "777":
                መልዕክት = "⚠️ የይለፍ ቃሉ የተሳሳተ ነው!"
            else:
                ዲፎልት_ካርታ = f"https://maps.google.com/maps?q={ስም}+Addis+Ababa&output=embed"
                ግንኙነት = sqlite3.connect(DATABASE_NAME)
                ጠቋሚ = ግንኙነት.cursor()
                ጠቋሚ.execute("INSERT OR REPLACE INTO ቦታዎች (ስም, ታሪክ, ደረጃ, ምድብ, ካርታ) VALUES (?, ?, ?, ?, ?)", (ስም, ታሪክ, ደረጃ, ምድብ, ዲፎልት_ካርታ))
                ግንኙነት.commit()
                ግንኙነት.close()
                መልዕክት = f"🎉 '{ስም}' በተሳካ ሁኔታ ተመዝግቧል!"

    ምድቦች = የቦታ_ስሞችን_በምድብ_አምጣ()
    return render_template_string(HTML_DIዛይን=HTML_ዲዛይን, ምድቦች=ምድቦች, ውጤት=ውጤት, መልዕክት=መልዕክት)

if __name__ == '__main__':
    # 💥 ሰርቨሩ ሲነሳ ያለምንም ቅድመ ሁኔታ ዳታቤዙን ሁልጊዜ ቀጥታ ይጭናል!
    ዳታቤዙን_አዘምን()
        
    ፖርት = int(os.environ.get("PORT", 5000))
    አፕ.run(host='0.0.0.0', port=ፖርት)

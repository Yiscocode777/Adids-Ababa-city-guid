from flask import Flask, request, render_template_string
import sqlite3

def ዳታቤዙን_አዘምን():
    # ስሙን ወደ 'ከተማ_መረጃ_አዲስ.db' ቀይረነዋል - ይህ የድሮውን ስህተት ያጠፋዋል!
    ግንኙነት = sqlite3.connect("ከተማ_መረጃ_አዲስ.db")
    ጠቋሚ = ግንኙነት.cursor()
    
    # 1. ጠረጴዛው ከሌለ መፍጠር
    ጠቋሚ.execute("""
        CREATE TABLE IF NOT EXISTS ቦታዎች (
            ስም TEXT PRIMARY KEY,
            ታሪክ TEXT,
            ደረጃ TEXT,
            ምድብ TEXT DEFAULT '🏡 መኖሪያ እና ሌሎች ሰፈሮች',
            ካርታ TEXT
        )
    """)
    ግንኙነት.commit()
    
    # 🌟 2. 60 የአዲስ አበባ ዋና ዋና ሰፈሮች ዝርዝር (ሙሉ በሙሉ በአማርኛ የተስተካከለ)
    ዋና_ቦታዎች = [
        # 🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች
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
        ("ሳይንስ ሙዚየም", "በቅርቡ የተገነባ፣ ሳይንስና ቴክኖሎጂን ለህዝብ የሚያሳይ ዘመናዊና ማራኪ የስነ-ህንፃ ጥበብ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),
        ("መስቀል አደባባይ", "የመስቀል ደመራ፣ ታላላቅ ህዝባዊ ስብሰባዎችና ስፖርታዊ እንቅስቃሴዎች የሚደረጉበት የከተማዋ ዋና አደባባይ::", "5 ኮከብ", "🏛 ታሪካዊ እና የመዝናኛ ስፍራዎች"),

        # 🛒 የንግድ ማዕከላት እና ገበያ
        ("መርካቶ", "የአፍሪካ ትልቁና ታዋቂው የውጭ ክፍት የገበያ ቦታ፣ ሁሉንም አይነት የንግድ ዕቃዎች መገኛ::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቦሌ", "ዘመናዊ የገበያ ማዕከላት፣ ታዋቂ ሆቴሎች፣ ካፌዎችና የባንክ ዋና መሥሪያ ቤቶች መገኛ ዘመናዊ ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሀያ ሁለት (22)", "ደማቅ የምሽት ህይወት፣ ዘመናዊ ህንፃዎችና የንግድ ሱቆች የበዙበት የቦሌ አዋሳኝ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቦሌ መድኃኔዓለም", "የመድኃኔዓለም ቤተክርስቲያን፣ ትላልቅ ሞሎች (Malls) እና ሲኒማ ቤቶች የሚገኙበት የንግድ ማኸከል::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("አትላስ", "በባህላዊና ዘመናዊ ምግብ ቤቶች፣ በከፍተኛ ሆቴሎችና በንግድ እንቅስቃሴ የምትታወቅ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ኦሎምፒያ", "ትላልቅ ቢሮዎችና የውጭ ድርጅቶች መቀመጫ የሆነች፣ በቦሌ መንገድ ላይ የምትገኝ የንግድ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("መገናኛ", "የከተማዋ ትልቁ የትራፊክና የንግድ መገናኛ፣ የገበያ አዳራሾችና የቢሮ ህንፃዎች መዓት የሞሉበት ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ገርጂ", "ሰፊ የመኖሪያ መንደሮች ያሉትና ፈጣን የንግድና የህንፃ ግንባታ የታየበት ታዋቂ አካባቢ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሲኤምሲ (CMC)", "ከፍተኛ ገቢ ያላቸው ነዋሪዎች የሚኖሩበት ዘመናዊ ቪላዎችና የንግድ ሱቆች ያሉበት ቪአይፒ ሰፈር::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("साሪስ", "በፋብሪካዎችና በጅምላ ንግድ መጋዘኖች የምትታወቅ፣ ወደ ደቡብ መውጫ ያለች የንግድ ቀጠና::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ቃሊቲ", "የትላልቅ ኢንዱስትሪዎች፣ የጉምሩክ መጋዘኖችና የጭነት መኪናዎች ማረፊያ የሆነች የንግድ ከተማ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ጎተራ", "በትላልቅ ዘመናዊ ኮንዶሚኒየሞችና በኢንተርክንቲኔንታል የልውውጥ ድልድይ የምትታወቅ የንግድ መገናኛ::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ላፍቶ", "ለኢንዱስትሪና ለመኖሪያ ምቹ የሆነች፣ የገበያ ማዕከላትና መዝናኛዎች ያሏት ደቡብ ምዕራብ ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሳር ቤት", "የአፍሪካ አንድነት ድርጅት (AU) አቅራቢያ የምትገኝ፣ የፈረስ ማጋለጫ ሜዳና የባንኮች መጋዘን ያለባት ሰፈር::", "4 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),
        ("ሜክሲኮ", "የንግድ ማዕከላት፣ የፌደራል ፖሊስ ዋና መሥሪያ ቤትና ትላልቅ ኮሌጆች የሚገኙበት የንግድ እምብርት::", "5 ኮከብ", "🛒 የንግድ ማዕከላት እና ገበያ"),

        # 🚌 የትራንስፖርት መናኸሪያዎች
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

        # 🏡 መኖሪያ እና ሌሎች ሰፈሮች
        ("አያት", "ሰፊና ፀጥተኛ የመኖሪያ መንደሮች፣ ቪላዎችና ዘመናዊ አፓርታማዎች የበዙባት የምስራቋ ውብ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ኮተቤ", "የአዲስ አበባ ዩኒቨርሲቲ ኮተቤ ካምፓስ የሚገኝበት፣ ሰፊ የመኖሪያና የትምህርት ቀጠና ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ካራሎ", "በኮተቤ አቅራቢያ የሚገኝ፣ ፈጣን የመኖሪያ ቤቶች ግንባታ እየተካሄደበት ያለ ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሲቪል ሰርቪስ", "የኢፌድሪ ሲቪል ሰርቪስ ዩኒቨርሲቲ የሚገኝበትና ለአያት መንገድ ቅርብ የሆነ ሰፈር::", "4 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሀያ አራት (24)", "በመገናኛና በኮተቤ መካከል የሚገኝ፣ ምቹ መኖሪያዎችና ትናንሽ ሱቆች ያሉት ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("አባዶ", "በከተማዋ ዳርቻ የሚገኝ ታላቅ የኮንዶሚኒየም ከተማ፣ በሺዎች የሚቆጠሩ ነዋሪዎች መኖሪያ::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("የካ አባዶ", "የየካ ክፍለ ከተማ አካል የሆነ፣ አዲስ የተቆረቆሩ ሰፊ የመኖሪያ መንደሮች መገኛ::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ካራንቡላ", "ወደ ሰንዳፋ መውጫ አካባቢ የሚገኝ፣ ለፀጥታና ንፁህ አየር ፈላጊዎች ተመራጭ መኖሪያ ሰፈር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("ሰሚት", "ውብ ቪላዎችና ንፁህ አስፋልቶች ያሉት፣ መካከለኛና ከፍተኛ ገቢ ያላቸው ሰዎች መኖሪያ ሰፈር::", "5 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
        ("बुልቡላ", "በቦሌ ክፍለ ከተማ ስር የሚገኝ፣ በፈጣን ሁኔታ እያደገ የመጣ አዲስ የመኖሪያ መንደር::", "3 ኮከብ", "🏡 መኖሪያ እና ሌሎች ሰፈሮች"),
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
        ዲፎልት_ካርታ = f"http://maps.google.com/?q={ስም}+Addis+Ababa"
        # እዚህ ጋር በትክክል 'ካርታ' በሚለው አማርኛ ተተክቷል!
        ጠቋሚ.execute("INSERT OR IGNORE INTO ቦታዎች (ስም, ታሪክ, ደረጃ, ምድብ, ካርታ) VALUES (?, ?, ?, ?, ?)", 
                       (ስም, ታሪክ, ደረጃ, ምድብ, ዲፎልት_ካርታ))
        
    ግንኙነት.commit()
    ግንኙነት.close()

# ዳታቤዙን በአዲስ ስም በንጽህና ማስነሳት
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
            font-family: 'Noto Sans Ethiopic', sans-serif; margin: 0; min-height: 100vh; 
            background: linear-gradient(rgba(15, 32, 67, 0.7), rgba(15, 32, 67, 0.85)), url('https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3?q=80&w=1200&auto=format&fit=crop') no-repeat center center fixed;
            background-size: cover; display: flex; flex-direction: column; align-items: center; padding: 30px 20px;
        }
        .container { 
            background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2); padding: 40px 30px; border-radius: 24px; 
            box-shadow: 0px 20px 40px rgba(0,0,0,0.4); width: 100%; max-width: 460px; text-align: center; box-sizing: border-box; margin-bottom: 35px; color: #ffffff;
        }
        .header-icon { font-size: 55px; margin-bottom: 5px; }
        h2 { color: #ffffff; font-size: 28px; margin-bottom: 8px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        p.subtitle { color: #e0e0e0; font-size: 15px; margin-bottom: 30px; }
        input[type="text"], textarea, select { 
            font-size: 16px; padding: 14px 18px; width: 100%; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 18px;
            box-sizing: border-box; font-family: inherit; outline: none; background: rgba(255, 255, 255, 0.9); color: #2c3e50;
        }
        .btn { 
            background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; padding: 16px; border: none; border-radius: 14px; cursor: pointer; font-size: 18px; font-weight: bold; width: 100%; box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4);
        }
        .btn-admin { background: linear-gradient(45deg, #11998e, #38ef7d); box-shadow: 0 6px 20px rgba(56, 239, 125, 0.3); }
        .result { margin-top: 30px; text-align: left; padding: 25px; border-left: 6px solid #00f2fe; background: rgba(15, 32, 67, 0.6); border-radius: 16px; }
        .result h3 { margin-top: 0; color: #00f2fe; font-size: 22px; }
        .badge { display: inline-block; background: #f1c40f; color: #2c3e50; padding: 6px 14px; border-radius: 20px; font-weight: bold; }
        .category-badge { display: inline-block; background: rgba(0, 242, 254, 0.2); color: #00f2fe; border: 1px solid #00f2fe; padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; }
        .maps-btn { display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #ea4335, #ff6b6b); color: white; text-decoration: none; padding: 12px 20px; border-radius: 10px; margin-top: 15px; font-weight: bold;}
        .alert { padding: 15px; border-radius: 14px; margin-top: 20px; font-weight: bold; text-align: center; background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
        optgroup { font-weight: bold; color: #1e3c72; background-color: #f0f4f8;}
        option { color: #333; background-color: #fff;}
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
                    <optgroup label="{{ ምድብ }}">
                        {% for ስም in ስሞች %}
                            <option value="{{ ስም }}">{{ ስም }}</option>
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
            <textarea name="አዲስ_ታሪክ" placeholder="የሰፈሩ ታሪክ..." rows="3" required></textarea>
            <select name="አዲስ_ደረጃ" required>
                <option value="" disabled selected>ደረጃ...</option>
                <option value="5 ኮከብ">⭐⭐⭐⭐⭐</option>
                <option value="4 ኮከብ">⭐⭐⭐⭐</option>
                <option value="3 ኮከብ">⭐⭐⭐</option>
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
            <div class="alert">🎉 {{ መልዕክት }}</div>
        {% endif %}
    </div>

    <script>
        function ቦታ_ፈልግ() {
            var ፊደል = document.getElementById("መፈለጊያ_ሳጥን").value.trim();
            var ዝርዝር = document.getElementById("የቦታ_ዝርዝር");
            var አማራጮች = ዝርዝር.getElementsByTagName("option");
            for (var i = 0; i < አማራጮች.length; i++) {
                if (አማራጮች[i].text.indexOf(ፊደል) > -1) { አማራጮች[i].style.display = ""; } 
                else { አማራጮች[i].style.display = "none"; }
            }
        }
    </script>
</body>
</html>
"""

def የቦታ_ስሞችን_በምድብ_አምጣ():
    ግንኙነት = sqlite3.connect("ከተማ_መረጃ_አዲስ.db")
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
                ግንኙነት = sqlite3.connect("ከተማ_መረጃ_አዲስ.db")
                ጠቋሚ = ግንኙነት.cursor()
                ጠቋሚ.execute("SELECT ስም, ታሪክ, ደረጃ, ምድብ, ካርታ FROM ቦታዎች WHERE ስም=?", (የተመረጠው_ቦታ,))
                ውጤት = ጠቋሚ.fetchone()
                ግንኙነት.close()
        elif ፎርም_አይነት == 'መዝግብ':
            ስም = request.form.get('አዲስ_ስም')
            ታሪክ = request.form.get('አዲስ_ታሪክ')
            ደረጃ = request.form.get('አዲስ_ደረጃ')
            ምድብ = request.form.get('አዲስ_ምድብ')
            디ፎልት_ካርታ = f"http://maps.google.com/?q={ስም}+Addis+Ababa"
            
            ግንኙነት = sqlite3.connect("ከተማ_መረጃ_አዲስ.db")
            ጠቋሚ = ግንኙነት.cursor()
            ጠቋሚ.execute("INSERT OR REPLACE INTO ቦታዎች (ስም, ታሪክ, ደረጃ, ምድብ, ካርታ) VALUES (?, ?, ?, ?, ?)", (ስም, ታሪክ, ደረጃ, ምድብ, ዲፎልት_ካርታ))
            ግንኙነት.commit()
            ግንኙነት.close()
            መልዕክት = f"'{ስም}' በተሳካ ሁኔታ በዳታቤዝ ውስጥ ተመዝግቧል!"

    ምድቦች = የቦታ_ስሞችን_በምድብ_አምጣ()
    return render_template_string(HTML_ዲዛይን, ምድቦች=ምድቦች, ውጤት=ውጤት, መልዕክት=መልዕክት)

if __name__ == '__main__':
    import os
    ፖርት = int(os.environ.get("PORT", 5000))
    አፕ.run(host='0.0.0.0', port=ፖርት)

# -*- coding: utf-8 -*-
"""Generate Arabic client reference guide for Zahar theme sections."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_sections():
    results = []
    sections_dir = ROOT / "sections"
    for schema_path in sorted(sections_dir.glob("*.schema.json")):
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        name = data.get("name", {})
        name_ar = name.get("ar") if isinstance(name, dict) else str(name)
        name_en = name.get("en") if isinstance(name, dict) else ""
        images = []
        settings_summary = []

        def walk(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "image":
                    label = obj.get("label")
                    info = obj.get("info")
                    images.append(
                        {
                            "id": obj.get("id"),
                            "label": label.get("ar") if isinstance(label, dict) else label,
                            "info": info.get("ar") if isinstance(info, dict) else info,
                        }
                    )
                if "type" in obj and "id" in obj:
                    label = obj.get("label")
                    info = obj.get("info")
                    settings_summary.append(
                        {
                            "id": obj.get("id"),
                            "type": obj.get("type"),
                            "label": label.get("ar") if isinstance(label, dict) else label,
                            "info": info.get("ar") if isinstance(info, dict) else info,
                            "default": obj.get("default"),
                        }
                    )
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for i in obj:
                    walk(i)

        walk(data)
        base = schema_path.name.replace(".schema.json", ".jinja")
        results.append(
            {
                "file": schema_path.name,
                "jinja": base,
                "name_ar": name_ar,
                "name_en": name_en,
                "images": images,
                "settings_count": len(settings_summary),
                "settings": settings_summary,
            }
        )
    return results


DATA = extract_sections()

# Manual enrichments: descriptions + recommended sizes when schema lacks info
ENRICH = {
    "main-slider.schema.json": {
        "desc": "السلايدر الرئيسي في أعلى الصفحة الرئيسية. أول انطباع للزائر — استخدم صور عالية الجودة ورسائل واضحة.",
        "tips": [
            "يفضّل صورتان: واحدة للجوال وأخرى سطح المكتب لجودة أفضل.",
            "تجنّب النصوص الصغيرة داخل الصورة؛ اكتب العناوين من إعدادات الثيم.",
            "الصور الثقيلة تبطئ المتجر — احفظ JPEG بجودة 80–85٪.",
        ],
        "sizes": [
            {"label": "صورة الجوال / الافتراضية", "size": "1400 × 600"},
            {"label": "صورة سطح المكتب (اختياري)", "size": "1920 × 800"},
        ],
        "category": "hero",
    },
    "ticker.schema.json": {
        "desc": "شريط متحرك يعرض عروضاً أو رسائل ترويجية بشكل مستمر أعلى أو داخل الصفحة.",
        "tips": ["اجعل النص قصيراً وواضحاً.", "استخدم ألواناً متوافقة مع هوية المتجر."],
        "sizes": [],
        "category": "promo",
    },
    "features-section.schema.json": {
        "desc": "عرض مميزات المتجر أو الخدمات (أيقونات + عناوين) لتعزيز الثقة.",
        "tips": ["استخدم أيقونات بخلفية شفافة PNG.", "يفضّل 3–6 عناصر فقط."],
        "sizes": [{"label": "أيقونة الميزة", "size": "200 × 200"}],
        "category": "content",
    },
    "partners.schema.json": {
        "desc": "شعارات الشركاء أو العلامات التي يعمل معها المتجر.",
        "tips": ["وحّد ارتفاع الشعارات قدر الإمكان.", "خلفية شفافة تعطي مظهراً أنظف."],
        "sizes": [{"label": "شعار الشريك", "size": "200 × 200"}],
        "category": "content",
    },
    "category-section.schema.json": {
        "desc": "سلايدر لعرض تصنيفات المتجر مع ربط مباشر بصفحات التصنيف.",
        "tips": ["اختر تصنيفات لها صور واضحة من لوحة سلة.", "لا تكثر التصنيفات المعروضة دفعة واحدة."],
        "sizes": [{"label": "صورة التصنيف (مستخرجة من التصنيف)", "size": "حوالي 400 × 400"}],
        "category": "catalog",
    },
    "category-products-section.schema.json": {
        "desc": "بطاقات فئات بصور مخصصة وعناوين وروابط — مثالية لتقسيم الأقسام الرئيسية.",
        "tips": ["التزم بالمقاس الموحّد حتى لا تختلف ارتفاعات البطاقات."],
        "sizes": [{"label": "صورة الفئة", "size": "480 × 170"}],
        "category": "catalog",
    },
    "collection-section.schema.json": {
        "desc": "مجموعات متنوعة بتابات: صورة كمبيوتر/موبايل مع منتج مرتبط.",
        "tips": ["جهّز نسختين من الصورة (ديسكتوب وموبايل).", "اختر منتجاً بارزاً لكل مجموعة."],
        "sizes": [
            {"label": "صورة الكمبيوتر", "size": "حوالي 600 × عرض مناسب"},
            {"label": "صورة الموبايل", "size": "حوالي 400 عرض"},
        ],
        "category": "catalog",
    },
    "diffrent-collction.schema.json": {
        "desc": "سكشن لاكتشاف مجموعة مميزة مع صور وعناوين وروابط وعدادات اختيارية.",
        "tips": ["مناسب لأبرز المجموعات أو الحملات الموسمية."],
        "sizes": [{"label": "صورة العنصر", "size": "مربّع أو 1:1 مفضّل"}],
        "category": "catalog",
    },
    "exploere-collections.schema.json": {
        "desc": "استكشاف المجموعات بصورة وعنوان ورابط لكل عنصر.",
        "tips": ["استخدم صوراً متناسقة في النسبة."],
        "sizes": [{"label": "صورة المجموعة", "size": "مربّع أو عرضي حسب التصميم"}],
        "category": "catalog",
    },
    "products-section.schema.json": {
        "desc": "عرض منتجات من تصنيفات أو قوائم محددة مع خيارات تخطيط وألوان.",
        "tips": ["تأكد أن صور المنتجات موحّدة المقاس في لوحة سلة.", "لا تعرض عدداً كبيراً جداً دفعة واحدة."],
        "sizes": [{"label": "صور المنتجات", "size": "حسب إعدادات بطاقة المنتج في المتجر"}],
        "category": "products",
    },
    "products-tabs-section.schema.json": {
        "desc": "منتجات مقسّمة على تابات (الأكثر مبيعاً، جديد، عروض…).",
        "tips": ["سمِّ التابات بأسماء واضحة للعميل."],
        "sizes": [],
        "category": "products",
    },
    "products-showcase-slider.schema.json": {
        "desc": "سلايدر إبراز منتجات مختارة بشكل بصري قوي.",
        "tips": ["اختر منتجات ذات صور احترافية."],
        "sizes": [],
        "category": "products",
    },
    "promo-samples-banner.schema.json": {
        "desc": "بنر ترويجي لعينات أو عروض خاصة مع صورة ونصوص وألوان قابلة للتخصيص.",
        "tips": ["اجعل الرسالة مختصرة وزر الدعوة واضحاً."],
        "sizes": [{"label": "صورة البنر", "size": "راجع معاينة السكشن بعد الرفع"}],
        "category": "promo",
    },
    "image-tabs-slider.schema.json": {
        "desc": "سلايدر صور مع تابات للتنقل بين محتويات مختلفة.",
        "tips": ["وحّد مقاسات الصور داخل نفس السكشن."],
        "sizes": [],
        "category": "media",
    },
    "ggallery.schema.json": {
        "desc": "معرض صور مربّع لعرض منتجات، لحظات، أو ستايل المتجر.",
        "tips": ["المقاس المربّع يضمن تناسق الشبكة."],
        "sizes": [{"label": "صورة المعرض", "size": "750 × 750"}],
        "category": "media",
    },
    "video.schema.json": {
        "desc": "سكشن فيديو لعرض المنتج أو القصة أو حملة إعلانية.",
        "tips": ["استخدم MP4 مضغوط.", "الحد الأقصى الموصى به: 10MB."],
        "sizes": [{"label": "ملف الفيديو", "size": "MP4 — أقصى 10MB"}],
        "category": "media",
    },
    "reels-section.schema.json": {
        "desc": "عرض ريلز / فيديوهات قصيرة بأسلوب عمودي يشبه السوشيال ميديا.",
        "tips": ["النسبة العمودية (9:16) هي الأنسب.", "اجعل مدة الفيديو قصيرة."],
        "sizes": [{"label": "فيديو الريل", "size": "يفضّل 1080 × 1920 (9:16)"}],
        "category": "media",
    },
    "before-after-section.schema.json": {
        "desc": "مقارنة قبل وبعد بسحّاب تفاعلي — مثالي لمستحضرات، تنظيف، تجميل، ترميم.",
        "tips": ["صوّر من نفس الزاوية والإضاءة.", "تأكد أن المقاسين متطابقان."],
        "sizes": [
            {"label": "صورة قبل", "size": "1200 × 500"},
            {"label": "صورة بعد", "size": "1200 × 500"},
        ],
        "category": "media",
    },
    "testimonials.schema.json": {
        "desc": "آراء وتجارب العملاء لبناء الثقة الاجتماعية.",
        "tips": ["استخدم أسماء حقيقية إن أمكن.", "آراء قصيرة أوضح من نصوص طويلة."],
        "sizes": [{"label": "صورة العميل (إن وُجدت)", "size": "مربّع صغير ~150 × 150"}],
        "category": "social",
    },
    "why_choose_us.schema.json": {
        "desc": "لماذا تختارنا — نقاط قوة المتجر مع أيقونات ونصوص.",
        "tips": ["ركز على فوائد العميل لا ميزات تقنية."],
        "sizes": [],
        "category": "content",
    },
    "faq-section.schema.json": {
        "desc": "أسئلة شائعة قابلة للطي لتقليل استفسارات الدعم وزيادة التحويل.",
        "tips": ["أجب باختصار.", "ضع أكثر الأسئلة تكراراً في الأعلى."],
        "sizes": [],
        "category": "content",
    },
    "blog-section.schema.json": {
        "desc": "عرض مقالات المدونة (سلايدر أو شبكة) مع صورة وملخص ورابط.",
        "tips": ["صورة المقال موحّدة المقاس تظهر أجمل في الشبكة."],
        "sizes": [{"label": "صورة المقال", "size": "حوالي 600 عرض (نسبة 16:9 أو 4:3)"}],
        "category": "content",
    },
}

CATEGORY_LABELS = {
    "hero": "الواجهة الرئيسية",
    "promo": "العروض والترويج",
    "catalog": "التصنيفات والمجموعات",
    "products": "المنتجات",
    "media": "الوسائط والمعارض",
    "social": "آراء العملاء",
    "content": "المحتوى والثقة",
    "other": "أخرى",
}

TYPE_AR = {
    "text": "نص",
    "textarea": "نص طويل",
    "image": "صورة",
    "url": "رابط",
    "color": "لون",
    "checkbox": "تفعيل/إيقاف",
    "select": "قائمة اختيار",
    "number": "رقم",
    "list": "قائمة عناصر",
    "product": "منتج",
    "category": "تصنيف",
    "products": "منتجات",
    "video": "فيديو",
    "richtext": "نص منسّق",
    "font": "خط",
    "range": "شريط قيمة",
}

HEADER_SIZES = [
    {"label": "شعار الديسكتوب", "size": "180 × 90"},
    {"label": "شعار الجوال", "size": "180 × 90"},
]

LAYOUT_HIGHLIGHTS = [
    {"title": "الخطوط العربية", "text": "اختيار خط المتجر من مجموعة خطوط عربية جاهزة (Changa، Cairo، Tajawal، وغيرها)."},
    {"title": "ألوان الهوية", "text": "الألوان الأساسية تؤخذ من إعدادات العلامة في سلة وتتناسق مع عناصر الثيم."},
    {"title": "صورة الدفع الآمن", "text": "مقاس مقترح 150 × 150 أو حسب موضع الفوتر."},
    {"title": "أيقونات التواصل", "text": "مقاس مقترح حوالي 200 × 200 للأيقونات المخصصة."},
]


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\u0600-\u06FF\-]+", "-", name.strip(), flags=re.UNICODE)
    return s.strip("-") or "section"


def sizes_for(sec: dict) -> list:
    enrich = ENRICH.get(sec["file"], {})
    if enrich.get("sizes"):
        return enrich["sizes"]
    out = []
    for img in sec.get("images") or []:
        info = img.get("info") or ""
        m = re.search(r"(\d+)\s*[*×x]\s*(\d+)", info)
        if m:
            out.append({"label": img.get("label") or "صورة", "size": f"{m.group(1)} × {m.group(2)}"})
        elif "480" in (info or "") and "170" in (info or ""):
            out.append({"label": img.get("label") or "صورة", "size": "480 × 170"})
        elif info:
            out.append({"label": img.get("label") or "صورة", "size": info})
    return out


def escape(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_sections_html():
    cards = []
    details = []
    for i, sec in enumerate(DATA, 1):
        enrich = ENRICH.get(sec["file"], {})
        name = (sec.get("name_ar") or sec.get("name_en") or sec["file"]).strip()
        sid = f"sec-{i}-{slugify(sec['file'].replace('.schema.json', ''))}"
        cat = enrich.get("category", "other")
        desc = enrich.get("desc", "سكشن قابل للتخصيص من محرر الثيم في سلة.")
        tips = enrich.get("tips") or []
        sizes = sizes_for(sec)
        settings = sec.get("settings") or []

        size_badges = "".join(
            f'<span class="badge">{escape(s["label"])}: <strong>{escape(s["size"])}</strong></span>'
            for s in sizes
        ) or '<span class="badge muted">لا يتطلب صوراً بمقاس ثابت</span>'

        cards.append(
            f"""
            <a class="sec-card" href="#{sid}" data-cat="{cat}">
              <span class="sec-num">{i:02d}</span>
              <h3>{escape(name)}</h3>
              <p>{escape(desc[:110])}{'…' if len(desc) > 110 else ''}</p>
              <div class="sec-meta">
                <span>{len(settings)} إعداد</span>
                <span>{CATEGORY_LABELS.get(cat, cat)}</span>
              </div>
            </a>"""
        )

        tips_html = ""
        if tips:
            tips_html = "<ul class='tips'>" + "".join(f"<li>{escape(t)}</li>" for t in tips) + "</ul>"

        sizes_html = ""
        if sizes:
            rows = "".join(
                f"<tr><td>{escape(s['label'])}</td><td><code>{escape(s['size'])}</code></td></tr>"
                for s in sizes
            )
            sizes_html = f"""
            <div class="panel">
              <h4>المقاسات الموصى بها</h4>
              <table><thead><tr><th>العنصر</th><th>المقاس</th></tr></thead><tbody>{rows}</tbody></table>
            </div>"""
        else:
            sizes_html = """
            <div class="panel">
              <h4>المقاسات الموصى بها</h4>
              <p class="empty">هذا السكشن يعتمد على نصوص/ألوان أو صور منتجات من سلة — لا يوجد مقاس صورة ثابت إلزامي.</p>
            </div>"""

        # dedupe settings by id+label for display
        seen = set()
        set_rows = []
        for st in settings:
            key = (st.get("id"), st.get("label"), st.get("type"))
            if key in seen:
                continue
            seen.add(key)
            typ = TYPE_AR.get(st.get("type") or "", st.get("type") or "—")
            info = st.get("info") or "—"
            default = st.get("default")
            default_s = "—" if default is None else escape(default)
            set_rows.append(
                f"<tr><td>{escape(st.get('label') or st.get('id'))}</td>"
                f"<td><span class='type'>{escape(typ)}</span></td>"
                f"<td>{escape(info)}</td>"
                f"<td><code>{default_s}</code></td></tr>"
            )

        details.append(
            f"""
            <article class="detail" id="{sid}" data-cat="{cat}">
              <header class="detail-head">
                <div>
                  <span class="cat-pill">{escape(CATEGORY_LABELS.get(cat, cat))}</span>
                  <h2>{escape(name)}</h2>
                  <p class="lead">{escape(desc)}</p>
                  <div class="badges">{size_badges}</div>
                </div>
                <div class="file-box">
                  <span>ملف السكشن</span>
                  <code>{escape(sec.get('jinja') or '')}</code>
                </div>
              </header>
              {sizes_html}
              <div class="panel">
                <h4>نصائح للتجّار</h4>
                {tips_html if tips_html else '<p class="empty">استخدم إعدادات السكشن من محرر الثيم وعاين على الجوال قبل النشر.</p>'}
              </div>
              <div class="panel">
                <h4>جدول الإعدادات المرجعي ({len(set_rows)})</h4>
                <div class="table-wrap">
                  <table>
                    <thead><tr><th>الإعداد</th><th>النوع</th><th>ملاحظة / مقاس</th><th>افتراضي</th></tr></thead>
                    <tbody>{''.join(set_rows)}</tbody>
                  </table>
                </div>
              </div>
              <a class="back-top" href="#sections">↑ العودة لقائمة السكاشن</a>
            </article>"""
        )

    return "\n".join(cards), "\n".join(details)


CARDS, DETAILS = build_sections_html()

FILTERS = "".join(
    f'<button type="button" class="filter" data-filter="{k}">{v}</button>'
    for k, v in [("all", "الكل")] + list(CATEGORY_LABELS.items())
)

HTML = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>دليل ثيم زهر | مرجع السكاشن والمقاسات للعملاء</title>
  <meta name="description" content="دليل مرجعي كامل لسكاشن ثيم زهر: شرح كل قسم، المقاسات الموصى بها، وجداول الإعدادات للتجّار على سلة." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0f1412;
      --bg-soft: #171e1b;
      --panel: #1c2622;
      --line: rgba(232, 220, 198, 0.14);
      --text: #f4efe6;
      --muted: #a8b0aa;
      --accent: #c4a574;
      --accent-2: #6f9e86;
      --danger: #d pen;
      --radius: 18px;
      --shadow: 0 20px 50px rgba(0,0,0,.35);
      --font: "IBM Plex Sans Arabic", sans-serif;
      --display: "Noto Kufi Arabic", "IBM Plex Sans Arabic", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: var(--font);
      background:
        radial-gradient(1200px 600px at 90% -10%, rgba(196,165,116,.18), transparent 55%),
        radial-gradient(900px 500px at -10% 20%, rgba(111,158,134,.14), transparent 50%),
        linear-gradient(180deg, #101613 0%, #0f1412 40%, #121816 100%);
      color: var(--text);
      line-height: 1.7;
    }}
    a {{ color: inherit; text-decoration: none; }}
    img {{ max-width: 100%; display: block; }}
    .wrap {{ width: min(1120px, calc(100% - 2rem)); margin-inline: auto; }}

    .nav {{
      position: sticky; top: 0; z-index: 50;
      backdrop-filter: blur(14px);
      background: rgba(15,20,18,.72);
      border-bottom: 1px solid var(--line);
    }}
    .nav-inner {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; padding: .9rem 0;
    }}
    .brand {{
      font-family: var(--display); font-weight: 700; font-size: 1.25rem;
      letter-spacing: -.02em;
    }}
    .brand span {{ color: var(--accent); }}
    .nav-links {{ display: flex; gap: 1rem; flex-wrap: wrap; font-size: .95rem; color: var(--muted); }}
    .nav-links a:hover {{ color: var(--text); }}
    .nav-cta {{
      background: var(--accent); color: #1a1510; font-weight: 700;
      padding: .55rem 1rem; border-radius: 999px; font-size: .9rem;
    }}

    .hero {{
      padding: clamp(3rem, 8vw, 6rem) 0 3rem;
      position: relative;
      overflow: hidden;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1.15fr .85fr;
      gap: 2.5rem;
      align-items: end;
    }}
    @media (max-width: 900px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
      .nav-links {{ display: none; }}
    }}
    .eyebrow {{
      color: var(--accent); font-weight: 600; font-size: .9rem;
      margin-bottom: .75rem; display: inline-flex; gap: .5rem; align-items: center;
    }}
    .hero h1 {{
      font-family: var(--display);
      font-size: clamp(2.2rem, 5vw, 3.6rem);
      line-height: 1.25; margin: 0 0 1rem;
    }}
    .hero h1 em {{
      font-style: normal; color: var(--accent);
    }}
    .hero-lead {{
      color: var(--muted); font-size: 1.08rem; max-width: 36rem; margin: 0 0 1.75rem;
    }}
    .hero-actions {{ display: flex; flex-wrap: wrap; gap: .75rem; }}
    .btn {{
      display: inline-flex; align-items: center; justify-content: center;
      padding: .8rem 1.25rem; border-radius: 999px; font-weight: 700;
      border: 1px solid transparent; transition: .2s ease;
    }}
    .btn-primary {{ background: var(--accent); color: #1a1510; }}
    .btn-primary:hover {{ filter: brightness(1.05); transform: translateY(-1px); }}
    .btn-ghost {{ border-color: var(--line); color: var(--text); }}
    .btn-ghost:hover {{ border-color: var(--accent); color: var(--accent); }}

    .stats {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem;
    }}
    .stat {{
      background: rgba(255,255,255,.03);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 1.1rem 1rem;
    }}
    .stat strong {{
      display: block; font-family: var(--display);
      font-size: 1.7rem; color: var(--accent); line-height: 1.2;
    }}
    .stat span {{ color: var(--muted); font-size: .88rem; }}

    section.block {{ padding: 3.5rem 0; }}
    .block h2 {{
      font-family: var(--display); font-size: clamp(1.6rem, 3vw, 2.2rem);
      margin: 0 0 .5rem;
    }}
    .block .sub {{ color: var(--muted); margin: 0 0 1.75rem; max-width: 40rem; }}

    .why-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;
    }}
    @media (max-width: 800px) {{ .why-grid, .stats, .sec-grid {{ grid-template-columns: 1fr; }} }}
    .why {{
      background: var(--panel); border: 1px solid var(--line);
      border-radius: var(--radius); padding: 1.35rem;
    }}
    .why h3 {{ margin: 0 0 .4rem; font-size: 1.05rem; }}
    .why p {{ margin: 0; color: var(--muted); font-size: .95rem; }}

    .filters {{
      display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 1.25rem;
    }}
    .filter {{
      background: transparent; color: var(--muted); border: 1px solid var(--line);
      border-radius: 999px; padding: .45rem .9rem; cursor: pointer; font: inherit;
    }}
    .filter.active, .filter:hover {{
      color: #1a1510; background: var(--accent); border-color: var(--accent);
    }}

    .sec-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;
    }}
    @media (max-width: 1000px) {{ .sec-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    .sec-card {{
      background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      border: 1px solid var(--line); border-radius: var(--radius);
      padding: 1.2rem; min-height: 180px; transition: .2s ease;
      display: flex; flex-direction: column; gap: .55rem;
    }}
    .sec-card:hover {{
      transform: translateY(-3px); border-color: rgba(196,165,116,.45);
      box-shadow: var(--shadow);
    }}
    .sec-num {{
      font-family: var(--display); color: var(--accent); font-size: .85rem; letter-spacing: .08em;
    }}
    .sec-card h3 {{ margin: 0; font-size: 1.05rem; }}
    .sec-card p {{ margin: 0; color: var(--muted); font-size: .9rem; flex: 1; }}
    .sec-meta {{
      display: flex; justify-content: space-between; gap: .5rem;
      color: var(--accent-2); font-size: .8rem; border-top: 1px solid var(--line);
      padding-top: .7rem; margin-top: .2rem;
    }}

    .sizes-table {{
      width: 100%; border-collapse: collapse; overflow: hidden;
      border: 1px solid var(--line); border-radius: var(--radius);
      background: var(--panel);
    }}
    .sizes-table th, .sizes-table td {{
      padding: .85rem 1rem; border-bottom: 1px solid var(--line); text-align: right;
    }}
    .sizes-table th {{ color: var(--muted); font-weight: 600; font-size: .85rem; }}
    .sizes-table tr:last-child td {{ border-bottom: 0; }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      background: rgba(255,255,255,.06); padding: .15rem .4rem; border-radius: 6px;
      font-size: .88em; direction: ltr; unicode-bidi: plaintext;
    }}

    .detail {{
      margin: 2rem 0 3rem; padding: 1.5rem;
      background: rgba(28,38,34,.7); border: 1px solid var(--line);
      border-radius: calc(var(--radius) + 4px);
      scroll-margin-top: 5rem;
    }}
    .detail-head {{
      display: flex; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;
      margin-bottom: 1.25rem;
    }}
    .cat-pill {{
      display: inline-block; font-size: .78rem; color: var(--accent-2);
      border: 1px solid rgba(111,158,134,.35); padding: .2rem .6rem; border-radius: 999px;
      margin-bottom: .5rem;
    }}
    .detail h2 {{ margin: 0 0 .4rem; font-family: var(--display); }}
    .lead {{ color: var(--muted); margin: 0 0 .9rem; max-width: 46rem; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: .4rem; }}
    .badge {{
      background: rgba(196,165,116,.12); border: 1px solid rgba(196,165,116,.3);
      color: var(--text); border-radius: 999px; padding: .25rem .7rem; font-size: .82rem;
    }}
    .badge.muted {{ background: rgba(255,255,255,.04); border-color: var(--line); color: var(--muted); }}
    .file-box {{
      background: var(--bg-soft); border: 1px dashed var(--line); border-radius: 14px;
      padding: .9rem 1rem; min-width: 220px;
    }}
    .file-box span {{ display: block; color: var(--muted); font-size: .8rem; margin-bottom: .25rem; }}
    .panel {{
      background: rgba(0,0,0,.18); border: 1px solid var(--line);
      border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 1rem;
    }}
    .panel h4 {{ margin: 0 0 .75rem; font-size: 1rem; }}
    .tips {{ margin: 0; padding-inline-start: 1.2rem; color: var(--muted); }}
    .tips li {{ margin-bottom: .35rem; }}
    .empty {{ color: var(--muted); margin: 0; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{
      text-align: right; padding: .7rem .55rem; border-bottom: 1px solid var(--line);
      vertical-align: top; font-size: .92rem;
    }}
    th {{ color: var(--muted); font-weight: 600; white-space: nowrap; }}
    .type {{
      display: inline-block; background: rgba(111,158,134,.15); color: #b7d5c6;
      border-radius: 8px; padding: .1rem .45rem; font-size: .8rem;
    }}
    .back-top {{
      display: inline-block; margin-top: .5rem; color: var(--accent); font-weight: 600;
    }}

    .faq details {{
      background: var(--panel); border: 1px solid var(--line);
      border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: .65rem;
    }}
    .faq summary {{ cursor: pointer; font-weight: 600; }}
    .faq p {{ color: var(--muted); margin: .7rem 0 0; }}

    .cta {{
      margin: 2rem 0 4rem; padding: 2.2rem;
      border-radius: calc(var(--radius) + 6px);
      background:
        linear-gradient(135deg, rgba(196,165,116,.18), rgba(111,158,134,.12)),
        var(--panel);
      border: 1px solid var(--line);
      text-align: center;
    }}
    .cta h2 {{ margin: 0 0 .5rem; font-family: var(--display); }}
    .cta p {{ color: var(--muted); margin: 0 0 1.2rem; }}

    footer {{
      border-top: 1px solid var(--line); padding: 1.5rem 0 2.5rem; color: var(--muted);
      font-size: .9rem;
    }}
    footer .foot {{
      display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    }}

    .search {{
      width: 100%; max-width: 360px; margin-bottom: 1rem;
      background: var(--panel); border: 1px solid var(--line); color: var(--text);
      border-radius: 999px; padding: .7rem 1rem; font: inherit;
    }}
    .search::placeholder {{ color: var(--muted); }}
    .hidden {{ display: none !important; }}
  </style>
</head>
<body>
  <header class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="#">ثيم <span>زهر</span></a>
      <nav class="nav-links">
        <a href="#why">ليش الدليل؟</a>
        <a href="#sizes">جدول المقاسات</a>
        <a href="#sections">السكاشن</a>
        <a href="#header">الهيدر والتخطيط</a>
        <a href="#faq">أسئلة شائعة</a>
      </nav>
      <a class="nav-cta" href="https://github.com/smartcodecrew/zahar2" target="_blank" rel="noopener">المستودع على GitHub</a>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <div class="eyebrow">مرجع العملاء · ثيم سلة</div>
          <h1>دليل ثيم <em>زهر</em><br/>شرح كل سكشن والمقاسات في مكان واحد</h1>
          <p class="hero-lead">
            صفحة مرجعية للتجّار وفرق المحتوى: ماذا يفعل كل سكشن، أي مقاس صورة ترفع،
            وما الإعدادات المتاحة — بنفس روح صفحات توثيق الثيمات الاحترافية.
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#sections">تصفّح السكاشن</a>
            <a class="btn btn-ghost" href="#sizes">جدول المقاسات السريع</a>
          </div>
        </div>
        <div class="stats">
          <div class="stat"><strong>{len(DATA)}</strong><span>سكشن موثّق</span></div>
          <div class="stat"><strong>RTL</strong><span>عربي بالكامل</span></div>
          <div class="stat"><strong>1</strong><span>مرجع موحّد لكل العملاء</span></div>
        </div>
      </div>
    </section>

    <section class="block" id="why">
      <div class="wrap">
        <h2>ليش الدليل؟</h2>
        <p class="sub">بدل ما كل عميل يسأل عن المقاسات والإعدادات، هذا المرجع يوحّد الإجابة ويسرّع تجهيز المحتوى.</p>
        <div class="why-grid">
          <div class="why">
            <h3>مقاسات واضحة</h3>
            <p>كل صورة لها مقاس موصى به مستخرج من إعدادات الثيم نفسها، مع نصائح للرفع.</p>
          </div>
          <div class="why">
            <h3>شرح لكل سكشن</h3>
            <p>متى تستخدم السكشن، ماذا يظهر للعميل، وكيف تخصّصه من محرر سلة.</p>
          </div>
          <div class="why">
            <h3>جداول إعدادات</h3>
            <p>قائمة الحقول (نص، صورة، لون، قائمة…) مع الملاحظات والقيم الافتراضية.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="block" id="sizes">
      <div class="wrap">
        <h2>جدول المقاسات السريع</h2>
        <p class="sub">أهم المقاسات اللي يحتاجها فريق التصميم قبل رفع الصور على المتجر.</p>
        <table class="sizes-table">
          <thead><tr><th>الموضع</th><th>المقاس الموصى به</th></tr></thead>
          <tbody>
            <tr><td>شعار الهيدر (ديسكتوب / جوال)</td><td><code>180 × 90</code></td></tr>
            <tr><td>سلايدر رئيسي — جوال / افتراضي</td><td><code>1400 × 600</code></td></tr>
            <tr><td>سلايدر رئيسي — سطح المكتب</td><td><code>1920 × 800</code></td></tr>
            <tr><td>مقارنة قبل وبعد</td><td><code>1200 × 500</code></td></tr>
            <tr><td>معرض الصور (Gallery)</td><td><code>750 × 750</code></td></tr>
            <tr><td>بطاقات الفئات</td><td><code>480 × 170</code></td></tr>
            <tr><td>أيقونات المميزات / الشركاء</td><td><code>200 × 200</code></td></tr>
            <tr><td>فيديو (MP4)</td><td><code>أقصى 10MB</code></td></tr>
            <tr><td>ريلز</td><td><code>1080 × 1920 (9:16) مفضّل</code></td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="block" id="header">
      <div class="wrap">
        <h2>الهيدر وإعدادات التخطيط</h2>
        <p class="sub">إعدادات عامة تؤثر على كل صفحات المتجر — ابدأ منها قبل بناء الصفحة الرئيسية.</p>
        <div class="why-grid">
          <div class="why">
            <h3>الهيدر</h3>
            <p>شعار {HEADER_SIZES[0]['size']}، شعار جوال اختياري بنفس المقاس، شريط تنبيهات، رأس ثابت، وإخفاء اللغة/العملة.</p>
          </div>
          {''.join(f'<div class="why"><h3>{escape(h["title"])}</h3><p>{escape(h["text"])}</p></div>' for h in LAYOUT_HIGHLIGHTS[:2])}
        </div>
      </div>
    </section>

    <section class="block" id="sections">
      <div class="wrap">
        <h2>سكاشن الثيم</h2>
        <p class="sub">اضغط أي سكشن للانتقال لشرحه الكامل، المقاسات، وجدول الإعدادات.</p>
        <input class="search" id="search" type="search" placeholder="ابحث باسم السكشن…" />
        <div class="filters" id="filters">
          {FILTERS}
        </div>
        <div class="sec-grid" id="cards">
          {CARDS}
        </div>
      </div>
    </section>

    <section class="block" id="details">
      <div class="wrap">
        <h2>التفاصيل المرجعية</h2>
        <p class="sub">مرجع كامل لكل سكشن — انسخ المقاسات لفريق التصميم وشارك الرابط مع العملاء.</p>
        {DETAILS}
      </div>
    </section>

    <section class="block faq" id="faq">
      <div class="wrap">
        <h2>أسئلة شائعة</h2>
        <p class="sub">إجابات سريعة للتجّار قبل رفع الصور وتفعيل السكاشن.</p>
        <details open>
          <summary>هل لازم ألتزم بالمقاس بالبكسل حرفيًا؟</summary>
          <p>الأفضل الالتزام بالنسبة والمقاس الموصى به. لو الصورة أكبر بنفس النسبة غالبًا تظهر بشكل ممتاز. لو أصغر أو بنسبة مختلفة قد تظهر مقصوصة أو ممدودة.</p>
        </details>
        <details>
          <summary>أي صيغة صور أفضل؟</summary>
          <p>JPG للصور الفوتوغرافية، PNG للأيقونات والشعارات بخلفية شفافة، وWebP إن كانت متاحة لديك بجودة عالية وحجم أقل.</p>
        </details>
        <details>
          <summary>هل الدليل يتحدث تلقائيًا مع تحديث الثيم؟</summary>
          <p>نعم — هذا الدليل مبني من ملفات الـ schema في المستودع. عند إضافة سكشن أو تعديل مقاس، نحدّث الصفحة ونرفعها على GitHub Pages.</p>
        </details>
        <details>
          <summary>وين ألاقي الدليل بعد الرفع؟</summary>
          <p>من رابط GitHub Pages الخاص بالمستودع (يظهر بعد تفعيل Pages من إعدادات المستودع على مجلد docs).</p>
        </details>
      </div>
    </section>

    <div class="wrap">
      <div class="cta">
        <h2>جاهز تجهّز محتوى متجرك؟</h2>
        <p>شارك هذا الرابط مع المصمم وفريق المحتوى — كل المقاسات والإعدادات في صفحة واحدة.</p>
        <a class="btn btn-primary" href="#sections">ارجع للسكاشن</a>
      </div>
    </div>
  </main>

  <footer>
    <div class="wrap foot">
      <div>© 2026 ثيم زهر · دليل العملاء المرجعي</div>
      <div><a href="https://github.com/smartcodecrew/zahar2" target="_blank" rel="noopener">smartcodecrew/zahar2</a></div>
    </div>
  </footer>

  <script>
    const filters = document.getElementById('filters');
    const cards = [...document.querySelectorAll('.sec-card')];
    const details = [...document.querySelectorAll('.detail')];
    const search = document.getElementById('search');
    let active = 'all';

    function apply() {{
      const q = (search.value || '').trim();
      cards.forEach(card => {{
        const cat = card.dataset.cat;
        const text = card.innerText;
        const okCat = active === 'all' || cat === active;
        const okQ = !q || text.includes(q);
        card.classList.toggle('hidden', !(okCat && okQ));
      }});
      details.forEach(d => {{
        const cat = d.dataset.cat;
        const text = d.innerText;
        const okCat = active === 'all' || cat === active;
        const okQ = !q || text.includes(q);
        d.classList.toggle('hidden', !(okCat && okQ));
      }});
    }}

    filters.addEventListener('click', (e) => {{
      const btn = e.target.closest('.filter');
      if (!btn) return;
      active = btn.dataset.filter;
      filters.querySelectorAll('.filter').forEach(b => b.classList.toggle('active', b === btn));
      apply();
    }});
    filters.querySelector('[data-filter="all"]').classList.add('active');
    search.addEventListener('input', apply);
  </script>
</body>
</html>
"""

# fix accidental typo in CSS if any
HTML = HTML.replace("--danger: #d pen;", "--danger: #d97a6c;")

out = ROOT / "docs" / "index.html"
out.write_text(HTML, encoding="utf-8")
print("Wrote", out, "bytes", out.stat().st_size)

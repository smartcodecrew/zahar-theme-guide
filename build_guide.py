# -*- coding: utf-8 -*-
"""Generate Arabic client reference guide for Zahra / Zahar theme."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# —— Brand / commercial ——
THEME_NAME_AR = "زهرة"
THEME_NAME_EN = "Zahra"
THEME_PRICE = "460 ر.س"
THEME_PRICE_OLD = "700 ر.س"
THEME_PRICE_NOTE = "دفعة واحدة · تخصيص ودعم فني"
THEME_PRICE_HELP = "إذا واجهت مشكلة في إعدادات الثيم، راسلنا وسنساعدك مجاناً"
CONTACT_EMAIL = "smartcodecrew@gmail.com"
CONTACT_PHONE = "01145828786"
CONTACT_PHONE_TEL = "+201145828786"
PREVIEW_URL = (
    "https://doyftt.dev.zid.store/ar/"
    "?theme=8a4af4f7-7c81-4c0c-a672-82b970f4a2cb"
    "&md_token=Zt4meo486fHGqn7eu0wHjYkp4ToWWuhutsf3wRMpO7y7J6sAzv98K0mVAT7Udbn5"
    "&previewMode=true"
)
EDITOR_URL = (
    "https://dashboard.zid.sa/ar-sa/stores/641897/theme-editor/"
    "8a4af4f7-7c81-4c0c-a672-82b970f4a2cb"
)
GITHUB_GUIDE = "https://github.com/smartcodecrew/zahar-theme-guide"
GITHUB_PAGES = "https://smartcodecrew.github.io/zahar-theme-guide/"

# Colors from live theme preview (--primary-color)
PRIMARY = "#5e3855"
PRIMARY_DARK = "#521B25"
PRIMARY_SOFT = "#7a4d70"
ON_PRIMARY = "#ffffff"
BG = "#faf7f9"
PANEL = "#ffffff"
TEXT = "#2c2c2c"
MUTED = "#6b6570"
LINE = "rgba(94, 56, 85, 0.14)"
ACCENT_GOLD = "#c4a574"


def extract_schema(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    name = data.get("name", {})
    groups = []
    for g in data.get("groups", []):
        gname = g.get("name", {})
        gname = gname.get("ar") if isinstance(gname, dict) else gname
        settings = []

        def collect(obj):
            if isinstance(obj, dict):
                if "type" in obj and "id" in obj and obj.get("type") != "fieldset":
                    lab = obj.get("label")
                    info = obj.get("info")
                    settings.append(
                        {
                            "id": obj.get("id"),
                            "type": obj.get("type"),
                            "label": lab.get("ar") if isinstance(lab, dict) else lab,
                            "info": info.get("ar") if isinstance(info, dict) else info,
                            "default": obj.get("default"),
                        }
                    )
                for v in obj.values():
                    collect(v)
            elif isinstance(obj, list):
                for i in obj:
                    collect(i)

        collect(g)
        seen, uniq = set(), []
        for s in settings:
            k = (s["id"], s["label"], s["type"])
            if k in seen:
                continue
            seen.add(k)
            uniq.append(s)
        groups.append({"id": g.get("id"), "name": gname, "settings": uniq})
    return {
        "name_ar": name.get("ar") if isinstance(name, dict) else name,
        "name_en": name.get("en") if isinstance(name, dict) else "",
        "groups": groups,
    }


def extract_sections():
    results = []
    for schema_path in sorted((ROOT / "sections").glob("*.schema.json")):
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        name = data.get("name", {})
        images, settings_summary = [], []

        def walk(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "image":
                    label, info = obj.get("label"), obj.get("info")
                    images.append(
                        {
                            "id": obj.get("id"),
                            "label": label.get("ar") if isinstance(label, dict) else label,
                            "info": info.get("ar") if isinstance(info, dict) else info,
                        }
                    )
                if "type" in obj and "id" in obj:
                    label, info = obj.get("label"), obj.get("info")
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
        results.append(
            {
                "file": schema_path.name,
                "jinja": schema_path.name.replace(".schema.json", ".jinja"),
                "name_ar": name.get("ar") if isinstance(name, dict) else str(name),
                "name_en": name.get("en") if isinstance(name, dict) else "",
                "images": images,
                "settings": settings_summary,
            }
        )
    return results


DATA = extract_sections()
LAYOUT = extract_schema(ROOT / "layout.schema.json")
HEADER = extract_schema(ROOT / "header.schema.json")

ENRICH = {
    "main-slider.schema.json": {
        "desc": "السلايدر الرئيسي أعلى الصفحة. من المعاينة الحية: صور بعرض ~1900×594 تظهر بعرض الشاشة.",
        "tips": [
            "الصور المستخدمة في المعاينة: تقريباً 1900 × 594.",
            "المقاس الموصى في الإعدادات: 1400×600 للجوال و 1920×800 للكمبيوتر.",
            "اكتب العنوان والزر من الإعدادات وليس داخل الصورة.",
        ],
        "sizes": [
            {"label": "صورة الجوال / الافتراضية", "size": "1400 × 600"},
            {"label": "صورة سطح المكتب", "size": "1920 × 800"},
            {"label": "مثال حي من المعاينة", "size": "~1900 × 594"},
        ],
        "category": "hero",
        "live": "جمالك يبدأ من هنا",
    },
    "ticker.schema.json": {
        "desc": "شريط متحرك للعروض والرسائل الترويجية.",
        "tips": ["نص قصير وواضح.", "ألوان متوافقة مع هوية المتجر."],
        "sizes": [],
        "category": "promo",
    },
    "features-section.schema.json": {
        "desc": "مميزات المتجر بأيقونات وعناوين لبناء الثقة.",
        "tips": ["أيقونات PNG بخلفية شفافة.", "يفضّل 3–6 عناصر."],
        "sizes": [{"label": "أيقونة", "size": "200 × 200"}],
        "category": "content",
    },
    "partners.schema.json": {
        "desc": "شعارات الشركاء والعلامات (شركاؤنا المتميزين في المعاينة).",
        "tips": ["وحّد ارتفاع الشعارات.", "خلفية شفافة أنظف."],
        "sizes": [{"label": "شعار الشريك", "size": "200 × 200"}],
        "category": "content",
        "live": "شركأنا المتميزين",
    },
    "category-section.schema.json": {
        "desc": "سلايدر تصنيفات مربوط بتصنيفات سلة/زد.",
        "tips": ["اختر تصنيفات لها صور واضحة."],
        "sizes": [{"label": "صورة التصنيف", "size": "حوالي 400 × 400"}],
        "category": "catalog",
    },
    "category-products-section.schema.json": {
        "desc": "بطاقات فئات دائرية/أفقية بروابط مخصصة — ظاهرة أسفل السلايدر في المعاينة.",
        "tips": ["التزم بالمقاس الموحّد."],
        "sizes": [{"label": "صورة الفئة", "size": "480 × 170"}],
        "category": "catalog",
        "live": "العطور / المكياج / العناية…",
    },
    "collection-section.schema.json": {
        "desc": "مجموعات متنوعة بتابات وصور ديسكتوب/موبايل مع منتج.",
        "tips": ["جهّز نسختين للصورة.", "اختر منتجاً بارزاً."],
        "sizes": [
            {"label": "صورة الكمبيوتر", "size": "~600 عرض"},
            {"label": "صورة الموبايل", "size": "~400 عرض"},
        ],
        "category": "catalog",
        "live": "الصيف / مفضلات المشاهير",
    },
    "diffrent-collction.schema.json": {
        "desc": "اكتشف مجموعتنا المميزة — صور وعناوين وروابط.",
        "tips": ["مناسب للحملات الموسمية."],
        "sizes": [{"label": "صورة العنصر", "size": "مربّع 1:1 مفضّل"}],
        "category": "catalog",
    },
    "exploere-collections.schema.json": {
        "desc": "استكشاف المجموعات بصورة وعنوان ورابط (ظاهر في المعاينة بعنوان «استكشف المجموعات»).",
        "tips": ["وحّد نسب الصور."],
        "sizes": [{"label": "صورة المجموعة", "size": "مربّع أو عرضي"}],
        "category": "catalog",
        "live": "استكشف المجموعات",
    },
    "products-section.schema.json": {
        "desc": "عرض منتجات من تصنيفات — بطاقة المنتج في الثيم بأزرار أضف للسلة والمعاينة السريعة.",
        "tips": ["صور منتجات مربّعة ~1000×1000 تظهر بأفضل شكل."],
        "sizes": [{"label": "صورة المنتج", "size": "1000 × 1000 مفضّل"}],
        "category": "products",
        "live": "الأكثر مبيعا",
    },
    "products-tabs-section.schema.json": {
        "desc": "منتجات على تابات (أحدث المنتجات، المرطبات…). من المعاينة: شبكة حتى 6 أعمدة على الديسكتوب.",
        "tips": ["سمِّ التابات بوضوح."],
        "sizes": [{"label": "صورة المنتج", "size": "1000 × 1000 مفضّل"}],
        "category": "products",
        "live": "أحدث المنتجات",
    },
    "products-showcase-slider.schema.json": {
        "desc": "سلايدر إبراز منتجات/محتوى بصري (مادة طبيعية في المعاينة).",
        "tips": ["صور احترافية عالية الجودة."],
        "sizes": [],
        "category": "products",
        "live": "مادة طبيعية",
    },
    "promo-samples-banner.schema.json": {
        "desc": "بنر ترويجي للعينات/العروض — في المعاينة: «عينات مكياج مجانية».",
        "tips": ["رسالة قصيرة وزر واضح."],
        "sizes": [{"label": "خلفية البنر (إن وُجدت)", "size": "حسب العرض الكامل"}],
        "category": "promo",
        "live": "عينات مكياج مجانية",
    },
    "image-tabs-slider.schema.json": {
        "desc": "سلايدر صور مع تابات.",
        "tips": ["وحّد مقاسات الصور داخل السكشن."],
        "sizes": [],
        "category": "media",
    },
    "ggallery.schema.json": {
        "desc": "معرض صور / بنرات عمودية متعددة — مناسب لعروض المنتجات والحملات.",
        "tips": ["المقاس المربّع أو العمودي حسب تصميم البطاقات.", "وحّد نسبة الصور داخل نفس الصف."],
        "sizes": [{"label": "صورة المعرض / البنر", "size": "750 × 750 أو عمودي حسب التصميم"}],
        "category": "media",
        "live": "عناية مرطبة بالبشرة",
    },
    "video.schema.json": {
        "desc": "سكشن فيديو للمنتج أو الحملة.",
        "tips": ["MP4 مضغوط — أقصى 10MB."],
        "sizes": [{"label": "فيديو", "size": "MP4 — أقصى 10MB"}],
        "category": "media",
    },
    "reels-section.schema.json": {
        "desc": "ريلز عمودية بأسلوب سوشيال مع بطاقة منتج وسعر أسفل كل ريل.",
        "tips": ["النسبة العمودية (9:16) هي الأنسب.", "اجعل مدة الفيديو/المحتوى قصيرة.", "اربط كل ريل بمنتج واضح."],
        "sizes": [{"label": "صورة/فيديو الريل", "size": "1080 × 1920 (9:16)"}],
        "category": "media",
        "live": "مفضلات المشاهير",
    },
    "before-after-section.schema.json": {
        "desc": "مقارنة قبل وبعد بسحّاب تفاعلي — ظاهرة في المعاينة لمحتوى العناية بالبشرة.",
        "tips": ["نفس الزاوية والإضاءة للصورتين.", "المقاسان متطابقان."],
        "sizes": [
            {"label": "صورة قبل", "size": "1200 × 500"},
            {"label": "صورة بعد", "size": "1200 × 500"},
        ],
        "category": "media",
        "live": "بشرة مرهقة وجافة",
    },
    "testimonials.schema.json": {
        "desc": "آراء العملاء (يقول العملاء! في المعاينة).",
        "tips": ["آراء قصيرة أوضح."],
        "sizes": [{"label": "صورة العميل", "size": "~150 × 150"}],
        "category": "social",
        "live": "يقول العملاء!",
    },
    "why_choose_us.schema.json": {
        "desc": "لماذا تختارنا؟ — نقاط قوة المتجر.",
        "tips": ["ركّز على فوائد العميل."],
        "sizes": [],
        "category": "content",
        "live": "لماذا تختارنا؟",
    },
    "faq-section.schema.json": {
        "desc": "أسئلة شائعة قابلة للطي.",
        "tips": ["الأكثر تكراراً أولاً."],
        "sizes": [],
        "category": "content",
        "live": "الأسئلة الشائعه",
    },
    "blog-section.schema.json": {
        "desc": "المدونة — سلايدر أو شبكة مقالات.",
        "tips": ["صورة مقال موحّدة المقاس."],
        "sizes": [{"label": "صورة المقال", "size": "~600 عرض (16:9 أو 4:3)"}],
        "category": "content",
        "live": "المدونة",
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
    "range": "شريط قيمة",
    "category_products": "منتجات تصنيف",
}


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


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\u0600-\u06FF\-]+", "-", name.strip(), flags=re.UNICODE)
    return s.strip("-") or "section"


def shot_path(key: str) -> str | None:
    p = DOCS / "assets" / "sections" / f"{key}.png"
    return f"assets/sections/{key}.png" if p.exists() else None


def shot_html(key: str, alt: str, cls: str = "sec-shot") -> str:
    src = shot_path(key)
    if not src:
        return f'<div class="shot-missing">لا توجد لقطة من المعاينة لهذا السكشن حالياً</div>'
    return f'<figure class="{cls}"><img src="{src}" alt="{escape(alt)}" loading="lazy" /></figure>'


def sizes_for(sec):
    enrich = ENRICH.get(sec["file"], {})
    if enrich.get("sizes"):
        return enrich["sizes"]
    out = []
    for img in sec.get("images") or []:
        info = img.get("info") or ""
        m = re.search(r"(\d+)\s*[*×x]\s*(\d+)", info)
        if m:
            out.append({"label": img.get("label") or "صورة", "size": f"{m.group(1)} × {m.group(2)}"})
        elif info:
            out.append({"label": img.get("label") or "صورة", "size": info})
    return out


def settings_table(settings):
    seen, rows = set(), []
    for st in settings:
        key = (st.get("id"), st.get("label"), st.get("type"))
        if key in seen:
            continue
        seen.add(key)
        typ = TYPE_AR.get(st.get("type") or "", st.get("type") or "—")
        info = st.get("info") or "—"
        default = st.get("default")
        default_s = "—" if default is None else escape(default)
        rows.append(
            f"<tr><td>{escape(st.get('label') or st.get('id'))}</td>"
            f"<td><span class='type'>{escape(typ)}</span></td>"
            f"<td>{escape(info)}</td>"
            f"<td><code>{default_s}</code></td></tr>"
        )
    return rows


def build_global_block(title, sid, intro, groups, extra_sizes=None, shot_key=None):
    sizes_html = ""
    if extra_sizes:
        rows = "".join(
            f"<tr><td>{escape(s['label'])}</td><td><code>{escape(s['size'])}</code></td></tr>"
            for s in extra_sizes
        )
        sizes_html = f"""
        <div class="panel">
          <h4>المقاسات</h4>
          <table><thead><tr><th>العنصر</th><th>المقاس</th></tr></thead><tbody>{rows}</tbody></table>
        </div>"""
    shot = shot_html(shot_key, title, "detail-shot") if shot_key else ""
    groups_html = []
    for g in groups:
        rows = settings_table(g["settings"])
        groups_html.append(
            f"""
            <div class="panel">
              <h4>{escape(g.get('name') or g.get('id'))} ({len(rows)})</h4>
              <div class="table-wrap">
                <table>
                  <thead><tr><th>الإعداد</th><th>النوع</th><th>ملاحظة / مقاس</th><th>افتراضي</th></tr></thead>
                  <tbody>{''.join(rows)}</tbody>
                </table>
              </div>
            </div>"""
        )
    return f"""
    <article class="detail" id="{sid}">
      <header class="detail-head">
        <div>
          <span class="cat-pill">إعدادات عامة</span>
          <h2>{escape(title)}</h2>
          <p class="lead">{escape(intro)}</p>
        </div>
      </header>
      {shot}
      {sizes_html}
      {''.join(groups_html)}
      <a class="back-top" href="#globals">↑ العودة للإعدادات العامة</a>
    </article>"""


def build_sections_html():
    cards, details = [], []
    for i, sec in enumerate(DATA, 1):
        enrich = ENRICH.get(sec["file"], {})
        name = (sec.get("name_ar") or sec.get("name_en") or sec["file"]).strip()
        key = sec["file"].replace(".schema.json", "")
        sid = f"sec-{i}-{slugify(key)}"
        cat = enrich.get("category", "other")
        desc = enrich.get("desc", "سكشن قابل للتخصيص من محرر الثيم.")
        tips = enrich.get("tips") or []
        sizes = sizes_for(sec)
        live = enrich.get("live")
        settings = sec.get("settings") or []
        thumb = shot_path(key)

        size_badges = "".join(
            f'<span class="badge">{escape(s["label"])}: <strong>{escape(s["size"])}</strong></span>'
            for s in sizes
        ) or '<span class="badge muted">لا يتطلب صوراً بمقاس ثابت</span>'

        live_badge = f'<span class="live">في المعاينة: {escape(live)}</span>' if live else ""
        thumb_html = (
            f'<div class="card-thumb"><img src="{thumb}" alt="{escape(name)}" loading="lazy" /></div>'
            if thumb
            else '<div class="card-thumb missing">بدون لقطة</div>'
        )

        cards.append(
            f"""
            <a class="sec-card" href="#{sid}" data-cat="{cat}">
              {thumb_html}
              <span class="sec-num">{i:02d}</span>
              <h3>{escape(name)}</h3>
              <p>{escape(desc[:100])}{'…' if len(desc) > 100 else ''}</p>
              {live_badge}
              <div class="sec-meta">
                <span>{len(settings)} إعداد</span>
                <span>{CATEGORY_LABELS.get(cat, cat)}</span>
              </div>
            </a>"""
        )

        tips_html = (
            "<ul class='tips'>" + "".join(f"<li>{escape(t)}</li>" for t in tips) + "</ul>"
            if tips
            else "<p class='empty'>عاين على الجوال قبل النشر.</p>"
        )
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
              <p class="empty">لا يوجد مقاس صورة ثابت إلزامي لهذا السكشن.</p>
            </div>"""

        set_rows = settings_table(settings)
        details.append(
            f"""
            <article class="detail" id="{sid}" data-cat="{cat}">
              <header class="detail-head">
                <div>
                  <span class="cat-pill">{escape(CATEGORY_LABELS.get(cat, cat))}</span>
                  <h2>{escape(name)}</h2>
                  <p class="lead">{escape(desc)}</p>
                  {live_badge}
                  <div class="badges">{size_badges}</div>
                </div>
                <div class="file-box">
                  <span>ملف السكشن</span>
                  <code>{escape(sec.get('jinja') or '')}</code>
                </div>
              </header>
              {shot_html(key, name, "detail-shot")}
              {sizes_html}
              <div class="panel"><h4>نصائح للتجّار</h4>{tips_html}</div>
              <div class="panel">
                <h4>جدول الإعدادات ({len(set_rows)})</h4>
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

HEADER_BLOCK = build_global_block(
    "الهيدر (أعلى الصفحة)",
    "global-header",
    "شعار المتجر، شريط البحث، الرأس الثابت، وشريط التنبيهات المتحرك.",
    HEADER["groups"],
    [
        {"label": "شعار الديسكتوب", "size": "180 × 90"},
        {"label": "شعار الجوال", "size": "180 × 90"},
        {"label": "عرض الشعار في المعاينة", "size": "180 × 90 (ملف المصدر ~200×100)"},
    ],
    shot_key="header",
)

footer_groups = [g for g in LAYOUT["groups"] if g.get("id") == "footer"]
layout_groups = [g for g in LAYOUT["groups"] if g.get("id") != "footer"]

LAYOUT_BLOCK = build_global_block(
    "إعدادات التخطيط (Layout)",
    "global-layout",
    "الخطوط، ألوان الهيدر/الفوتر، تفاصيل المنتج، الأزرار العائمة (واتساب / رجوع لأعلى)، القائمة السفلية، ومنتجات السلة.",
    layout_groups,
    [
        {"label": "صورة خلفية عامة (إن وُجدت)", "size": "150 × 150"},
        {"label": "أيقونات الدفع في صفحة المنتج", "size": "حسب الأيقونة"},
    ],
)

FOOTER_BLOCK = build_global_block(
    "الفوتر (أسفل الصفحة)",
    "global-footer",
    "لوجو الفوتر، نبذة عن المتجر، شريط الخدمات، روابط مهمة، والموقع الجغرافي — ضمن إعدادات التخطيط.",
    footer_groups,
    [{"label": "لوجو أسفل الصفحة", "size": "200 × 200"}],
    shot_key="footer",
)

FILTERS = "".join(
    f'<button type="button" class="filter" data-filter="{k}">{v}</button>'
    for k, v in [("all", "الكل")] + list(CATEGORY_LABELS.items())
)

HTML = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>دليل ثيم {THEME_NAME_AR} | مرجع السكاشن والمقاسات</title>
  <meta name="description" content="دليل مرجعي لثيم {THEME_NAME_AR} على زد: شرح السكاشن، المقاسات، إعدادات الهيدر والفوتر والتخطيط، مع معاينة حية وتواصل مباشر." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --primary: {PRIMARY};
      --primary-dark: {PRIMARY_DARK};
      --primary-soft: {PRIMARY_SOFT};
      --on-primary: {ON_PRIMARY};
      --bg: {BG};
      --panel: {PANEL};
      --text: {TEXT};
      --muted: {MUTED};
      --line: {LINE};
      --gold: {ACCENT_GOLD};
      --radius: 18px;
      --shadow: 0 18px 40px rgba(94,56,85,.12);
      --font: "IBM Plex Sans Arabic", sans-serif;
      --display: "Noto Kufi Arabic", "IBM Plex Sans Arabic", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: var(--font);
      color: var(--text);
      background:
        radial-gradient(900px 420px at 100% 0%, rgba(94,56,85,.08), transparent 55%),
        radial-gradient(700px 360px at 0% 30%, rgba(196,165,116,.10), transparent 50%),
        var(--bg);
      line-height: 1.7;
    }}
    a {{ color: inherit; text-decoration: none; }}
    img {{ max-width: 100%; display: block; }}
    .wrap {{ width: min(1120px, calc(100% - 2rem)); margin-inline: auto; }}

    .nav {{
      position: sticky; top: 0; z-index: 50;
      backdrop-filter: blur(14px);
      background: rgba(250,247,249,.88);
      border-bottom: 1px solid var(--line);
    }}
    .nav-inner {{
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; padding: .85rem 0;
    }}
    .brand {{
      font-family: var(--display); font-weight: 700; font-size: 1.2rem;
      color: var(--primary);
    }}
    .nav-links {{ display: flex; gap: .9rem; flex-wrap: wrap; font-size: .92rem; color: var(--muted); }}
    .nav-links a:hover {{ color: var(--primary); }}
    .nav-cta {{
      background: var(--primary); color: var(--on-primary); font-weight: 700;
      padding: .55rem 1rem; border-radius: 999px; font-size: .88rem;
    }}

    .hero {{
      padding: clamp(2.5rem, 7vw, 5rem) 0 2.5rem;
    }}
    .hero-grid {{
      display: grid; grid-template-columns: 1.05fr .95fr; gap: 2rem; align-items: center;
    }}
    @media (max-width: 900px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
      .nav-links {{ display: none; }}
    }}
    .eyebrow {{
      color: var(--primary-soft); font-weight: 600; font-size: .9rem; margin-bottom: .6rem;
    }}
    .hero h1 {{
      font-family: var(--display);
      font-size: clamp(2rem, 4.5vw, 3.2rem);
      line-height: 1.25; margin: 0 0 .9rem; color: var(--primary-dark);
    }}
    .hero h1 em {{ font-style: normal; color: var(--primary); }}
    .hero-lead {{ color: var(--muted); font-size: 1.05rem; max-width: 36rem; margin: 0 0 1.4rem; }}
    .hero-actions {{ display: flex; flex-wrap: wrap; gap: .65rem; margin-bottom: 1.2rem; }}
    .btn {{
      display: inline-flex; align-items: center; justify-content: center; gap: .4rem;
      padding: .75rem 1.15rem; border-radius: 999px; font-weight: 700;
      border: 1px solid transparent; transition: .2s ease;
    }}
    .btn-primary {{ background: var(--primary); color: var(--on-primary); }}
    .btn-primary:hover {{ background: var(--primary-dark); transform: translateY(-1px); }}
    .btn-ghost {{ border-color: var(--line); background: #fff; color: var(--primary); }}
    .btn-ghost:hover {{ border-color: var(--primary); }}
    .btn-gold {{ background: var(--gold); color: #2a2116; }}

    .price-chip {{
      display: inline-flex; flex-direction: column; gap: .15rem;
      background: #fff; border: 1px solid var(--line); border-radius: 16px;
      padding: .85rem 1.1rem; box-shadow: var(--shadow);
    }}
    .price-chip strong {{
      font-family: var(--display); font-size: 1.35rem; color: var(--primary);
    }}
    .price-chip .old-price {{
      color: var(--muted); font-size: .95rem; text-decoration: line-through;
    }}
    .price-chip span.note {{ color: var(--muted); font-size: .85rem; }}
    .price-chip .help {{
      color: var(--primary-soft); font-size: .78rem; line-height: 1.55;
      margin-top: .35rem; max-width: 16rem;
    }}

    .hero-visual {{
      border-radius: calc(var(--radius) + 6px); overflow: hidden;
      border: 1px solid var(--line); box-shadow: var(--shadow); background: #fff;
    }}
    .hero-visual img {{ width: 100%; aspect-ratio: 16/10; object-fit: cover; object-position: top; }}

    .contact-row {{
      display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1rem;
    }}
    .contact-pill {{
      display: inline-flex; align-items: center; gap: .45rem;
      background: rgba(94,56,85,.06); border: 1px solid var(--line);
      color: var(--primary-dark); border-radius: 999px; padding: .45rem .9rem;
      font-weight: 600; font-size: .9rem;
    }}
    .contact-pill:hover {{ background: var(--primary); color: #fff; border-color: var(--primary); }}

    section.block {{ padding: 3rem 0; }}
    .block h2 {{
      font-family: var(--display); font-size: clamp(1.5rem, 3vw, 2rem);
      margin: 0 0 .45rem; color: var(--primary-dark);
    }}
    .block .sub {{ color: var(--muted); margin: 0 0 1.5rem; max-width: 42rem; }}

    .preview-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;
    }}
    @media (max-width: 900px) {{ .preview-grid {{ grid-template-columns: 1fr; }} }}
    .shot {{
      background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
      overflow: hidden; box-shadow: var(--shadow);
    }}
    .shot img {{ width: 100%; aspect-ratio: 16/11; object-fit: cover; object-position: top; }}
    .shot figcaption {{
      padding: .75rem 1rem; color: var(--muted); font-size: .88rem;
      border-top: 1px solid var(--line);
    }}

    .swatches {{
      display: flex; flex-wrap: wrap; gap: .75rem; margin-bottom: 1.5rem;
    }}
    .swatch {{
      display: flex; align-items: center; gap: .6rem;
      background: #fff; border: 1px solid var(--line); border-radius: 14px;
      padding: .55rem .8rem; min-width: 160px;
    }}
    .swatch i {{
      width: 28px; height: 28px; border-radius: 8px; border: 1px solid var(--line);
    }}
    .swatch code {{ font-size: .85rem; direction: ltr; }}

    .why-grid, .stats {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: .85rem;
    }}
    @media (max-width: 800px) {{
      .why-grid, .stats, .sec-grid {{ grid-template-columns: 1fr; }}
    }}
    .why, .stat {{
      background: var(--panel); border: 1px solid var(--line);
      border-radius: var(--radius); padding: 1.15rem;
    }}
    .why h3 {{ margin: 0 0 .35rem; font-size: 1.02rem; color: var(--primary-dark); }}
    .why p {{ margin: 0; color: var(--muted); font-size: .94rem; }}
    .stat strong {{
      display: block; font-family: var(--display); font-size: 1.55rem;
      color: var(--primary); line-height: 1.2;
    }}
    .stat span {{ color: var(--muted); font-size: .88rem; }}

    .filters {{ display: flex; flex-wrap: wrap; gap: .45rem; margin-bottom: 1.1rem; }}
    .filter {{
      background: #fff; color: var(--muted); border: 1px solid var(--line);
      border-radius: 999px; padding: .4rem .85rem; cursor: pointer; font: inherit;
    }}
    .filter.active, .filter:hover {{
      color: #fff; background: var(--primary); border-color: var(--primary);
    }}

    .sec-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: .9rem;
    }}
    @media (max-width: 1000px) {{ .sec-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    .sec-card {{
      background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
      padding: 0; min-height: 220px; transition: .2s ease;
      display: flex; flex-direction: column; gap: 0; overflow: hidden;
    }}
    .sec-card:hover {{
      transform: translateY(-3px); border-color: rgba(94,56,85,.35); box-shadow: var(--shadow);
    }}
    .card-thumb {{
      aspect-ratio: 16/9; background: #f0eaef; overflow: hidden; border-bottom: 1px solid var(--line);
    }}
    .card-thumb img {{ width: 100%; height: 100%; object-fit: cover; object-position: top center; }}
    .card-thumb.missing {{
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); font-size: .85rem;
    }}
    .sec-card .sec-num, .sec-card h3, .sec-card p, .sec-card .live, .sec-card .sec-meta {{
      margin-inline: 1.05rem;
    }}
    .sec-card .sec-num {{ margin-top: .85rem; }}
    .sec-card h3 {{ margin-top: .25rem; margin-bottom: 0; }}
    .sec-card p {{ margin: .35rem 1.05rem; }}
    .sec-card .live {{ margin: 0 1.05rem .35rem; width: fit-content; }}
    .sec-card .sec-meta {{ margin: auto 1.05rem .9rem; padding-top: .65rem; }}
    .sec-num {{ font-family: var(--display); color: var(--primary); font-size: .82rem; letter-spacing: .06em; }}
    .sec-card h3 {{ font-size: 1.02rem; color: var(--primary-dark); }}
    .sec-card p {{ color: var(--muted); font-size: .88rem; flex: 1; }}
    .live {{
      display: inline-block; font-size: .78rem; color: var(--primary);
      background: rgba(94,56,85,.08); border-radius: 999px; padding: .15rem .55rem;
    }}
    .sec-meta {{
      display: flex; justify-content: space-between; gap: .5rem;
      color: var(--primary-soft); font-size: .78rem; border-top: 1px solid var(--line);
    }}
    .detail-shot {{
      margin: 0 0 1rem; border-radius: 14px; overflow: hidden;
      border: 1px solid var(--line); background: #f7f2f5;
    }}
    .detail-shot img {{ width: 100%; max-height: 520px; object-fit: contain; object-position: top; background: #fff; }}
    .shot-missing {{
      margin: 0 0 1rem; padding: 1.2rem; border-radius: 14px;
      border: 1px dashed var(--line); color: var(--muted); text-align: center; background: var(--bg);
    }}

    .sizes-table, table {{ width: 100%; border-collapse: collapse; }}
    .sizes-table {{
      background: #fff; border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden;
    }}
    .sizes-table th, .sizes-table td, th, td {{
      padding: .75rem .9rem; border-bottom: 1px solid var(--line); text-align: right;
      font-size: .92rem; vertical-align: top;
    }}
    .sizes-table th, th {{ color: var(--muted); font-weight: 600; }}
    .sizes-table tr:last-child td {{ border-bottom: 0; }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      background: rgba(94,56,85,.06); padding: .12rem .4rem; border-radius: 6px;
      font-size: .86em; direction: ltr; unicode-bidi: plaintext; color: var(--primary-dark);
    }}

    .detail {{
      margin: 1.75rem 0 2.5rem; padding: 1.35rem;
      background: #fff; border: 1px solid var(--line);
      border-radius: calc(var(--radius) + 4px); scroll-margin-top: 5rem;
      box-shadow: 0 8px 24px rgba(94,56,85,.05);
    }}
    .detail-head {{
      display: flex; justify-content: space-between; gap: 1.25rem; flex-wrap: wrap;
      margin-bottom: 1rem;
    }}
    .cat-pill {{
      display: inline-block; font-size: .76rem; color: var(--primary);
      border: 1px solid rgba(94,56,85,.25); padding: .18rem .55rem; border-radius: 999px;
      margin-bottom: .4rem;
    }}
    .detail h2 {{ margin: 0 0 .35rem; font-family: var(--display); color: var(--primary-dark); }}
    .lead {{ color: var(--muted); margin: .35rem 0 .7rem; max-width: 46rem; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: .35rem; margin-top: .5rem; }}
    .badge {{
      background: rgba(94,56,85,.07); border: 1px solid rgba(94,56,85,.18);
      border-radius: 999px; padding: .22rem .65rem; font-size: .8rem;
    }}
    .badge.muted {{ color: var(--muted); }}
    .file-box {{
      background: var(--bg); border: 1px dashed var(--line); border-radius: 14px;
      padding: .85rem 1rem; min-width: 200px;
    }}
    .file-box span {{ display: block; color: var(--muted); font-size: .78rem; margin-bottom: .2rem; }}
    .panel {{
      background: var(--bg); border: 1px solid var(--line);
      border-radius: 14px; padding: .95rem 1rem; margin-bottom: .85rem;
    }}
    .panel h4 {{ margin: 0 0 .65rem; font-size: .98rem; color: var(--primary-dark); }}
    .tips {{ margin: 0; padding-inline-start: 1.15rem; color: var(--muted); }}
    .tips li {{ margin-bottom: .3rem; }}
    .empty {{ color: var(--muted); margin: 0; }}
    .table-wrap {{ overflow-x: auto; }}
    .type {{
      display: inline-block; background: rgba(94,56,85,.1); color: var(--primary);
      border-radius: 8px; padding: .08rem .4rem; font-size: .78rem;
    }}
    .back-top {{ display: inline-block; margin-top: .35rem; color: var(--primary); font-weight: 600; }}

    .faq details {{
      background: #fff; border: 1px solid var(--line);
      border-radius: 14px; padding: .95rem 1.05rem; margin-bottom: .55rem;
    }}
    .faq summary {{ cursor: pointer; font-weight: 600; color: var(--primary-dark); }}
    .faq p {{ color: var(--muted); margin: .6rem 0 0; }}

    .cta {{
      margin: 1.5rem 0 3.5rem; padding: 2rem;
      border-radius: calc(var(--radius) + 6px);
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: #fff; text-align: center;
    }}
    .cta h2 {{ margin: 0 0 .4rem; font-family: var(--display); color: #fff; }}
    .cta p {{ margin: 0 0 1rem; opacity: .9; }}
    .cta .btn-gold {{ margin: .2rem; }}
    .cta .btn-ghost {{
      background: transparent; color: #fff; border-color: rgba(255,255,255,.35);
    }}
    .cta .contact-row {{ justify-content: center; }}
    .cta .contact-pill {{
      background: rgba(255,255,255,.12); border-color: rgba(255,255,255,.25); color: #fff;
    }}
    .cta .contact-pill:hover {{ background: #fff; color: var(--primary); }}

    footer.site {{
      border-top: 1px solid var(--line); padding: 1.35rem 0 2.2rem; color: var(--muted); font-size: .88rem;
    }}
    footer.site .foot {{
      display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    }}
    .search {{
      width: 100%; max-width: 360px; margin-bottom: .9rem;
      background: #fff; border: 1px solid var(--line); color: var(--text);
      border-radius: 999px; padding: .65rem 1rem; font: inherit;
    }}
    .hidden {{ display: none !important; }}
    .global-cards {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: .9rem;
    }}
    @media (max-width: 800px) {{ .global-cards {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header class="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="#">ثيم {THEME_NAME_AR}</a>
      <nav class="nav-links">
        <a href="#preview">المعاينة</a>
        <a href="#sizes">المقاسات</a>
        <a href="#globals">إعدادات عامة</a>
        <a href="#sections">السكاشن</a>
        <a href="#buy">السعر والتواصل</a>
      </nav>
      <a class="nav-cta" href="{PREVIEW_URL}" target="_blank" rel="noopener">معاينة مباشرة</a>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <div class="eyebrow">مرجع العملاء · ثيم زد · {THEME_NAME_EN}</div>
          <h1>دليل ثيم <em>{THEME_NAME_AR}</em><br/>سكاشن، مقاسات، وإعدادات كاملة</h1>
          <p class="hero-lead">
            مبني من ملفات الثيم + لقطات حقيقية من المعاينة الحية.
            كل سكشن مشروح مع المقاسات وجداول الإعدادات — للهيدر والفوتر والتخطيط أيضاً.
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{PREVIEW_URL}" target="_blank" rel="noopener">فتح المعاينة</a>
            <a class="btn btn-ghost" href="{EDITOR_URL}" target="_blank" rel="noopener">محرر التخصيص</a>
            <a class="btn btn-gold" href="#buy">السعر والتواصل</a>
          </div>
          <div class="price-chip">
            <strong>{escape(THEME_PRICE)}</strong>
            <span class="old-price">{escape(THEME_PRICE_OLD)}</span>
            <span class="note">{escape(THEME_PRICE_NOTE)}</span>
            <span class="help">{escape(THEME_PRICE_HELP)}</span>
          </div>
          <div class="contact-row">
            <a class="contact-pill" href="mailto:{CONTACT_EMAIL}">✉ {CONTACT_EMAIL}</a>
            <a class="contact-pill" href="tel:{CONTACT_PHONE_TEL}">☎ {CONTACT_PHONE}</a>
          </div>
        </div>
        <figure class="hero-visual">
          <img src="assets/preview-hero.png" alt="معاينة ثيم {THEME_NAME_AR} — السلايدر والفئات" />
        </figure>
      </div>
    </section>

    <section class="block" id="preview">
      <div class="wrap">
        <h2>لقطات من المعاينة الحية</h2>
        <p class="sub">صور مأخوذة من متجر التجربة على زد — نفس الثيم اللي يشتغل عند العملاء.</p>
        <div class="preview-grid">
          <figure class="shot">
            <img src="assets/preview-hero.png" alt="الهيدر والسلايدر والفئات" />
            <figcaption>الهيدر + السلايدر الرئيسي + فئات دائرية</figcaption>
          </figure>
          <figure class="shot">
            <img src="assets/preview-products.png" alt="تابات المنتجات" />
            <figcaption>سكشن تابات المنتجات وبطاقة المنتج</figcaption>
          </figure>
          <figure class="shot">
            <img src="assets/preview-before-after.png" alt="قبل وبعد والمجموعات" />
            <figcaption>مقارنة قبل/بعد + بنرات المجموعات</figcaption>
          </figure>
        </div>
        <div class="hero-actions" style="margin-top:1.25rem">
          <a class="btn btn-primary" href="{PREVIEW_URL}" target="_blank" rel="noopener">المعاينة الكاملة</a>
          <a class="btn btn-ghost" href="{EDITOR_URL}" target="_blank" rel="noopener">رابط التخصيص (لوحة زد)</a>
        </div>
      </div>
    </section>

    <section class="block" id="colors">
      <div class="wrap">
        <h2>ألوان الثيم</h2>
        <p class="sub">مستخرجة من المعاينة الحية (<code>--primary-color</code> وغيرها).</p>
        <div class="swatches">
          <div class="swatch"><i style="background:{PRIMARY}"></i><div>أساسي<br/><code>{PRIMARY}</code></div></div>
          <div class="swatch"><i style="background:{PRIMARY_DARK}"></i><div>أساسي غامق<br/><code>{PRIMARY_DARK}</code></div></div>
          <div class="swatch"><i style="background:{PRIMARY_SOFT}"></i><div>أساسي فاتح<br/><code>{PRIMARY_SOFT}</code></div></div>
          <div class="swatch"><i style="background:#ffffff;border:1px solid #ddd"></i><div>خلفية<br/><code>#ffffff</code></div></div>
          <div class="swatch"><i style="background:#363636"></i><div>نص<br/><code>#363636</code></div></div>
          <div class="swatch"><i style="background:{ACCENT_GOLD}"></i><div>لمسة ذهبية<br/><code>{ACCENT_GOLD}</code></div></div>
        </div>
        <div class="stats">
          <div class="stat"><strong>{len(DATA)}</strong><span>سكشن موثّق</span></div>
          <div class="stat"><strong>3</strong><span>هيدر · تخطيط · فوتر</span></div>
          <div class="stat"><strong>RTL</strong><span>عربي بالكامل</span></div>
        </div>
      </div>
    </section>

    <section class="block" id="sizes">
      <div class="wrap">
        <h2>جدول المقاسات السريع</h2>
        <p class="sub">مقاسات من إعدادات الثيم + قياسات الصور الفعلية في المعاينة.</p>
        <table class="sizes-table">
          <thead><tr><th>الموضع</th><th>المقاس الموصى به / الحي</th></tr></thead>
          <tbody>
            <tr><td>شعار الهيدر</td><td><code>180 × 90</code></td></tr>
            <tr><td>سلايدر — جوال / افتراضي</td><td><code>1400 × 600</code></td></tr>
            <tr><td>سلايدر — سطح المكتب</td><td><code>1920 × 800</code> · حي ≈ <code>1900 × 594</code></td></tr>
            <tr><td>بطاقات الفئات</td><td><code>480 × 170</code></td></tr>
            <tr><td>صور المنتجات</td><td><code>1000 × 1000</code> مفضّل</td></tr>
            <tr><td>قبل / بعد</td><td><code>1200 × 500</code></td></tr>
            <tr><td>معرض الصور</td><td><code>750 × 750</code></td></tr>
            <tr><td>أيقونات المميزات / الشركاء</td><td><code>200 × 200</code></td></tr>
            <tr><td>لوجو الفوتر</td><td><code>200 × 200</code></td></tr>
            <tr><td>فيديو</td><td><code>MP4 — أقصى 10MB</code></td></tr>
            <tr><td>ريلز</td><td><code>1080 × 1920 (9:16)</code></td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="block" id="globals">
      <div class="wrap">
        <h2>الإعدادات العامة</h2>
        <p class="sub">هيدر · تخطيط (Layout) · فوتر — تؤثر على كل صفحات المتجر.</p>
        <div class="global-cards">
          <a class="sec-card" href="#global-header">
            <span class="sec-num">01</span>
            <h3>الهيدر</h3>
            <p>شعار، بحث، رأس ثابت، شريط تنبيهات بألوان وتحريك.</p>
          </a>
          <a class="sec-card" href="#global-layout">
            <span class="sec-num">02</span>
            <h3>التخطيط</h3>
            <p>خطوط، ألوان، واتساب، رجوع لأعلى، قائمة سفلية، سلة.</p>
          </a>
          <a class="sec-card" href="#global-footer">
            <span class="sec-num">03</span>
            <h3>الفوتر</h3>
            <p>لوجو، عن المتجر، خدمات، روابط، موقع جغرافي.</p>
          </a>
        </div>
        {HEADER_BLOCK}
        {LAYOUT_BLOCK}
        {FOOTER_BLOCK}
      </div>
    </section>

    <section class="block" id="sections">
      <div class="wrap">
        <h2>سكاشن الثيم</h2>
        <p class="sub">اضغط أي سكشن للتفاصيل. الوسوم «في المعاينة» مربوطة بمحتوى المتجر التجريبي.</p>
        <input class="search" id="search" type="search" placeholder="ابحث باسم السكشن…" />
        <div class="filters" id="filters">{FILTERS}</div>
        <div class="sec-grid" id="cards">{CARDS}</div>
      </div>
    </section>

    <section class="block" id="details">
      <div class="wrap">
        <h2>التفاصيل المرجعية للسكاشن</h2>
        <p class="sub">شرح + مقاسات + جدول إعدادات لكل سكشن.</p>
        {DETAILS}
      </div>
    </section>

    <section class="block faq" id="faq">
      <div class="wrap">
        <h2>أسئلة شائعة</h2>
        <details open>
          <summary>هل المقاس لازم يكون بالبكسل حرفياً؟</summary>
          <p>الأفضل نفس النسبة والمقاس الموصى. صورة أكبر بنفس النسبة غالباً ممتازة.</p>
        </details>
        <details>
          <summary>من وين أخصّص السكاشن؟</summary>
          <p>من <a href="{EDITOR_URL}" target="_blank" rel="noopener">محرر الثيم في لوحة زد</a>، ومعاينة التغييرات من رابط المعاينة.</p>
        </details>
        <details>
          <summary>كيف أتواصل لشراء أو دعم الثيم؟</summary>
          <p>الإيميل <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> أو الهاتف <a href="tel:{CONTACT_PHONE_TEL}">{CONTACT_PHONE}</a>.</p>
        </details>
      </div>
    </section>

    <div class="wrap" id="buy">
      <div class="cta">
        <h2>جاهز تنقل متجرك لمستوى ثيم {THEME_NAME_AR}؟</h2>
        <p><strong>{escape(THEME_PRICE)}</strong> <span style="text-decoration:line-through;opacity:.75">{escape(THEME_PRICE_OLD)}</span> — {escape(THEME_PRICE_NOTE)}</p>
        <p style="opacity:.9;font-size:.95rem;margin:.35rem 0 1rem">{escape(THEME_PRICE_HELP)}</p>
        <a class="btn btn-gold" href="{PREVIEW_URL}" target="_blank" rel="noopener">شاهد المعاينة</a>
        <a class="btn btn-ghost" href="{EDITOR_URL}" target="_blank" rel="noopener">محرر التخصيص</a>
        <div class="contact-row">
          <a class="contact-pill" href="mailto:{CONTACT_EMAIL}">✉ {CONTACT_EMAIL}</a>
          <a class="contact-pill" href="tel:{CONTACT_PHONE_TEL}">☎ {CONTACT_PHONE}</a>
          <a class="contact-pill" href="https://wa.me/201145828786" target="_blank" rel="noopener">واتساب</a>
        </div>
      </div>
    </div>
  </main>

  <footer class="site">
    <div class="wrap foot">
      <div>© 2026 ثيم {THEME_NAME_AR} · Smart Code Crew</div>
      <div>Smart Code Crew</div>
    </div>
  </footer>

  <script>
    const filters = document.getElementById('filters');
    const cards = [...document.querySelectorAll('#cards .sec-card')];
    const details = [...document.querySelectorAll('#details .detail')];
    const search = document.getElementById('search');
    let active = 'all';
    function apply() {{
      const q = (search.value || '').trim();
      cards.forEach(card => {{
        const okCat = active === 'all' || card.dataset.cat === active;
        const okQ = !q || card.innerText.includes(q);
        card.classList.toggle('hidden', !(okCat && okQ));
      }});
      details.forEach(d => {{
        const okCat = active === 'all' || d.dataset.cat === active;
        const okQ = !q || d.innerText.includes(q);
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

out = DOCS / "index.html"
out.write_text(HTML, encoding="utf-8")
print("Wrote", out, "bytes", out.stat().st_size)
print("sections", len(DATA), "layout groups", len(LAYOUT["groups"]), "header groups", len(HEADER["groups"]))

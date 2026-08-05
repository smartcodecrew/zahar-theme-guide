# -*- coding: utf-8 -*-
"""Capture each homepage section from Zahra theme preview."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(r"E:\zahar2\docs\assets\sections")
OUT.mkdir(parents=True, exist_ok=True)

URL = (
    "https://doyftt.dev.zid.store/ar/"
    "?theme=8a4af4f7-7c81-4c0c-a672-82b970f4a2cb"
    "&md_token=Zt4meo486fHGqn7eu0wHjYkp4ToWWuhutsf3wRMpO7y7J6sAzv98K0mVAT7Udbn5"
    "&previewMode=true"
)

# schema-key -> section-id or css
SECTIONS = [
    ("header", "css=header.header-head"),
    ("main-slider", "524bf8c6-4b6d-483a-8d54-44bc916749ed"),
    ("category-products-section", "448f0ea0-da4c-4124-8bec-38a86d5c94b8"),
    ("promo-samples-banner", "a8c205cd-ce6c-47b3-921e-92818f665d9b"),
    ("category-section", "99efb815-5d54-4c3a-8885-c47509511a67"),
    ("products-tabs-section", "e52ee2c2-950c-4b2c-965d-ba16345dc864"),
    ("collection-section", "464f44bb-0896-461f-9b7f-2df6782ee778"),
    ("diffrent-collction", "7826f4bd-912c-4a78-b199-f4d4642bbbaa"),
    ("image-tabs-slider", "22a4e5fd-9403-47e3-8bf8-b9b55d9bd89c"),
    ("before-after-section", "ff1296e3-380a-45a5-9cc6-690b70d46c77"),
    ("features-section", "3bdf39ec-2dd3-4ff3-9ba4-01755e0864c1"),
    ("video", "cba410e3-c504-45b1-9603-9d7974a7e462"),
    ("exploere-collections", "a43270c5-af21-465a-8f2d-4864afb7fc81"),
    ("why_choose_us", "e1b78bf1-d1b2-41ef-843d-f2ed11564f61"),
    ("products-showcase-slider", "9e80c53f-31b8-42e2-ab8f-5c8874cd4ed0"),
    ("partners", "6f074a93-16ac-478e-9aa6-edf63e6df008"),
    ("products-section", "5ebf70e9-018a-44f5-8574-e7bf98c5fadc"),
    ("faq-section", "6b9cccc7-4887-4970-ba78-9c1689ef5d30"),
    ("testimonials", "626ba956-8d86-4028-83f7-8af369a2d561"),
    ("blog-section", "35949c2b-81c2-49a6-8f2e-fe98b38f7bfc"),
    ("footer", "css=footer"),
]


HIDE_UI_JS = r"""
() => {
  // Close sliding side menu if API exists
  try {
    if (window.slidingMenu && typeof window.slidingMenu.close === 'function') {
      window.slidingMenu.close();
    }
  } catch (e) {}
  try {
    if (typeof closeSlidingMenu === 'function') closeSlidingMenu();
  } catch (e) {}
  try {
    if (typeof closeSearchBox === 'function') closeSearchBox();
  } catch (e) {}

  const hide = (el) => {
    if (!el) return;
    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
    el.style.setProperty('pointer-events', 'none', 'important');
    el.setAttribute('aria-hidden', 'true');
    el.classList.remove('active', 'open', 'show', 'is-open', 'sm-open');
  };

  [
    '#sliding-menu',
    '#sidenav-overlay',
    '.slide-menu',
    '.sliding-menu',
    '[class*="slide-menu"]',
    '.sub-menu-block',
    '.dropdown-menu.show',
    '.sm-search-div',
    '.sm-search-div.show',
    '.sm-search-div.active',
    '.search-down-div',
    '.autocomplete-items',
  ].forEach((sel) => document.querySelectorAll(sel).forEach(hide));

  // Clear hover states that keep mega-menu open
  document.querySelectorAll('.top-level-link, .main-nav > li').forEach((el) => {
    el.classList.remove('hover', 'open', 'active', 'show');
  });

  // Force animations visible + unstick header
  document.querySelectorAll('.scroll-animate').forEach((el) => {
    el.classList.add('animated', 'in-view', 'visible');
    el.style.opacity = '1';
    el.style.transform = 'none';
    el.style.visibility = 'visible';
  });
  const h = document.querySelector('header.header-head');
  if (h) {
    h.style.setProperty('position', 'relative', 'important');
    h.style.setProperty('top', '0', 'important');
  }
  document
    .querySelectorAll('[class*="whatsapp"], .back-to-top, #backToTop, .floating-whatsapp')
    .forEach(hide);
}
"""


async def hide_overlays(page):
    await page.mouse.move(0, 0)
    await page.keyboard.press("Escape")
    await page.evaluate(HIDE_UI_JS)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=1)
        print("goto…")
        await page.goto(URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_timeout(2500)
        await hide_overlays(page)
        await page.wait_for_timeout(500)

        # Verify menu is gone
        menu_state = await page.evaluate(
            """() => {
            const m = document.getElementById('sliding-menu');
            if (!m) return {missing:true};
            const r = m.getBoundingClientRect();
            const s = getComputedStyle(m);
            return {display:s.display, visibility:s.visibility, w:Math.round(r.width), h:Math.round(r.height), x:Math.round(r.left)};
        }"""
        )
        print("menu_state", menu_state)

        for key, target in SECTIONS:
            if target.startswith("css="):
                sel = target[4:]
            else:
                sel = f'[section-id="{target}"]'
            loc = page.locator(sel).first
            try:
                await hide_overlays(page)
                await loc.scroll_into_view_if_needed(timeout=15000)
                await page.wait_for_timeout(350)
                # Only unhide scroll-animate within the target — never force-show overlays
                await page.evaluate(
                    """(sel) => {
                    const el = document.querySelector(sel);
                    if (!el) return;
                    el.querySelectorAll('.scroll-animate').forEach(n => {
                      n.style.opacity='1';
                      n.style.visibility='visible';
                      n.style.transform='none';
                    });
                }""",
                    sel,
                )
                await hide_overlays(page)
                await page.wait_for_timeout(200)
                box = await loc.bounding_box()
                if not box or box["height"] < 30:
                    print(f"SKIP {key} height={box}")
                    continue
                out = OUT / f"{key}.png"
                await loc.screenshot(path=str(out), timeout=60000)
                size = out.stat().st_size
                print(f"OK {key} {int(box['width'])}x{int(box['height'])} -> {size} bytes")
            except Exception as e:
                print(f"FAIL {key}: {e}")

        # Overview viewport shots for hero gallery (menu closed)
        await hide_overlays(page)
        await page.evaluate("window.scrollTo(0,0)")
        await page.wait_for_timeout(400)
        await hide_overlays(page)
        overview = OUT.parent
        await page.screenshot(path=str(overview / "preview-hero.png"), full_page=False)

        # products tabs area
        await page.locator('[section-id="e52ee2c2-950c-4b2c-965d-ba16345dc864"]').first.scroll_into_view_if_needed()
        await hide_overlays(page)
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(overview / "preview-products.png"), full_page=False)

        # before-after area
        await page.locator('[section-id="ff1296e3-380a-45a5-9cc6-690b70d46c77"]').first.scroll_into_view_if_needed()
        await hide_overlays(page)
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(overview / "preview-before-after.png"), full_page=False)
        print("overview shots refreshed")

        optional = [
            ("ticker", ".ticker-section, [class*='ticker']"),
            ("reels-section", ".reels-section, [class*='reels-section']"),
            ("ggallery", ".ggallery, [class*='gallery-section']"),
        ]
        for key, sel in optional:
            loc = page.locator(sel).first
            try:
                if await loc.count() == 0:
                    print(f"MISS {key}")
                    continue
                await hide_overlays(page)
                await loc.scroll_into_view_if_needed(timeout=5000)
                await hide_overlays(page)
                await page.wait_for_timeout(300)
                out = OUT / f"{key}.png"
                await loc.screenshot(path=str(out), timeout=30000)
                print(f"OK {key} -> {out.stat().st_size}")
            except Exception as e:
                print(f"MISS {key}: {e}")

        await browser.close()
        print("done")


if __name__ == "__main__":
    asyncio.run(main())

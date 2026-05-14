"""Render CI page in browser, dump the filings region's rendered HTML + screenshot."""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
PROFILE_DIR = ROOT / "playwright-profile"


async def main(ticker: str):
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto(f"https://www.canadianinsider.com/company?ticker={ticker}", wait_until="domcontentloaded", timeout=30000)
        # Wait for filings AJAX to populate
        try:
            await page.wait_for_function(
                """() => {
                    const heads = Array.from(document.querySelectorAll('div, h1, h2, h3, h4, h5'));
                    const target = heads.find(el => /Latest \\d+ SEDI filings/i.test(el.textContent || ''));
                    if (!target) return false;
                    const container = target.closest('div').parentElement;
                    return /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?\\s+\\d{1,2},?\\s+\\d{4}/i.test(container.textContent || '');
                }""",
                timeout=20000,
            )
        except Exception as e:
            print(f"wait_for_function failed: {e}")
        await asyncio.sleep(2)

        await page.screenshot(path=str(ROOT / "ci_rendered.png"), full_page=True)

        info = await page.evaluate("""() => {
            const heads = Array.from(document.querySelectorAll('div, h1, h2, h3, h4, h5'));
            const target = heads.find(el => /Latest \\d+ SEDI filings/i.test(el.textContent || ''));
            if (!target) return {found: false};
            // Walk up to find the smallest container that holds dates
            let container = target;
            for (let i = 0; i < 8; i++) {
                if (container.parentElement &&
                    /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\.?\\s+\\d{1,2},?\\s+\\d{4}/i.test(container.parentElement.textContent || '')) {
                    container = container.parentElement;
                } else break;
            }
            return {
                found: true,
                container_html: container.outerHTML.slice(0, 6000),
                container_text: container.textContent.slice(0, 2000),
            };
        }""")

        print(f"found: {info.get('found')}")
        if info.get("found"):
            print("=== CONTAINER TEXT (first 2000 chars) ===")
            print(info["container_text"])
            print()
            print("=== CONTAINER HTML (first 6000 chars) ===")
            print(info["container_html"])

        await asyncio.sleep(2)
        await ctx.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "AMX"))

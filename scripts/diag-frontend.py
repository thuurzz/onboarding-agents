from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    console_msgs = []
    page_errors = []
    page.on("console", lambda m: console_msgs.append(f"{m.type}: {m.text}"))
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    page.goto("http://192.168.1.13:3005", wait_until="networkidle")
    page.wait_for_timeout(1500)

    print("=== CONSOLE ===")
    for m in console_msgs:
        print(m)
    print("=== PAGE ERRORS ===")
    for e in page_errors:
        print(e)

    # Tenta digitar e ver o valor + estado
    page.fill("textarea", "teste hydration")
    page.wait_for_timeout(500)
    val = page.eval_on_selector("textarea", "t => t.value")
    print("=== textarea value após fill:", repr(val), "===")

    browser.close()

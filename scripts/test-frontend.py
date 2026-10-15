from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://192.168.1.13:3005", wait_until="networkidle")

    # 1. Verifica estado inicial
    title = page.inner_text("h1")
    print("TITLE:", title)

    # 2. Digita no textarea como usuário real (dispara onChange do React)
    page.fill("textarea", "quero acesso ao litellm")

    # 3. Verifica se o botão Enviar habilita
    btn = page.locator("button", has_text="Enviar")
    print("BOTÃO ENVIAR disabled após digitar:", btn.is_disabled())

    # 4. Clica e aguarda a resposta
    btn.click()
    page.wait_for_timeout(3000)

    body = page.inner_text("body")
    print("=== CONTEÚDO APÓS ENVIAR ===")
    print(body[:1200])

    browser.close()

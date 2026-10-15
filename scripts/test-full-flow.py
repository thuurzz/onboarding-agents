from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://192.168.1.13:3006", wait_until="networkidle")

    # Turno 1: classifica plataforma
    page.fill("textarea", "quero acesso ao langfuse")
    page.locator("button", has_text="Enviar").click()
    page.wait_for_timeout(2500)
    print("=== TURNO 1 (resposta do agente) ===")
    print(page.inner_text("body")[-400:])

    # Turno 2: completa campos
    page.fill("textarea", "nome_coordenacao: Coord RH, centro_custo: 987654321, matricula_responsavel: 0123456789, nome_projeto: projeto-rh, ambiente: staging, limite_trace_mensal: 50000")
    page.locator("button", has_text="Enviar").click()
    page.wait_for_timeout(2500)
    print("=== TURNO 2 (ticket criado?) ===")
    body = page.inner_text("body")
    print(body[-600:])

    # Aba Tickets
    page.locator("button", has_text="Tickets").click()
    page.wait_for_timeout(1500)
    print("=== ABA TICKETS ===")
    print(page.inner_text("body")[-600:])

    browser.close()

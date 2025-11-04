from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# -------------------------------
# Setup browser
# -------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 25)

url_base = "https://www.bkt-tires.com/es/es/agricultura?viewAll=1"
driver.get(url_base)

# -------------------------------
# Get categories
# -------------------------------
print("🔎 Buscando categorías...")

wait.until(EC.presence_of_all_elements_located((By.XPATH, "//strong[contains(@class,'-t-title-4')]")))
strongs = driver.find_elements(By.XPATH, "//strong[contains(@class,'-t-title-4')]")

categorias = []
vistos = set()

for s in strongs:
    nombre = (s.text or "").strip()
    if not nombre:
        continue

    href = None
    for xpath in [
        "following-sibling::a[@href][1]",
        "ancestor::*[self::div or self::section][contains(@class,'bkt')][1]//a[@href]",
        "following::a[@href][1]",
    ]:
        try:
            a = s.find_element(By.XPATH, xpath)
            href = a.get_attribute("href")
            if href:
                break
        except:
            pass

    if href and href not in vistos:
        categorias.append((nombre, href))
        vistos.add(href)

print(f"✅ {len(categorias)} categorías detectadas")

def obtener_modelos_en_pagina(driver, wait, max_scrolls=25):
    enlaces_previos = set()
    scrolls = 0

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.bkt-c-product")))
    except:
        print("⚠️ No se encontró ningún producto")
        return []

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        cards = driver.find_elements(By.CSS_SELECTOR, "a.bkt-c-product")
        enlaces = {c.get_attribute("href") for c in cards if c.get_attribute("href")}
        if len(enlaces) == len(enlaces_previos):
            break
        enlaces_previos = enlaces
        scrolls += 1

    return list(enlaces_previos)

# -------------------------------
# Search through categories and tyres
# -------------------------------
resultados = []
for categoria, link in categorias:
    print(f"\n🚜 Procesando categoría: {categoria}")
    driver.get(link)

    modelo_links = obtener_modelos_en_pagina(driver, wait)
    if not modelo_links:
        print(f"   ⚠️ No se encontraron neumáticos para {categoria}")
        continue

    print(f"   🔹 {len(modelo_links)} neumáticos encontrados")

    for modelo_link in modelo_links:
        try:
            driver.get(modelo_link)

            # Esperar solo el título del modelo
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
            time.sleep(1.5)

            # ---- Modelo ----
            try:
                modelo = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
            except:
                modelo = ""

            # ---- Línea ----
            try:
                linea_elem = driver.find_element(By.CSS_SELECTOR, "strong.bkt-pdp__subtitle.-t-title-5")
                linea_texto = linea_elem.text.strip()
                try:
                    span_text = linea_elem.find_element(By.TAG_NAME, "span").text.strip()
                    linea = f"{linea_texto} {span_text}".strip()
                except:
                    linea = linea_texto
            except:
                linea = ""

            # ---- Construcción ----
            try:
                construccion_ul = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'bkt-pdp__feature-title')][contains(.,'Construction')]/following-sibling::ul"
                )
                construccion = " ".join([li.text.strip() for li in construccion_ul.find_elements(By.TAG_NAME, "li")])
            except:
                construccion = ""

            # ---- Vehículos ----
            try:
                vehiculos_ul = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'bkt-pdp__feature-title')][contains(.,'Maquinarias')]/following-sibling::ul"
                )
                vehiculos = ", ".join([li.text.strip() for li in vehiculos_ul.find_elements(By.TAG_NAME, "li")])
            except:
                vehiculos = ""

            # ---- Usos ----
            try:
                usos_ul = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'bkt-pdp__feature-title')][contains(.,'Aplicaciones')]/following-sibling::ul"
                )
                usos = ", ".join([li.text.strip() for li in usos_ul.find_elements(By.TAG_NAME, "li")])
            except:
                usos = ""

            resultados.append({
                "Categoría": categoria,
                "Modelo": modelo,
                "Línea": linea,
                "Construcción": construccion,
                "Vehículos": vehiculos,
                "Usos": usos,
                "URL": modelo_link
            })

            print(f"      ✔ {modelo}")

        except Exception as e:
            print(f"      ❌ Error en {modelo_link}: {e}")
            continue

# Save CSV
df = pd.DataFrame(resultados)
df.to_csv("bkt_neumaticos_agricola.csv", index=False, encoding="utf-8-sig")

driver.quit()
print("\n✅ Scraping completado. Archivo guardado: bkt_neumaticos_agricola.csv")
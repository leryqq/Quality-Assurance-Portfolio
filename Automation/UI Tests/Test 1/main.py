from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from typing import List
import time
import re


# ---------- КЛАСС ДАННЫХ ----------
class CalendarEvent:
    def __init__(self, calendarId: str, start: str, end: str, id: str,
                 location: str, people: List[str], title: str):
        self.calendarId = calendarId
        self.start = datetime.fromisoformat(start.replace("Z", "+00:00"))
        self.end = datetime.fromisoformat(end.replace("Z", "+00:00"))
        self.id = id
        self.location = location
        self.people = people
        self.title = title


# ---------- НАСТРОЙКА ДАННЫХ ----------
'''
Необходимые данные:
 * start, end (в таймзоне сервера)
 * provider (в формате Provider - First Name Second Name, PMHNP)
'''
data = {
    "calendarId": "1-c",
    "start": "2026-02-04T09:20:00.000Z",
    "end": "2026-02-04T09:40:00.000Z",
    "id": "3867",
    "location": "Video",
    "people": [
        "Patient - Testing Childtwentynine",
        "Provider - Test Provider, PMHNP"
    ],
    "title": "Testing Childtwentynine"
}

booked_event = CalendarEvent(**data)
print(f"Title: '{booked_event.title}'")
print(f"Start: '{booked_event.start}' End: '{booked_event.end}'")
print(f"People: '{booked_event.people}'")


# ---------- НАСТРОЙКА БРАУЗЕРА ----------
chrome_options = Options()
chrome_options.add_argument("--headless")              # запуск без GUI
chrome_options.add_argument("--window-size=1920,1080") # чтобы страница выглядела как при нормальном окне

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 20)


# ---------- СИСТЕМА СТАТУСОВ ----------
status_log = {}
def set_status(step_name, success, message=""):
    status_log[step_name] = {"result": "✅ Успех" if success else "❌ Неудача", "details": message}
    print(f"\n--- {step_name}: {'✅' if success else '❌'} {message} ---\n")


# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------

def wait_and_click(driver, selector, timeout=10, description="элемент"):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        element.click()
        #print(f"✅ Клик по {description}")
        return True
    except TimeoutException:
        print(f"❌ {description} не появился за {timeout} сек.")
    except ElementClickInterceptedException:
        print(f"⚠️ {description} найден, но перекрыт другим элементом.")
    return False


def select_provider(driver, provider_name):
    try:
        old_count = len(driver.find_elements(By.CSS_SELECTOR, ".fc-timegrid-event-harness"))
        provider_select = Select(driver.find_element(By.CSS_SELECTOR, ".bubble-element.Dropdown.dropdown-chevron"))
        current = provider_select.first_selected_option.text.strip()

        if current != provider_name:
            #print(f"🔁 Выбираем провайдера: {provider_name}")
            provider_select.select_by_visible_text(provider_name)
            WebDriverWait(driver, 60).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".fc-timegrid-event-harness")) != old_count
            )
        #else:
            #print(f"✅ Провайдер уже выбран: {provider_name}")

        set_status("Выбор провайдера", True, f"Провайдер: {provider_name}")
        return True
    except Exception as e:
        set_status("Выбор провайдера", False, str(e))
        return False


def go_to_date(driver, target_date, max_attempts=40):
    try:
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()

        for attempt in range(max_attempts):
            date_columns = driver.find_elements(By.CSS_SELECTOR, "[data-date]")
            visible_dates = sorted(
                [datetime.strptime(c.get_attribute("data-date"), "%Y-%m-%d").date() for c in date_columns]
            )
            first_date, last_date = visible_dates[0], visible_dates[-1]
            #print(f"📅 Видимый диапазон: {first_date} → {last_date}")

            if first_date <= target_date <= last_date:
                #print(f"✅ Дата {target_date} видна.")
                set_status("Переход к дате", True, f"Дата {target_date}")
                return True
            elif target_date < first_date:
                wait_and_click(driver, "button.fc-prev-button", description="Prev")
            else:
                wait_and_click(driver, "button.fc-next-button", description="Next")

            time.sleep(0.3)

        set_status("Переход к дате", False, f"Не удалось найти {target_date}")
        return False
    except Exception as e:
        set_status("Переход к дате", False, str(e))
        return False


def find_and_click_event(driver, booked_event):
    try:
        target_date = booked_event.start.date().isoformat()
        columns = driver.find_elements(By.CSS_SELECTOR, "[data-date]")

        for col in columns:
            col_date = col.get_attribute("data-date")
            if col_date != target_date:
                continue

            #print(f"🎯 Обрабатываем дату {col_date}")
            events = col.find_elements(By.CSS_SELECTOR, "a.fc-timegrid-event")

            for event in events:
                try:
                    time_el = event.find_element(By.CSS_SELECTOR, ".fc-event-time")
                    title_el = event.find_element(By.CSS_SELECTOR, ".fc-event-title")
                    times = re.findall(r"\d{1,2}:\d{2}", time_el.text.strip())
                    if len(times) < 2:
                        continue

                    event_start, event_end = map(lambda t: datetime.strptime(t, "%H:%M").time(), times[:2])
                    title_text = title_el.text.strip()
                    #print(f"🕓 {title_text}: {event_start}–{event_end}")

                    if (event_start == booked_event.start.time() and
                        event_end == booked_event.end.time()):
                        print(f"✅ Найдено совпадение для {title_text} ({col_date})")
                        event.click()

                        if wait_and_click(driver, ".bubble-element.Text.cmoqr0", description="кнопка Block"):
                            WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, ".bubble-element.Popup.cmosaV0"))
                            )
                            wait_and_click(driver, ".clickable-element.bubble-element.Button.cmosd0",
                                           description="кнопка 'Yes'")
                            WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, ".bubble-element.Text.cmouaK0"))
                            )
                            set_status("Подтверждение ивента", True, "Ивент успешно заблокирован")
                            return True
                except StaleElementReferenceException:
                    continue
        set_status("Подтверждение ивента", False, "Не найдено нужное событие")
        return False
    except Exception as e:
        set_status("Подтверждение ивента", False, str(e))
        return False


# ---------- ОСНОВНОЙ ПРОЦЕСС ----------

try:
    driver.get("https://my.example.com/")
    WebDriverWait(driver, 15).until(lambda d: "login.example.com" in d.current_url)
    set_status("Открытие сайта", True)
except Exception as e:
    set_status("Открытие сайта", False, str(e))

try:
    driver.find_element(By.CSS_SELECTOR, ".input.cc3305b2a.cf567b0e0").send_keys("login")
    driver.find_element(By.CSS_SELECTOR, ".input.cc3305b2a.c4d148681").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, ".c64f86813.cec2941d2.c6c4189b0.c9177de29.c6048fd88").click()
    WebDriverWait(driver, 15).until(lambda d: "agenda" in d.current_url)
    set_status("Логин", True)
except Exception as e:
    set_status("Логин", False, str(e))

try:
    driver.get("https://my.example.com/admin?tab=calendar&preloader=")
    WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".fc-view-harness.fc-view-harness-active")))
    set_status("Переход в админ", True)
except Exception as e:
    set_status("Переход в админ", False, str(e))

provider_name = next(p.replace("Provider - ", "") for p in booked_event.people if p.startswith("Provider - "))
select_provider(driver, provider_name)
go_to_date(driver, booked_event.start.date())
find_and_click_event(driver, booked_event)

# ---------- ИТОГ ----------
print("\n==============================")
print("📊 Итог выполнения:")
for step, info in status_log.items():
    print(f"{step}: {info['result']} — {info['details']}")
print("==============================")

if all(info["result"] == "✅ Успех" for info in status_log.values()):
    print("🎉 ОБЩИЙ РЕЗУЛЬТАТ: ✅ УСПЕХ")
else:
    print("💥 ОБЩИЙ РЕЗУЛЬТАТ: ❌ НЕУДАЧА")

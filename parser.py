import os
import re
from collections import Counter
import requests
import urllib3

# Отключаем предупреждения SSL в консоли
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def extract_ips(file_path):
    """Ищет все IPv4 в файле."""
    ip_pattern = re.compile(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    )
    ip_list = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                found_ips = ip_pattern.findall(line)
                ip_list.extend(found_ips)
    except FileNotFoundError:
        print(f"[-] Ошибка: Файл логов '{file_path}' не найден.")
    return ip_list


def get_ip_geo(ip):
    """Определяет страну по IP в ОНЛАЙН режиме через надежное API ipinfo.io."""
    if ip.startswith(("127.", "192.168.", "10.", "172.16.")):
        return "Internal Network"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # Переключились на HTTPS эндпоинт ipinfo.io (он намного стабильнее)
        response = requests.get(
            f"https://ipinfo.io/{ip}/json", headers=headers, timeout=5, verify=False
        )

        if response.status_code == 200:
            data = response.json()
            # ipinfo возвращает код страны (например, 'US', 'RU'), преобразуем в читаемый вид
            return data.get("country", "Unknown")
        else:
            return f"Http Status {response.status_code}"

    except Exception as e:
        # Показываем реальный тип ошибки для точной диагностики
        return f"Debug Error: {type(e).__name__} -> {e}"


def analyze_logs(file_path, top_n=5):
    """Главная функция аналитики."""
    ips = extract_ips(file_path)

    if not ips:
        print("[-] IP-адреса для анализа не найдены.")
        return

    print(f"[+] Всего найдено IP-адресов в логе: {len(ips)}")
    print(f"[+] Уникальных адресов: {len(set(ips))}\n")

    ip_counts = Counter(ips)
    print(f"ТОП-{top_n} самых активных IP-адресов:")
    print("-" * 50)

    for ip, count in ip_counts.most_common(top_n):
        country = get_ip_geo(ip)
        print(f"IP: {ip:<15} | Запросов: {count:<5} | Страна: {country}")


def generate_html_report(ip_counts, file_path="cyber_report.html"):
    """Создает HTML-отчет с результатами онлайн-анализа."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ИБ Аналитика Логов (Онлайн)</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 40px; }
            h2 { color: #2c3e50; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #2980b9; color: white; }
            tr:hover { background-color: #f5f5f5; }
            .badge { background: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        </style>
    </head>
    <body>
        <h2> Отчет по онлайн-анализу активности IP</h2>
        <p>Данные получены в реальном времени через IPInfo API.</p>
        <table>
            <tr>
                <th>IP-Адрес</th>
                <th>Количество запросов</th>
                <th>Страна происхождения</th>
            </tr>
    """

    for ip, count in ip_counts.most_common(10):
        country = get_ip_geo(ip)
        html_content += f"""
            <tr>
                <td><strong>{ip}</strong></td>
                <td><span class="badge">{count}</span></td>
                <td>{country}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\n[+] Отчет успешно сохранен в файл: {file_path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_to_read = os.path.join(script_dir, "log.txt")

    ips = extract_ips(file_to_read)
    ip_counts = Counter(ips)

    analyze_logs(file_to_read, top_n=5)

    if ips:
        generate_html_report(ip_counts, os.path.join(script_dir, "cyber_report.html"))

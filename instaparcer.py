import instaloader
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Настройка Instaloader
L = instaloader.Instaloader()

# L.login('your_username', 'your_password')

def get_instagram_data(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        data = {
            "Имя": profile.full_name,
            "Подписчики": profile.followers,
            "Постов": profile.mediacount,
            "Рилсов": sum(1 for post in profile.get_posts() if post.is_video),
            "Описание": profile.biography,
            "Просмотры рилсов": sum(post.video_view_count for post in profile.get_posts() if post.is_video),
            "Просмотры постов": sum(post.video_view_count for post in profile.get_posts() if not post.is_video),
        }
        return data
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None
# Настройка Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # JSON-файл с ключами API

def update_google_sheets(sheet_name, username):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1
    
    data = get_instagram_data(username)
    if not data:
        return
    
    # Записываем данные в Google Sheets
    values = [data["Имя"], data["Подписчики"], data["Постов"], data["Рилсов"], data["Просмотры рилсов"], data["Просмотры постов"], data["Описание"]]
    sheet.append_row(values)
    print("Данные обновлены в Google Sheets")

# Пример использования
if __name__ == "__main__":
    update_google_sheets("Instagram Stats", "instagram_username")
    print("Скрипт завершен")

import asyncio
from google.oauth2.service_account import Credentials
import gspread

async def update_image_sizes(sheet_id, url_to_size_map):
    creds = Credentials.from_service_account_file('credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)

    # Отримання діапазону URL для порівняння
    urls_cells = worksheet.range(f'A2:A{1 + len(url_to_size_map)}')
    urls = [cell.value for cell in urls_cells]

    # Підготовка оновлень
    updates = []
    for i, cell in enumerate(urls_cells, start=2):
        url = cell.value
        size = url_to_size_map.get(url, "Not found")
        updates.append({'range': f'B{i}', 'values': [[size]]})

    # Виконання оновлень
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: worksheet.batch_update(updates))

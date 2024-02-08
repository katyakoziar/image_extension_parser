import asyncio
from google.oauth2.service_account import Credentials
import gspread
from concurrent.futures import ThreadPoolExecutor

async def update_image_sizes(sheet_id, image_sizes):
    creds = Credentials.from_service_account_file('credentials.json',
                    scopes=['https://www.googleapis.com/auth/spreadsheets',
                            'https://www.googleapis.com/auth/drive'])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)

    loop = asyncio.get_running_loop()

    async def update_cell(index, size):
        with ThreadPoolExecutor() as pool:
            if size is not None:
                await loop.run_in_executor(pool, worksheet.update_cell, index, 2, size)
            else:
                await loop.run_in_executor(pool, worksheet.update_cell, index, 2, "Not found")

    count = 0
    tasks = []
    for index, size in enumerate(image_sizes, start=2):
        tasks.append(update_cell(index, size))
        count += 1
        if count % 500 == 0:
            await asyncio.gather(*tasks)
            tasks = []
            await asyncio.sleep(100)

    if tasks:
        await asyncio.gather(*tasks)

import aiohttp
from PIL import Image
from io import BytesIO
import asyncio

async def get_image_size(url, session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                img = Image.open(BytesIO(content))
                return f"{img.width}x{img.height}"
            else:
                print(f"Не вдалося завантажити зображення {url}: Статус-код {response.status}")
                return None
    except Exception as e:
        print(f"Не вдалося отримати розмір для {url}: {e}")
        return None

async def fetch_all_images(image_urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in image_urls:
            if url not in [None, 'nan', '']:
                task = asyncio.create_task(get_image_size(url, session))
                tasks.append(task)
        return await asyncio.gather(*tasks)

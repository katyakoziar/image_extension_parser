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
                return url, f"{img.width}x{img.height}"
            else:
                print(f"Не вдалося завантажити зображення {url}: Статус-код {response.status}")
                return url, None
    except Exception as e:
        print(f"Не вдалося отримати розмір для {url}: {e}")
        return url, None


async def fetch_all_images(image_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(get_image_size(url, session))
            for url in image_urls if url not in [None, 'nan', '']
        ]
        results = await asyncio.gather(*tasks)
        return {url: size for url, size in results if url}

import asyncio
from read_data import get_image_urls
from image_parser import fetch_all_images
from write_data import update_image_sizes

sheet_id = '1TdRPOjLB0s5GZh_KIlwNe-ZhJMBvgV0i26KdsTVRBEs'


async def main():
    image_urls = await get_image_urls()
    image_sizes = await fetch_all_images(image_urls)
    await update_image_sizes(sheet_id, image_sizes)

if __name__ == '__main__':
    asyncio.run(main())

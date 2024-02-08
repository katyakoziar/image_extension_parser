import aiohttp


sheet_id = '1TdRPOjLB0s5GZh_KIlwNe-ZhJMBvgV0i26KdsTVRBEs'
sheet_name = 'feed'
api_key = 'AIzaSyDKlIkwmn-rHuNw41M41Flw-o0-XP54YPs'
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_name}?key={api_key}'

async def get_image_urls():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return [row[0] for row in data['values'] if row]


import aiohttp
import aiofiles
import asyncio
import yadisk
from params import token

FOLDER_NAME = 'download'


async def download_file(url, file_name):
    try:
        print(f'Начато скачивание файла: {file_name}')
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, ssl=False)
            image = await response.read()

        async with aiofiles.open(f"{FOLDER_NAME}/{file_name}", 'wb') as file:
            await file.write(image)
        print(f'Скачен файл: {file_name}')
    except Exception as ex:
        print(ex)


async def download_files():
    yandex = yadisk.YaDisk(token=token)

    tasks = []
    for file in yandex.listdir('/Task3/'):
        file_name = file['name']
        link = yandex.get_download_link(f'/Task3/{file_name}')
        tasks.append(download_file(link, file_name))

    await asyncio.gather(*tasks)


def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(download_files())


if __name__ == '__main__':
    main()

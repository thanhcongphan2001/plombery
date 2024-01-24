import httpx
from apscheduler.triggers.interval import IntervalTrigger
from plombery import task, get_logger, Trigger, register_pipeline
from datetime import datetime
from telegram import Bot

bot_token = "6780230286:AAFamzsqOBq80Ze9cDb1mRiCZGldedBUyhw"
chat_id = "@gis_bot_group"
bot = Bot(token=bot_token)
project = "default"
spider = "vietmap"
prov_code = "52,74,70,60,96,66,11,75"
limit = 5000000
concurrent=8
username =  "congplombery.pt"
start_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
result =[]

@task
async def fetch_raw_sales_data(): 
    logger = get_logger()
    logger.debug("Fetching Vietmap data from the API...")

    api_url = "https://scrapyd.laragis.vn/daemonstatus.json"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
        except httpx.TimeoutException:
            logger.error(f"Error api https://scrapyd.laragis.vn/daemonstatus.json")
            return []

    if response.status_code == 200:
        data = response.json()
       
        if data['running'] == 0:
            logger.info("Fetched Vietmap data from the API")
            result = httpx.post(
                "https://scrapyd.laragis.vn/schedule.json",
                data = {
                    "project": project,
                    "spider": spider,
                    "prov_code": prov_code,
                    "limit": limit,
                    "username": username,
                    "setting": [
                        f"CONCURRENT_REQUESTS={concurrent}",
                        f"CONCURRENT_REQUESTS_PER_DOMAIN={concurrent}",
                    ],
                },
            )

            message = (
                f"*{username}* runned *{spider.upper()}* for province *{prov_code}*\n"
                f"Start time: *{start_time}*\n"
                f"Concurrent: {concurrent}\n"
            )
            
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="markdown") # type: ignore

            return result
        else :
            logger.info("Crawl vietmap is running")
            result = []

    else:
        logger.error(f"Failed to fetch Vietmap data. Status code: {response.status_code}")
        result = []

    return result



register_pipeline(
    id="Vietmap",
    description="Crawl data of provinces and cities in Vietnam using Vietmap provider",
    tasks=[fetch_raw_sales_data],
    triggers=[
        Trigger(
            id="every hour",
            name="every hour",
            description="Run the vietmap every hour",
            schedule=IntervalTrigger(seconds=1800),
        ),
    ],
)



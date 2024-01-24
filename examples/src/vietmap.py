import httpx
from apscheduler.triggers.interval import IntervalTrigger
from plombery import task, get_logger, Trigger, register_pipeline


@task
async def fetch_raw_sales_data():

    logger = get_logger()

    logger.debug("Fetching sales data from the API...")

    api_url = "https://scrapyd.laragis.vn/daemonstatus.json"
    result =[]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
        except httpx.TimeoutException:
            logger.error(f"Error api https://scrapyd.laragis.vn/daemonstatus.json")
            return []

    if response.status_code == 200:
        data = response.json()

        if data['running'] == 0:
            logger.info("Fetched real sales data from the API")
            result = httpx.post(
                "https://scrapyd.laragis.vn/schedule.json",
                data = {
                    "project": 'default',
                    "spider": 'vietmap',
                    "prov_code": '51',
                    "limit": 1,
                    "username": 'congplombery.pt',
                    "setting": [
                        f"CONCURRENT_REQUESTS=8",
                        f"CONCURRENT_REQUESTS_PER_DOMAIN=8",
                    ],
                },
            )
            return result
        else :
            logger.info("Crawl vietmap is running")
            result = []

    else:
        logger.error(f"Failed to fetch sales data. Status code: {response.status_code}")
        result = []

    # Return the results of your task to have it stored
    # and accessible on the web UI
    return result

register_pipeline(
    id="Vietmap",
    description="Aggregate sales activity from all stores across the country",
    tasks=[fetch_raw_sales_data],
    triggers=[
        Trigger(
            id="every hour",
            name="every hour",
            description="Run the vietmap every hour",
            schedule=IntervalTrigger(seconds=3600),
        ),
    ],
)



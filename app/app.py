from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from config.config import settings
import logging

from fastapi.templating import Jinja2Templates
from tasks.celery_worker import task_scrapers, task_parsers
from service.statistic_service import ScraperAnalytics, ParserAnalytics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/status")
def get_status():
    return {"status": "OK"}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    scraper_analytics, parser_analytics = ScraperAnalytics(), ParserAnalytics()

    context = {
        "request": request,

        "scraper_avg_pages_per_scraper": scraper_analytics.average_pages_per_scraper(),
        "scraper_total_runs_per_scraper": scraper_analytics.total_runs_per_scraper(),
        "scraper_longest_run_time": scraper_analytics.longest_run_time(),
        "scraper_average_run_time": scraper_analytics.average_run_time(),
        "scraper_most_page_visited": scraper_analytics.most_pages_visited(),
        "scraper_all": scraper_analytics.sum_by_run_id(),
        "scraper_last": scraper_analytics.get_last_run(),

        "parser_total_runs_per_parser": parser_analytics.total_runs_per_parser(),
        "parser_longest_run_time": parser_analytics.longest_run_time(),
        "parser_average_run_time": parser_analytics.average_run_time(),
        "parser_all": parser_analytics.sum_by_run_id(),
        "parser_last": parser_analytics.get_last_run(),
    }

    return templates.TemplateResponse(
        "root.html",
        context=context
    )


@app.get("/task/scraper")
async def run_scrape_task(request: Request):
    task_scrapers.delay()
    return {"status": "OK"}


@app.get("/task/parser")
async def run_parser_task(request: Request):
    task_parsers.delay()
    return {"status": "OK"}

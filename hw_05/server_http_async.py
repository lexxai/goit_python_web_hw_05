import logging
import mimetypes
from aiohttp import web
from aiopath import AsyncPath


BASE_ROOT_DIR = AsyncPath("html")
ERROR_PAGE = BASE_ROOT_DIR.joinpath("error.html")
INDEX_PAGE = BASE_ROOT_DIR.joinpath("index.html")
PAGE_CHARSET = "utf-8"

routes = web.RouteTableDef()


def log_configure():
    FORMAT = "%(asctime)s  %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)


@routes.get("/")
@routes.get("/{name}")
async def variable_handler(request):
    status = 200
    charset = PAGE_CHARSET
    try:
        name = request.match_info["name"]
    except KeyError:
        name = None
    # logger.info(f"{name=}")
    if not name:
        doc_path = INDEX_PAGE
    else:
        doc_path = BASE_ROOT_DIR.joinpath(name)
    if not await doc_path.exists():
        doc_path = ERROR_PAGE
        status = 404
    if doc_path:
        mimetype, _ = mimetypes.guess_type(doc_path)
        if not mimetype:
            mimetype = "text/plain"
        content_type = mimetype
        try:
            async with doc_path.open("r", encoding=charset) as afp:
                html_txt = await afp.readlines()
        except OSError:
            logger.error(f"Problem open file: {doc_path}")

        body = "".join(html_txt)
        return web.Response(
            body=body, status=status, content_type=content_type, charset=charset
        )


app = web.Application()
app.add_routes(routes)


if __name__ == "__main__":
    # if platform.system() == "Windows":
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    log_configure()
    logger = logging.getLogger(__name__)
    web.run_app(app, port=8000)

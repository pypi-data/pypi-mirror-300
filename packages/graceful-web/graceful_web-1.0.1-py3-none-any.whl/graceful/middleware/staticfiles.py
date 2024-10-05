import os

from graceful.response import HttpResponse


async def static_files_middleware(request, fetch):
    url = request.url.lstrip("/")
    path = os.path.join(cwd, url)

    if os.path.isfile(path):
        return (
            HttpResponse(headers={"Content-Type": "text/x-file"}),
            lambda: url,
        )

    elif os.path.isfile(os.path.join(path, "index.html")):
        return (
            HttpResponse(headers={"Content-Type": "text/x-file"}),
            lambda: os.path.join(url, "index.html"),
        )

    elif os.path.isdir(path):
        pass

    return await fetch(request)


cwd = os.getcwd()

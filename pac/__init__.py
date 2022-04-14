import logging
import datetime

import azure.functions as func


def main(req: func.HttpRequest, pacBlob: str) -> func.HttpResponse:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.error('[%s] Info: GetPAC invoked.', utc_timestamp)

    proxy = req.params.get('proxy')
    if not proxy:
        proxy = "127.0.0.1:1080"
    type = req.params.get('type')
    if not type:
        type = "PROXY"
    return func.HttpResponse(pacBlob.replace("__PROXY__", f"\"{type} {proxy}\""))

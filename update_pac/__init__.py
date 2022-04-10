import datetime
import logging
import requests
import gzip
import json

import azure.functions as func

latest_rel_url = 'https://api.github.com/repos/iBug/pac/releases/latest'


def main(pacTimer: func.TimerRequest, pacBlob: func.Out[bytes]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.error('[%s] Info: UpdatePAC invoked.', utc_timestamp)

    latest_rels = json.loads(requests.get(latest_rel_url).text)
    assets = latest_rels['assets']
    asset_urls = [a['browser_download_url'] for a in assets]
    gfwlist_17mon_url = asset_urls[1]
    if 'gfwlist-17mon' not in gfwlist_17mon_url:
        logging.error(
            '[%s] Error: the second artifact is not gfwlist-17mon.', utc_timestamp)
        return

    pac_resp = requests.get(gfwlist_17mon_url)
    gziped_pac = b''
    for chunk in pac_resp.iter_content(chunk_size=1024):
        if chunk:
            gziped_pac += chunk
    raw_pac = gzip.decompress(gziped_pac)
    pacBlob.set(raw_pac)

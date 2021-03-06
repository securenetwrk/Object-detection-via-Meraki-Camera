import json, requests, os, uuid

MERAKI_API_KEY = ""

NETWORK_ID = ""


def get_response(uri, payload=None, method="GET"):
    # Get video link
    url = "https://api.meraki.com/api/v0{0}".format(uri)

    headers = {
        'X-Cisco-Meraki-API-Key': MERAKI_API_KEY
    }

    if method == "GET":
        resp = requests.request(method, url, headers=headers, params=payload)

    if method == "POST":
        resp = requests.request(method, url, headers=headers, data=payload)

    if int(resp.status_code / 100) == 2:
        return resp.json()
    else:
        return None


def get_snapshot(serial, ts, network_id=NETWORK_ID):
    uri = "/networks/{0}/cameras/{1}/snapshot".format(network_id, serial)

    querystring = {"timestamp": ts}

    resp = get_response(uri, json.dumps(querystring), "POST")

    if resp:

        url = resp["url"]

        print("Image url : {0}".format(url))

        # attempt to fetch the image for 20 times

        for i in range(0, 20):
            resp = requests.request("GET", url)
            if int(resp.status_code / 100) == 2:
                print("{0} time succeed".format(i))
                break
            else:
                print("{0} time failed".format(i))

        return url
    else:
        return None


def init_meraki(network_id, api_key):
    global ZONE_CAMERA_MAPPING, MERAKI_API_KEY, NETWORK_ID

    MERAKI_API_KEY = api_key

    NETWORK_ID = network_id

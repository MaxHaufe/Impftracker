import requests
import json
import telegram_send
import logging

city_hashes = {
    "Dresden": "c623c847b78dres",
    "Kamenz": "c602b847b78bba",
    "Loebau": "c6034d6a1f23aa",
    "Pirna": "c6034d6ce8279b"
    # "Plauen": "c423c83f37ekaj"
}

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    # TODO hardcoded - issue
    json_file = '/home/pi/impftracker/result.json'

    info_log = setup_logger("info_log", "info.log")
    result_log = setup_logger("result_log", "result.log")

    response = requests.get("https://countee-impfee.b-cdn.net/api/1.1/de/counters/getAll/_iz_sachsen?cached=impfee")

    if response.status_code != 200:
        info_log.info("FAIL")
        exit(-1)
    json_obj = json.loads(response.content)

    result = {}
    data_from_file = {}
    for city, hash_ in city_hashes.items():
        amount = json_obj["response"]["data"][hash_]["counteritems"][0]["val"]
        result[city] = amount

    with open(json_file, 'r') as reader:
        data_from_file = json.load(reader)

    with open(json_file, 'w') as writer:
        json.dump(result, writer)

    if data_from_file != result:
        message = ""
        for city, nr in result.items():
            message += "{:<12s}{:>10d}\n".format(city, nr)

        result_log.info(result)
        telegram_send.send(messages=[message])

    info_log.info("Running...SUCCESS")
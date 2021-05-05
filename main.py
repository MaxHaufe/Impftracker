import requests
import json
import telegram_send
import logging

city_hashes = {
    "Dresden": "c623c847b78dres",
    "Kamenz": "c602b847b78bba",
    "Loebau": "c6034d6a1f23aa",
    "Pirna": "c6034d6ce8279b",
    "Plauen": "c423c83f37ekaj"
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
    send_msg_flag = False

    info_log = setup_logger("info_log", "info.log")
    result_log = setup_logger("result_log", "result.log")

    info_log.info("Running...")
    response = requests.get("https://countee-impfee.b-cdn.net/api/1.1/de/counters/getAll/_iz_sachsen?cached=impfee")

    if response.status_code != 200:
        print("Status Code: " + str(response.status_code))
        exit(-1)
    json_obj = json.loads(response.content)
    result = []
    for city, hash_ in city_hashes.items():
        amount = json_obj["response"]["data"][hash_]["counteritems"][0]["val"]
        # send msg if any value > 0
        if amount > 0:
            send_msg_flag = True
            string = "{:<12s}{:>10d}".format(city, amount)
            result.append(string)
            msg = city + ": " + str(amount)
            result_log.info(msg)

    if send_msg_flag:
        telegram_send.send(messages=(["\n".join(result)]))

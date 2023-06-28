import asyncio
import websockets
import json
import time
import statistics

TimeNow = int(time.time()) * 1000
Past24hr = (int(time.time()) * 1000) - 86400000


def extract_dvol_data(response):
    parsed_response = json.loads(response)
    data = parsed_response["result"]["data"]
    values = []
    for point in data:
        values.append(point[1])
        values.append(point[4])
    result = statistics.mean(values)
    return result


def define_limits(avgDVOL, price):
    impliedRange = (avgDVOL / 19.104) / 100
    upperLimitMulti = 1 + impliedRange
    lowerLimitMulti = 1 - impliedRange
    upperBound = price * upperLimitMulti
    lowerBound = price * lowerLimitMulti
    return upperBound, lowerBound


async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        msg_str = json.dumps(msg)
        await websocket.send(msg_str)
        while websocket.open:
            response = await websocket.recv()
            return response


async def get_price():
    msg = \
        {"jsonrpc": "2.0",
         "method": "public/get_index_price",
         "id": 440414585,
         "params": {
             "index_name": "btc_usd"}
         }
    response = await call_api(msg)
    parsed_response = json.loads(response)
    index_price = parsed_response["result"]["index_price"]
    return index_price


async def get_dvol():
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 440141585,
            "method": "public/get_volatility_index_data",
            "params": {
                "currency": "BTC",
                "start_timestamp": Past24hr,
                "end_timestamp": TimeNow,
                "resolution": "43200"
            }
        }
    response = await call_api(msg)
    avgDVOL = extract_dvol_data(response)
    return avgDVOL


async def main():
    avgDVOL = await get_dvol()
    price = await get_price()
    upperBound, lowerBound = define_limits(avgDVOL, price)
    print("AVG DVOL Past 24hrs:", avgDVOL)
    print("Impiled Range is between", upperBound, "&", lowerBound)

if __name__ == '__main__':
    asyncio.run(main())

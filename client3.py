import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2  # Calculate the price as the average of bid and ask
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b != 0:
        return price_a / price_b
    else:
        print("Error: Cannot divide by zero (price_b is zero).")
        return None

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        prices = []  # List to store prices

        """ ----------- Update to get the ratio --------------- """
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))
            prices.append(price)  # Store the price

        if len(prices) >= 2:
            ratio = getRatio(prices[0], prices[1])
            if ratio is not None:
                print("Ratio %s" % ratio)
            else:
                print("Cannot calculate the ratio due to division by zero.")
        else:
            print("Not enough prices to calculate the ratio.")
import requests
from bs4 import BeautifulSoup
import json

with open('vals.json') as f:
    valConv = json.load(f)

hub1props = [1, 2, 3, 4, 5]
hub2props = [6, 7, 8, 10, 12, 13, 16, 19]
hub3props = [23, 25, 26, 27, 29, 30, 31, 32, 34, 35, 36, 37]

points = {}

total = 0


def scrapeHubble(props, baseurl):
    global total
    for i in props:
        URL = baseurl + str(i)
        r = requests.get(URL)

        # If this line causes an error, run 'pip install html5lib' or install html5lib
        soup = BeautifulSoup(r.content, 'html5lib')

        votestable = soup.find("table", {"class": "votes-table"})

        for row in votestable.findAll("tr"):
            atag = row.findAll("a")[0]

            if (atag.find("span") != None):
                bech32addr = atag.find("span").string
                points[bech32addr] = points.get(bech32addr, 0) + 1
            else:
                valhex = atag['href'].split("/")[-1]
                if valhex not in valConv:
                    print(atag.string.strip())
                    print(valhex)
                    print()
                else:
                    bech32addr = valConv[valhex]
                    points[bech32addr] = points.get(bech32addr, 0) + 1

            total += 1


scrapeHubble(
    hub1props, "https://hubble.figment.io/cosmos/chains/cosmoshub-1/governance/proposals/")
scrapeHubble(
    hub2props, "https://hubble.figment.io/cosmos/chains/cosmoshub-2/governance/proposals/")
scrapeHubble(
    hub3props, "https://hubble.figment.io/cosmos/chains/cosmoshub-3/governance/proposals/")

print(json.dumps(points, indent=4, sort_keys=True))


print(len(points))

print(total)

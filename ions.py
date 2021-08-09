import json
import requests
from bs4 import BeautifulSoup

points = {}
total = 0

for genesis in ['genesis.cosmoshub-2.json', 'genesis.cosmoshub-3.json', 'genesis.cosmoshub-4.json']:
    with open(genesis) as f:
        hub = json.load(f)

    for delegation in hub["app_state"]["staking"]["delegations"]:
        if (delegation['validator_address'] == 'cosmosvaloper1ey69r37gfxvxg62sh4r0ktpuc46pzjrm873ae8'):
            delegator = delegation['delegator_address']

            points[delegator] = points.get(delegator, 0) + 1
            total = total + 1


with open('vals.json') as f:
    valConv = json.load(f)

hub1props = [1, 2, 3, 4, 5]
hub2props = [6, 7, 8, 10, 12, 13, 16, 19]
hub3props = [23, 25, 26, 27, 29, 30, 31, 32, 34, 35, 36, 37]


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

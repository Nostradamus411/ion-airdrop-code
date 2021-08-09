import json


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


print(json.dumps(points, indent=4, sort_keys=True))

print(len(points))

print(total)

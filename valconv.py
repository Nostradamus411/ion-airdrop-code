from subprocess import PIPE
import json
import subprocess
import os
import base64


consToAddrs = {}

with open('validators.json') as f:
    vals = json.load(f)

for val in vals['validators']:

    conspubkey = val['consensus_pubkey']['key']
    valaddr = val['operator_address']

    comp_process = subprocess.run(
        ["osmosisd", "debug", "pubkey", conspubkey], stdout=PIPE, stderr=PIPE)

    consaddr = comp_process.stderr.decode(
        "utf-8").split('\n')[0].split(" ")[1]

    comp_process = subprocess.run(
        ["osmosisd", "debug", "bech32-convert", valaddr, "-p", "cosmos"], stdout=PIPE, stderr=PIPE)

    bech32addr = comp_process.stderr.decode("utf-8").strip()

    consToAddrs[consaddr] = bech32addr

print(json.dumps(consToAddrs, indent=4, sort_keys=True))

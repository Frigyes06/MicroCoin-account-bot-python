'''
Copyright (c) 2021 Frigyes06

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
'''

import requests
import json
from params import wallet_jsonrpc_ip, wallet_jsonrpc_port

wallet_jsonrpc_ip_port = wallet_jsonrpc_ip + ':' + str(wallet_jsonrpc_port)

wallet_ok = False

class WalletCommError(Exception):
    pass


class WalletPubKeyError(Exception):
    pass


class WalletInvalidOperationError(Exception):
    pass


class WalletNotReadyError(Exception):
    pass


class WalletInvalidTargetAccountError(Exception):
    pass

def wallet_has_nodes():
    global wallet_ok
    try:
        data = {"jsonrpc": "2.0", "method": "nodestatus", "params": {}, "id": 123}
        try:
            response_raw = requests.post(wallet_jsonrpc_ip_port, json=data)
        except:
            raise WalletCommError

        response = json.loads(response_raw.text)
        if response["result"]["ready"] == False and response["result"]["ready_s"] == "Alone in the world...":
            wallet_ok = False
            return False
        else:
            wallet_ok = True
            return True
    except Exception as e:
        print(f"Wallet has nodes error: " + str(e))
        wallet_ok = False
        return False

def changekey(new_enc_pubkey, account):
    try:
        msg={"jsonrpc":"2.0","method":"changekey","params":{"account":account,"new_enc_pubkey":new_enc_pubkey,"fee":0,"payload":"","payload_method":"none"},"id":123}
        print(msg)
        try:
            response_raw = requests.post(wallet_jsonrpc_ip_port, json=msg)
        except:
            raise WalletCommError

        response = json.loads(response_raw.text)
        if response["error"]:
            print(response)
            return False
        else:
            return True
    except Exception as e:
        print(f"Exception occured:", e)
        return False

def getwalletaccounts():
    try:
        msg = {"jsonrpc":"2.0","method":"getwalletaccounts","id":123}
        try:
            response_raw = requests.post(wallet_jsonrpc_ip_port, json=msg)
        except:
            raise WalletCommError
        response = json.loads(response_raw.text)
        return response["result"]
    except Exception as e:
        print(f"Exception occured:", e)
        return False

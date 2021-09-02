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

import json
with open('config.txt') as f:
    config_data = json.load(f)
    f.close()

version = 2.0

private_key = config_data["private_key"]
wallet_jsonrpc_ip = config_data["wallet_jsonrpc_ip"]
wallet_jsonrpc_port = config_data["wallet_jsonrpc_port"]
discord_bot_token = config_data["discord_bot_token"]
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

import discord
from base58 import b58decode
from wallet_json_rpc import changekey, wallet_has_nodes, getwalletaccounts
from params import discord_bot_token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    words = msg.split()

    if len(words) > 1:
        await message.channel.send("Csak a publikus kulcsodat küld!")
        return
    else:
        wallet_ok = wallet_has_nodes()
        if wallet_ok:
            global decoded
            try:
                decoded = b58decode(msg)
                decoded = decoded.hex()
            except Exception as e:
                print(f"Exception", e, "occured.")
                await message.channel.send("Hoppá! Valószínűleg rossz a kulcsod!")
                return
            
            print(decoded)
            
            if not decoded.startswith("01ca02"):
                await message.channel.send("Hoppá! Valószínűleg rossz a kulcsod!")
                return
            
            sliced = decoded[6:len(decoded) - 8]
            length = len(sliced)
            X = sliced[4:68]
            Y = sliced[length - 64:length]

            print(X, ",", Y)

            accounts = getwalletaccounts()
            acctochange = ""

            print(accounts)
            for f in range(len(accounts)):
                if accounts[f].balance == 0:
                    acctochange = accounts[f]
                    break

            if acctochange == "":
                await message.channel.send("Sajnos most nincs szabad számlám, kérlek próbálkozz újra később.")
                return

            succes = changekey(decoded[2:len(decoded)-8], acctochange)
            if succes:
                await message.channel.send("Kaptál egy számlát!")
            else:
                await message.channel.send("Hoppá! A tranzakció feldolgozása közben hiba történt. Kérlek próbálkozz újra 5-7 perc múlva.")
        else:
            await message.channel.send("A MicroCoin Daemon még nem működik, kérlek próbálkozz újra később")
        
client.run(discord_bot_token)
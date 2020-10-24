from mcstatus import MinecraftServer
import time,requests,json
from datetime import datetime
import requests

def log(message):
    time = str(datetime.now()).split(" ")[1].split(".")[0]
    message = f"<{time}> {message}"
    discord_mess = {
    "content": message,
    "username": "Eden server",
    "avatar_url": "https://cdn.discordapp.com/icons/752571416934744095/872b6b45fc245c6bab8ff7df3d54326d.png?size=128"}

    requests.post("https://discordapp.com/api/webhooks/765780298897948692/FG3zOc7aBcWxYTx21pgzcZDMG6Xt7Hk-dCmOpdh7KJVesqvuma9PtoKKELIS4uxc3KvV",
    json=discord_mess)

print("starting")
server = MinecraftServer.lookup("play.paradisenetworkmc.com")
players,old_players = [],[]
server_up,server_up_old = None,None
log("script start")
loop = True
while loop:
    try:
        players = server.query().players.names
        server_up = True
    except:
        server_up = False
    
    if server_up != server_up_old:
        if server_up == False:
            log("server offline\n")
            players,old_players = [],[]
        elif server_up == True:
            log("server online")
    server_up_old = server_up
    
    if server_up == True:
        for player in players:
            if player not in old_players:
                log(f"[{len(players)}] {player} joined the game")
        for player in old_players:
            if player not in players:
                log(f"[{len(players)}] {player} left the game")
        old_players = players
    time.sleep(60)
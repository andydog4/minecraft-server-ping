from mcstatus import MinecraftServer
import time
from datetime import datetime

def log(message):
    message = f"<{datetime.now()}> {message}"
    print(message)
    message = f"{message}\n"
    with open("log.txt","a") as file:
        file.write(message)
        file.close()


server = MinecraftServer.lookup("play.paradisenetworkmc.com")
players,old_players = [],[]
server_up,server_up_old = None,None
log("script start")
loop = True
while loop:
    changed = False
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
                log(f"[{len(players)}] {player} has joined the game")
        for player in old_players:
            if player not in players:
                log(f"[{len(players)}] {player} has left the game")
        old_players = players
    time.sleep(300)
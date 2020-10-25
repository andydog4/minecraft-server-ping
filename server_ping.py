from mcstatus import MinecraftServer
from datetime import datetime
import time,requests,json

wait_time = 60
server_ips = [
    "play.paradisenetworkmc.com",
    "minecraft.josho.nz",
    "mc.andydog4.xyz"]

def send(message,webhook):
    time = str(datetime.now()).split(" ")[1].split(".")[0]
    message = f"<{time}> {message}"
    print(message)
    discord_message = {
    "content": message,
    "username": "server tracker",
    "avatar_url": "https://cdn.discordapp.com/icons/302094807046684672/a_4a2d4c71d0ec0c7f72792d7280a6529d.png?size=64"}
    requests.post(webhook,json=discord_message)

class server():
    def __init__(self,ip):
        self.server = MinecraftServer.lookup(ip)
        self.webhook = "https://discordapp.com/api/webhooks/765780298897948692/FG3zOc7aBcWxYTx21pgzcZDMG6Xt7Hk-dCmOpdh7KJVesqvuma9PtoKKELIS4uxc3KvV"
        self.server_up_old,self.old_players = None,[]
        self.name = ip.split(".")[1]

    def send(self,message):
        message = f"<{self.name}> {message}"
        send(message,self.webhook)
    
    def check(self):
        try:
            players = self.server.query().players.names
            server_up = True
        except:
            server_up = False
        if server_up != self.server_up_old:
            if server_up == False:
                self.send("server offline\n")
                players,self.old_players = [],[]
            elif server_up == True:
                self.send("server online")
        self.server_up_old = server_up
        
        if server_up == True:
            for player in players:
                if player not in self.old_players:
                    self.send(f"[{len(players)}] {player} joined the game")
            for player in self.old_players:
                if player not in players:
                    self.send(f"[{len(players)}] {player} left the game")
            self.old_players = players

print("starting")
servers = []
for item in server_ips:
    servers.append(server(item))

for item in servers:
    send(f"tracking {item.name}",item.webhook)

while True:
    for item in servers:
        item.check()
    time.sleep(wait_time)
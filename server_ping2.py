from mcstatus import MinecraftServer
from datetime import datetime
from math import pi
import time,requests,random

wait_time = 60
discord_avatar = "https://cdn.discordapp.com/icons/302094807046684672/a_4a2d4c71d0ec0c7f72792d7280a6529d.png?size=64"
server_ips = [
    "minecraft.josho.nz",
    "mc.andydog4.xyz"]
time_stamp = lambda: str(datetime.now()).split(" ")[1].split(".")[0]

class server():
    def __init__(self,ip):
        self.server = MinecraftServer.lookup(ip)
        self.webhook = "https://discordapp.com/api/webhooks/765780298897948692/FG3zOc7aBcWxYTx21pgzcZDMG6Xt7Hk-dCmOpdh7KJVesqvuma9PtoKKELIS4uxc3KvV"
        self.server_up_old,self.old_players = None,[]
        self.name = ip.split(".")[1]
        self.url = ip.split(".",1)[1]
        random.seed(len(ip)*pi)
        self.color = random.randint(0,0xffffff)

    def send(self,message):
        requests.post(self.webhook,json={
            "embeds": [{
                "title": self.name,
                "description": message,
                "color": self.color,
                "url": f"https://{self.url}",
                "footer": {
                    "text": time_stamp()}}],
            "username": "Server Tracker",
            "avatar_url": "https://cdn.discordapp.com/icons/302094807046684672/a_4a2d4c71d0ec0c7f72792d7280a6529d.png?size=64"})
    
    def check(self):
        def joined(joined=[]):
            for player in players:
                if player not in self.old_players:
                    joined.append(player)
            return joined

        def left(left=[]):
            for player in self.old_players:
                if player not in players:
                    left.append(player)
            return left

        def edit(prefix,item):
            for i in range(len(item)):
                item[i] = prefix + item[i]
            return item

        try:#check start
            players = self.server.query().players.names
            server_up = True
        except:
            players = []
            server_up = False

        player_list = lambda data: f"Players: {len(players)}\n{chr(10).join(data)}\n"
        joined = joined()
        left = left()

        if server_up == True: #if server on
            if server_up != self.server_up_old:#if server turns on
                self.send(f"Server started:\n{player_list(edit('+',joined))}")
            else:#server running
                if len(joined) or len(left): #if player count changes
                    players_edit = []
                    for player in players:
                        if player in self.old_players: #if player was all readdy on
                            players_edit.append(player)
                    players_edit.extend(edit("+",joined))
                    players_edit.extend(edit("-",left))
                    self.send(player_list(players_edit))
        else:#if server off
            if server_up != self.server_up_old:
                self.send(f"Server Stopped:\n{player_list(edit('-',left))}")

        self.old_players = players
        self.server_up_old = server_up

print("starting")
servers = []
for ip in server_ips:
    servers.append(server(ip))

loop = True
while loop == True: #server check loop
    for server in servers:
        server.check()
    time.sleep(wait_time)
    #loop = False
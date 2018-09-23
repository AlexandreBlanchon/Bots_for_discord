# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 16:32:15 2018

@author: Alexandre
"""

import discord.ext.commands as disc
import random
import os

TOKEN = os.environ['TOKEN']
BOT_PREFIX = os.environ['PREFIX']
client = disc.Bot(BOT_PREFIX)

data = dict(dict([]))

traduction = ['', 'Merlin', 'Perceval', 'Chevalier', 'Assassin', 'Oberon', 'Morgane', 'un sbire de Mordred']
roles = [[]]*11
tours = [[]]*11 
# 1 : Merlin
# 2 : Perceval
# 3 : Chevalier
# 4 : Assassin
# 5 : Oberon
# 6 : Morgane
# 7 : Sbire
roles[3] = [1,2,4]
roles[5] = [1,2,3,4,7]
roles[6] = [1,2,3,3,4,6]
roles[7] = [1,2,3,3,4,5,7]
roles[8] = [1,2,3,3,3,4,5,6]
roles[9] = [1,2,3,3,3,3,4,6,7]
roles[10] = [1,2,3,3,3,3,4,5,6,7]

tours[3] = [1,2,3,2,3]
tours[5] = [2,3,2,3,3]
tours[6] = [2,3,4,3,4]
tours[7] = [2,3,3,4,4]
tours[8] = [3,4,4,5,5]
tours[9] = [3,4,4,5,5]
tours[10] = [3,4,4,5,5]

@client.event
async def on_ready():
    print("Successfully logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------------------------")

@client.command(brief = "I'm polite !", description = "I reply whenever you greet me !", aliases = ['Hello', 'Hi', 'hi'])
async def hello():
    await client.say("Hello !")
        
@client.command(pass_context = True, brief = "Termine la partie", description = "Permet de quitter une partie à tout moment. A utiliser quand une partie se termine.", aliases = ['end'])
async def end_game(context):
    global data
    server = context.message.server.id
    data[server][game_started] = False
    data[server][fail] = False
    data[server][failures] = 0
    data[server][successes] = 0
    data[server][quest] = 1
    data[server][questers] = []
    data[server][vote] = 1
    data[server][leader] = 0
    data[server][players] = []
    data[server][voters] = []
    await client.say("La partie a bien été réinitialisée. Entrez la commande start pour commencer le choix des joueurs !")


@client.event
async def on_server_join():    
    await client.say("Hello everyone ! I'm AvalonBot and it's so nice to meet you !")
    
@client.command(aliases = ['startgame', 'start-game', 'start'], brief = "C'est là que tout commence !", pass_context = True)
async def start_game(context):
    global data
    server = context.message.server.id
    if server in data and data[server][game_started]:
        await client.say("Une partie est déjà en cours. Entrez la commande join pour la rejoindre.")
    else:
        data[server] = dict([])
        data[server][game_started] = True
        data[server][fail] = False
        data[server][failures] = 0
        data[server][successes] = 0
        data[server][quest] = 1
        data[server][questers] = []
        data[server][vote] = 1
        data[server][leader] = 0
        data[server][players] = []
        data[server][voters] = []
        await client.say("Une partie d'Avalon a été lancée ! Entrez la commande join pour participer !")
        await client.say("POUR L'INSTANT, la plupart des commandes peuvent être entrées en message privé. Je ferai une MàJ quand j'aurai le temps pour pouvoir porter AvalonBot sur d'autres serveurs, et certaines fonctionnalités seront supprimées.")
    
@client.command(pass_context = True, brief = "Rejoignez une partie")
async def join(context):
    global data
    server = context.message.server.id
    if game_started:
        if context.message.author not in data[server][players]:
            if len(data[server][players]) < len(roles)-1:
                data[server][players] += [context.message.author]
                await client.reply("c'est noté. Tu as rejoint la partie !")
            else:
               await client.reply("je suis désolé, mais je ne peux pas t'ajouter à la partie. Le nombre de joueurs maximum est atteint.") 
        else:
            await client.reply("tu es déjà dans la partie.")
    else:
        await client.say("Il n'y a pas de partie en cours. Lancez-en une avec la commande start !")

@client.command(pass_context = True, brief = "La liste des joueurs")
async def players_list(context):
    global data
    server = context.message.server.id
    await client.say("Voici la liste des joueurs")
    for i in data[server][players]:
        await client.say(i.mention)

@client.command(pass_context = True, brief = "Un test de fonctionnalités (détection des id_users)")
async def test(context):
    def check(msg):
        return True
    await client.say("Ceci est un test. "+context.message.author.mention+", désigne un joueur")
    msg = await client.wait_for_message(author = context.message.author,check = check)
    user_id = msg.content
    await client.say("Tu as parlé de {} ?".format(user_id))
    user = await client.get_user_info(user_id[2:-1])
    await client.send_message(destination = user, content = context.message.author.mention+" mentionned you !")
    
@client.command(pass_context = True, brief = "Un test de fonctionnalités (mention du server)")
async def server_mention(context):
    await client.reply("Nous sommes sur le serveur "+context.message.server.name)
    await client.reply("Nous sommes sur le serveur "+str(context.message.server.id))

@client.command(pass_context = True, brief = "Une fois que tous les joueurs sont là")
async def pret(context):
    global data
    server = context.message.server.id
    def check(msg):
        return True if msg.content[2:-1] in [i.id for i in data[server][players]] else False
    def check2(msg):
        return True if msg.author.id in [i.id for i in data[server][voters]] and (msg.content == 'Pour' or msg.content == 'Contre') else False
    def check3(msg):
        return True if msg.author.id in [i.id for i in data[server][voters]] and (msg.content == 'Succès' or msg.content == 'Echec') else False
    if not game_started:
        await client.say("Il n'y a pas de partie en cours. Lancez-en une avec la commande start !")
    elif len(data[server][players]) < 5 and en(data[server][players]) != 3:
        await client.say("Pas assez de joueurs !")
    else:
        await client.say("La partie va commencer. Je commence à distribuer les rôles.")
        data[server][temp] = roles[len(data[server][players])].copy()
        random.shuffle(data[server][temp])
        data[server][game_data] = [(data[server][temp][i], data[server][players][i]) for i in range (len(data[server][players]))]
        random.shuffle(data[server][players])
        for i in data[server][game_data]:
            await client.send_message(destination = i[1], content = "Pour la partie d'Avalon en cours sur le serveur "+context.message.server.name+", tu es "+traduction[i[0]])
            if i[0]<4:
                await client.send_message(destination = i[1], content = "Tu es un loyal serviteur d'Arthur. Il t'incombe de démasquer les serviteurs du mal et de les empêcher de nuire à Merlin !")
            else:
                await client.send_message(destination = i[1], content = "Tu sers le mal. Avec tes alliés, tu dois faire échouer les loyaux serviteurs d'Arthur dans leur quête, ou au moins découvrir l'identité de Merlin !")
            if i[0]==1:
                for j in data[server][game_data]:
                    if j[0]>3:
                        await client.send_message(destination = i[1], content = "Tes pouvoirs magiques te révèlent que "+j[1].name+" sert le mal.")
            if i[0]==2:
                for j in data[server][game_data]:
                    if j[0]==1:
                        await client.send_message(destination = i[1], content = "Tu connais l'identité secrète de Merlin ! C'est "+j[1].name)
            if i[0]>3:
                for j in data[server][game_data]:
                    if j[0]>3 and j[1] != i[1]:
                        await client.send_message(destination = i[1], content = j[1].name+" est un de tes alliés.")
        await client.say("Les rôles ont été distribués. Nous pouvons maintenant passer à la phase de quêtes !")
        while data[server][failures]<3 and data[server][successes]<3:
            await client.say("Procédons à la quête numéro "+str(data[server][quest])+", vote numéro "+str(data[server][vote]))
            if data[server][vote] == 5:
                await client.say("Attention ! Cette équipe de quête sera automatiquement acceptée.")
            await client.say("C'est à "+data[server][players][data[server][leader]].mention+" de choisir l'équipe. Elle devra être constituée de "+str(tours[len(data[server][players])][data[server][quest]-1])+" joueurs.")
            data[server][questers] = []
            while len(data[server][questers])<tours[len(data[server][players])][data[server][quest]-1] and data[server][vote] < 5:
                msg = await client.wait_for_message(author = data[server][players][data[server][leader]], check = check)
                user_id = msg.content
                await client.say(content = user_id+" a été ajouté à l'équipe de quête.")
                user = await client.get_user_info(user_id[2:-1])
                if user not in data[server][questers]:
                    data[server][questers] += [await client.get_user_info(user_id[2:-1])]
                else:
                    await client.say("Cette personne a déjà été ajoutée à l'équipe de quête.")
            await client.say("L'équipe de quête a été constituée. Les personnes suivantes en font partie :")
            for i in data[server][questers]:
                await client.say(i.mention)
            await client.say("Votez Pour ou Contre l'équipe de quête !")
            data[server][voters] = data[server][players].copy()
            votes_pour = 0
            while data[server][voters] != [] and votes_pour <= len(data[server][players])//2 and data[server][vote] < 5:
                msg = await client.wait_for_message(check = check2)
                data[server][voters].remove(msg.author)
                await client.say(msg.author.mention+" a voté "+msg.content)
                if msg.content == "Pour":
                    votes_pour += 1
            if votes_pour > len(data[server][players])//2 or data[server][vote] == 5:
                await client.say("L'équipe est acceptée ! Il faut maintenant que les membres de l'équipe m'envoient leur vote (Succès ou Echec) par message privé.")
                data[server][voters] = data[server][questers].copy()
                data[server][fail] = False
                while data[server][voters] != []:
                    msg = await client.wait_for_message(check = check3)
                    data[server][voters].remove(msg.author)
                    await client.say(msg.author.mention + " a voté.")
                    if msg.content == "Echec":
                        data[server][fail] = True
                if data[server][fail]:
                    await client.say("La quête est un échec.")
                    data[server][failures] +=1
                    data[server][leader] = (data[server][leader] + 1)%len(data[server][players])
                    data[server][quest] +=1
                else:
                    await client.say("La quête est un succès.")
                    data[server][successes] +=1
                    data[server][leader] = (data[server][leader] + 1)%len(data[server][players])
                    data[server][quest] +=1
            else:
                await client.say("L'équipe est refusée")
                data[server][leader] = (data[server][leader] + 1)%len(data[server][players])
        if data[server][failures]==3:
            await client.say("Les agents du Mal, c'est à dire ")
            for j in data[server][game_data]:
                    if j[0]>3:
                        await client.say(j[0].mention)
            await client.say("ont vaincu.")
        if data[server][successes]==3:
            await client.say("Les loyaux serviteurs d'Arthur ont accompli leurs trois quêtes. L'assassin, c'est à dire : ")
            for j in data[server][game_data]:
                    if j[0]==4:
                        assassin = j[1]
                        await client.say(j[1].mention)
            await client.say("peut maintenant désigner sa victime")
            msg = await client.wait_for_message(author = assassin, check = check)
            user_id = msg.content
            user = await client.get_user_info(user_id[2:-1])
            if (1, user) in data[server][game_data]:
                await client.say ("L'assassin a tué Merlin. C'est finalement le Mal qui a vaincu !")
            else:
                await client.say("L'assassin n'a pas réussi à tuer Merlin. Le Bien triomphe !")
     
@client.command(pass_context = True, brief = "Un test de fonctionnalités (demande de mp)")
async def mp(context):
    await client.wait_for_message(author = context.message.author)
    await client.whisper("J'ai bien reçu ton message")               
     
        
client.run(TOKEN)








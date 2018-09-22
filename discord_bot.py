# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 16:32:15 2018

@author: Alexandre
"""

import discord as discord
import discord.ext.commands as disc
import random
import time

BOT_PREFIX = ("!", "?")
TOKEN = 'NDkyNzAyMDY5NzE1ODk0Mjkz.Doaycw.2DL8tKNQl9bDl0o3JXlEhyXbpcQ'

client = disc.Bot(BOT_PREFIX)
game_started = False
fail = False
failures = 0
successes = 0
quest = 1
questers = []
vote = 1
leader = 0
players = []
voters = []
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
roles[5] = [1,2,3,4,7]
roles[6] = [1,2,3,3,4,6]
roles[7] = [1,2,3,3,4,5,7]
roles[8] = [1,2,3,3,3,4,5,6]
roles[9] = [1,2,3,3,3,3,4,6,7]
roles[10] = [1,2,3,3,3,3,4,5,6,7]

tours[5] = [2,3,2,3,3]
tours[6] = [2,3,4,3,4]
tours[7] = [2,3,3,4,4]
tours[8] = [3,4,4,5,5]
tours[9] = [3,4,4,5,5]
tours[10] = [3,4,4,5,5]

@client.command(brief = "I'm polite !", description = "I reply whenever you greet me !", aliases = ['Hello', 'Hi', 'hi'])
async def hello():
    await client.say("Hello !")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    
@client.event
async def on_server_join():    
    await client.say("Hello everyone ! I'm AvalonBot and it's so nice to meet you !")
    
@client.command(aliases = ['startgame', 'start-game', 'start'], brief = "C'est là que tout commence !")
async def start_game():
    global game_started
    if game_started:
        await client.say("Une partie est déjà en cours. Entrez la commande join pour la rejoindre.")
    else:
        game_started = True
        await client.say("Une partie d'Avalon a été lancée ! Entrez la commande join pour participer !")
    
@client.command(pass_context = True, brief = "Rejoignez une partie")
async def join(context):
    global game_started, players
    if game_started:
        if context.message.author not in players:
            if len(players) < len(roles):
                players += [context.message.author]
                await client.reply("c'est noté. Tu as rejoint la partie !")
            else:
               await client.reply("je suis désolé, mais je ne peux pas t'ajouter à la partie. Le nombre de joueurs maximum est atteint.") 
        else:
            await client.reply("tu es déjà dans la partie.")
    else:
        await client.say("Il n'y a pas de partie en cours. Lancez-en une avec la commande start !")

@client.command(pass_context = True, brief = "La liste des joueurs")
async def players_list(context):
    global players
    await client.say("Voici la liste des joueurs")
    for i in players:
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

@client.command(pass_context = True, brief = "Une fois que tous les joueurs sont là")
async def pret(context):
    global players, game_started, questers, quest, leader, roles, tours, vote, failures, successes, voters
    def check(msg):
        return True if msg.content[2:-1] in [i.id for i in players] else False
    def check2(msg):
        return True if msg.author in [i.id for i in voters] and (msg.content == 'Pour' or msg.content == 'Contre') else False
    def check3(msg):
        return True if msg.author in [i.id for i in voters] and (msg.content == 'Succès' or msg.content == 'Echec') else False
    if not game_started:
        await client.say("Il n'y a pas de partie en cours. Lancez-en une avec la commande start !")
    elif len(players) < 5:
        await client.say("Pas assez de joueurs !")
    else:
        await client.say("La partie va commencer. Je commence à distribuer les rôles.")
        temp = roles[len(players)].copy()
        temp = random.shuffle(temp)
        game_data = [(temp[i], players[i]) for i in range (len(players))]
        players = random.shuffle(players)
        for i in game_data:
            await client.whisper(destination = i[1], content = "Pour la partie d'Avalon en cours sur le serveur "+context.message.server.name+", tu es "+traduction[i[0]])
            if i[0]<4:
                await client.whisper(destination = i[1], content = "Tu es un loyal serviteur d'Arthur. Il t'incombe de démasquer les serviteurs du mal et de les empêcher de nuire à Merlin !")
            else:
                await client.whisper(destination = i[1], content = "Tu sers le mal. Avec tes alliés, tu dois faire échouer les loyaux serviteurs d'Arthur dans leur quête, ou au moins découvrir l'identité de Merlin !")
            if i[0]==1:
                for j in game_data:
                    if j[0]>3:
                        await client.whisper(destination = i[1], content = "Tes pouvoirs magiques te révèlent que "+j[0].mention+" sert le mal.")
            if i[0]==2:
                for j in game_data:
                    if j[0]==1:
                        await client.whisper(destination = i[1], content = "Tu connais l'identité secrète de Merlin ! C'est "+j[1].mention)
            if i[0]>3:
                for j in game_data:
                    if j[0]>3 and j[1] != i[1]:
                        await client.whisper(destination = i[1], content = j[0].mention+" est un de tes alliés.")
        await client.say("Les rôles ont été distribués. Nous pouvons maintenant passer à la phase de quêtes !")
        while failures<3 and successes<3:
            await client.say("Procédons à la quête numéro "+str(quest)+", vote numéro "+str(vote))
            if vote == 5:
                await client.say("Attention ! Cette équipe de quête sera automatiquement acceptée.")
                await client.say("C'est à "+players[leader].mention+"de choisir l'équipe.")
            while len(questers)<tours[len(players)][quest]:
                msg = await client.wait_for_message(author = players[leader], check = check)
                user_id = msg.content
                await client.reply(msg = msg, content = user_id+" a été ajouté à l'équipe de quête.")
                questers += [await client.get_user_info(user_id[2:-1])]
            await client.say("L'équipe de quête a été constituée. Les personnes suivantes en font partie :")
            for i in questers:
                await client.say(i.mention)
            await client.say("Votez Pour ou Contre l'équipe de quête ! (En message privé si possible)")
            voters = players.copy()
            votes_pour = 0
            while voters != [] and votes_pour <= len(players)//2:
                msg = await client.wait_for_message(author = players[leader], check = check2)
                voters.remove(msg.author)
                await client.say(msg.author.mention+" a voté "+msg.content)
                if msg.content == "Pour":
                    votes_pour += 1
            if votes_pour > len(players)//2:
                await client.say("L'équipe est acceptée ! Il faut maintenant que les membres de l'équipe m'envoient leur vote (Succès ou Echec) par message privé.")
                voters = questers.copy()
                while voters != []:
                    msg = await client.wait_for_message(author = players[leader], check = check3)
                    voters.remove(msg.author)
                    await client.say(msg.author.mention + " a voté.")
                    if msg.content == "Echec":
                        fail = True
                if fail:
                    await client.say("La quête est un échec.")
                    failures +=1
                    leader +=1
                    quest +=1
                else:
                    await client.say("La quête est un succès.")
                    successes +=1
                    leader +=1
                    quest +=1
            else:
                await client.say("L'équipe est refusée")
                leader +=1
        if failures==3:
            await client.say("Les agents du Mal, c'est à dire ")
            for j in game_data:
                    if j[0]>3:
                        await client.say(j[0].mention)
            await client.say("ont vaincu.")
        if successes==3:
            await client.say("Les loyaux serviteurs d'Arthur ont accompli leurs trois quêtes. L'assassin, c'est à dire : ")
            for j in game_data:
                    if j[0]==4:
                        await client.say(j[0].mention)
            await client.say("peut maintenant désigner sa victime")
            msg = await client.wait_for_message(author = players[leader], check = check)
            user_id = msg.content
            user = await client.get_user_info(user_id[2:-1])
            if (user, 1) in game_data:
                await client.say ("L'assassin a tué Merlin. C'est finalement le Mal qui ont vaincu !")
            else:
                await client.say("L'assassin n'a pas réussi à tuer Merlin. Le Bien triomphe !")
     
@client.command(pass_context = True, brief = "Un test de fonctionnalités (demande de mp)")
async def mp(context):
    await client.wait_for_message(author = context.message.author)
    await client.whisper("J'ai bien reçu ton message")               
     
        
client.run(TOKEN)








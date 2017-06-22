import sys
import re
import telebot
from telebot import types
import time 
import json
import urllib
import random
import os
import six
import socket
import requests
from collections import OrderedDict
from colorclass import Color
from io import StringIO

print(Color(
    '{autored}[{/red}{autoyellow}+{/yellow}{autored}]{/red} {autocyan} Bnet iniciado.{/cyan}'))

import sqlite3
con = sqlite3.connect('bnet.db',check_same_thread = False)
c = con.cursor()
pkmn = ""

TOKEN = '' 


usuarios = [line.rstrip('\n') for line in open('users.txt')] 
admins = [1896312]

bot = telebot.TeleBot(TOKEN) 
hora = time.strftime("%Y-%m-%d %H:%M:%S")

try:
    bot.send_message(admins[0], "@BattleNet_Bot ha sido encendido")
except Exception as e:
    bot.send_message(admins[0], str(e))

def listener(messages):
	for m in messages:
		cid = m.chat.id
		uid = m.from_user.id
		uname = m.from_user.username
		mct = m.chat.title
		ufm = m.from_user.first_name
		ulm = m.from_user.last_name
			
		if m.text:
			mensaje = f"{{autogreen}}User:{{/green}} {ufm}\n"
			if cid < 0:
				mensaje += f"{{autoyellow}}Chat:{{/yellow}} {mct}\n"
				mensaje += f"{{autored}}Hora:{{/red}} {hora}\n"
				mensaje += f"{{autocyan}}UserID:{{/cyan}} [{uid}]"
			if cid < 0:
				mensaje += f"{{autoblue}} ChatID:{{/blue}} [{cid}]"
				mensaje += "\n"
				mensaje += f"{{automagenta}}Mensaje:{{/magenta}} {m.text}\n"
				mensaje += "{autoblack}-------------------------------{/black}\n"
			else:
				mensaje += f"{{autored}}Hora:{{/red}} {hora}\n"
				mensaje += f"{{autocyan}}UserID:{{/cyan}} [{uid}] "
				mensaje += f"{{automagenta}}Mensaje:{{/magenta}} {m.text}\n"
				mensaje += "{autoblack}-------------------------------{/black}\n"
				
			if m.text.startswith("/"):
				f = open('log.txt', 'a')
				f.write(mensaje)
				f.close()
				patata = open('id.txt', 'a')
				patata.write(f'@{uname} [{uid}]\n')
				patata.close()
				print (Color(str(mensaje)))

bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	comandos = "Avaible commands:\n"
	comandos += "/add - The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).\n"
	comandos += "/edit - The format of the command is `/edit Battletag` where `Battletag` is your Battletag (or Blizzard ID).\n"
	comandos += "/list - List of the Battletags.\n"
	comandos += "/mybt - You don't remember your Battletag? NP BRUH!"
	bot.send_message(cid, comandos, parse_mode="Markdown")
	
	
@bot.message_handler(commands=['eg'])
def command_eg(m):
	cid = m.chat.id
	EG = existeGrupo(cid)
	if(EG == 1):
		bot.send_message(cid, "El grupo existe en la BD",
						 parse_mode="Markdown")
	else:
		bot.send_message(cid, "El grupo NO existe en la BD",
						 parse_mode="Markdown")

def existeGrupo(cid):
	c.execute(f"SELECT COUNT(*) FROM GRUPO WHERE idGrupo ='{cid}'")
	try:
		for i in c:
			print("Vamos a ver si el select de grupo ha devuelto algún elemento")
			print(f'El resultado del select es: {i[0]}')
			EG =i[0]
	
	except Exception as e:
		print(e)
		print("Estamos aquí porque el select nos ha devuelto un elemento vacío")
		EG = 0
	
	return EG

def existeUser(uid):
	c.execute(f"SELECT COUNT(*) FROM Usuarios WHERE idUsuario ='{uid}'")
	try:
		for i in c:
			print("Vamos a ver si el select de Usuarios ha devuelto algún elemento")
			print(f"El resultado del select es: {i[0]}")
			EU =i[0]
	
	except Exception as e:
		print(e)
		print("Estamos aquí porque el select nos ha devuelto un elemento vacío")
		EU = 0
	
	return EU

def existeUserGru(uid,cid):
	c.execute(f"SELECT COUNT(*) FROM UsuGrupo WHERE idUsuarioFK ='{uid}' AND idGrupoFK ='{cid}'")
	try:
		for i in c:
			print("Vamos a ver si el select de UsuGrupo ha devuelto algún elemento")
			print(f"El resultado del select es: {i[0]}")
			EUG =i[0]
	
	except Exception as e:
		print(e)
		print("Estamos aquí porque el select nos ha devuelto un elemento vacío")
		EUG = 0
	print(f"Vamos a devolver el valor de EUG que es {EUG}")
	return EUG

@bot.message_handler(commands=['list'])
def command_id(m):
	cid = m.chat.id 
	uname = m.from_user.username
	uid = m.from_user.id
	arrayl = []
	try:
		print("entro en el try")
		c.execute(f"SELECT idUsuario,ALIAS,Battletag FROM Usuarios INNER JOIN UsuGrupo ON Usuarios.idUsuario = UsuGrupo.idUsuarioFK WHERE UsuGrupo.idGrupoFK ='{cid}' ORDER BY Alias ASC")
		print("hago el for?")
		for i in c:
			print("1")
			Alias_resultado = f'{i[1]}: '
			print("2)" + str(Alias_resultado))
			btag_resultado = i[2]
			print("3)" + str(btag_resultado))
			p = f'*{Alias_resultado}* `{btag_resultado}`'
			print("4" + str(p))
			arrayl.append(p)
			print("5")
		f = str(arrayl).replace(" '","").replace("'","")
		f = f.replace(",", "\n").replace("[","").replace("]","")
		if not f:
			f = "The DB is empty. Please add yourself with `/add Battletag` where `Battletag` is your Battletag or Blizzard ID."
			print(str(f))
			bot.send_message(cid, f'{f}', parse_mode = "Markdown")
			con.commit()
		else:
			print(str(f))
			bot.send_message(cid, f'{f}', parse_mode = "Markdown")
			con.commit()
	
	except:
		bot.send_message(cid, "An error ocurred. Report to @Intervencion.")


@bot.message_handler(commands=['add'])
def command_addbtag(m):
	cid = m.chat.id
	uid = m.from_user.id
	mct = m.chat.title
	ufm = m.from_user.first_name
	ulm = m.from_user.last_name
	if (m.from_user.username is None):
		if (ulm == None):
			uname = ufm
		else:
			uname = f'{ufm} {ulm}'
	else:
		uname = m.from_user.username
	if(cid>0):
		bot.send_message(cid,"This only works in groups.")
	elif(cid<0):
		print(str(cid))
		print("VAMOS A LEERLO SIN TRY")
		try:
			btag = m.text.split(' ', 1)[1].capitalize()
			print(str(btag))
			if re.match("^(\w+)#(\d{4,5})$", btag):
				print("He entrado comprovando que el patrón es bueno")
				print("voy a mirar si el grupo ya existe")
				EG = existeGrupo(cid)
				if (EG == 0):
					print("El Grupo no existe, ergo tengo que crearlo")
					print(m.chat.title)
					print(f"El nombre del chat es: {mct}")
					print("Ahora vamos a hacer el insert en el grupo")
					try:
						c.execute(f"INSERT INTO Grupo (idGrupo,NombreGrup) VALUES ('{cid}','{mct}')")
						print(f"El id del grupo {cid}")
						nocapital = uname.capitalize()
						EU = existeUser(uid)
						if(EU == 0):
							c.execute(f"INSERT INTO Usuarios (idUsuario,ALIAS,Battletag) VALUES ('{uid}','@{nocapital}','{btag}')")
						print("ESTOY DEBAJO DEL IF de ENTRE USUARIO = 0")
						c.execute(f"INSERT INTO UsuGrupo(idUsuarioFK,idGrupoFK) VALUES ('{uid}','{cid}')")
						bot.send_message(cid, f"*{uname}* has been added to the DB with Battletag *{btag}*.", parse_mode="Markdown")
						con.commit()
					except sqlite3.Error as e:
						print(e)
						bot.send_message(cid, f"*{uname}* has been added to the DB with Battletag *{btag}*.", parse_mode="Markdown")
				elif(EG == 1):
					print("El grupo sí existe")
					nocapital = uname.capitalize()
					try:
						EU = existeUser(uid)
						if(EU == 0):
							c.execute(f"INSERT INTO Usuarios (idUsuario,ALIAS,Battletag) VALUES ('{uid}', '@{nocapital}','{btag}')")
						print("ESTOY DEBAJO DEL IF de ENTRE USUARIO = 0 Y AHORA VOY A COMPROBAR EUG")
						EUG = existeUserGru(uid,cid)
						print("Sabemos que EUG vale " + str(EUG))
						if(EUG == 0):
							print("Entro cuando no existe la combinación usuario - grupo")
							c.execute(f"INSERT INTO UsuGrupo(idUsuarioFK,idGrupoFK) VALUES ('{uid}','{cid}')")
							bot.send_message(cid, f"*{uname}* has been added to the DB with Battletag *{btag}*.", parse_mode="Markdown")
						if(EUG == 1):
							bot.send_message(cid, "You have already introduced your Battletag in this group, if you want to edit it use `/edit`", parse_mode="Markdown")
						con.commit()
					except sqlite3.Error as e:
						print(e)
						bot.send_message(cid, "You have already introduced your Battletag in this group, if you want to edit it use `/edit`", parse_mode="Markdown")
			else:
				bot.send_message(cid, "ElseError: The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).", parse_mode="Markdown")
		except:
			bot.send_message(cid, "ExceptError: The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).", parse_mode="Markdown")


@bot.message_handler(commands=['edit']) 
def command_editbtag(m):
	cid = m.chat.id
	uid = m.from_user.id
	ufm = m.from_user.first_name
	ulm = m.from_user.last_name
	if (m.from_user.username is None):
		uname = f"{ufm} {ulm}"
	else:
		uname = m.from_user.username
	try:
		btag = m.text.split(' ', 1)[1].capitalize()
		print(str(btag))
		if re.match("^(\w+)#(\d{4,5})$", btag):
			try:
			  c.execute(f"UPDATE Usuarios SET 'Battletag' = '{btag}','Alias'='@{uname}' WHERE idUsuario = {uid}")
			  bot.send_message(cid, f"*{uname}* now have Battletag *{btag}*.", parse_mode = "Markdown")
			  con.commit()
	
			except sqlite3.Error:
			  bot.send_message(cid, "ExceptError: The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).", parse_mode="Markdown")
		else:
			
			bot.send_message(cid, "ElseError: The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).", parse_mode="Markdown")
	except:
	  bot.send_message(cid, "ExceptError: The format of the command is `/add Battletag` where `Battletag` is your Battletag (or Blizzard ID).", parse_mode="Markdown")


@bot.message_handler(commands=['mybt']) 
def command_mibtag(m):
	cid = m.chat.id
	uid = m.from_user.id
	ufm = m.from_user.first_name
	ulm = m.from_user.last_name
	if (m.from_user.username is None):
		uname = f"{ufm} {ulm}"
	else:
		uname = m.from_user.username
	try:
		c.execute(f"SELECT ALIAS,Battletag from Usuarios WHERE idUsuario={uid}")
		
		for i in c:
			Alias_resultado = f"{i[0]} "
			btag_resultado = i[1]
				
		if (btag_resultado == None):
			bot.send_message(cid, f'Your Battletag is not in the DB.', parse_mode = "Markdown")
			con.commit()
		else:
			bot.send_message(cid, f'*{Alias_resultado}*: `{btag_resultado}`', parse_mode = "Markdown")
			con.commit()
	except:
		bot.send_message(cid, "Your Battletag is not in the DB.", parse_mode = "Markdown")

from config import *

@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    uid = m.from_user.id
    #try:
        #send_udp('exec')
    #except Exception as e:
    #    bot.send_message(1896312, send_exception(e), parse_mode="Markdown")
    if not is_recent(m):
        return None
    if m.from_user.id in admins:
        if len(m.text.split()) == 1:
            bot.send_message(
                cid,
                "Uso: /exec _<code>_ - Ejecuta el siguiente bloque de código.",
                parse_mode="Markdown")
            return
        cout = StringIO()
        sys.stdout = cout
        cerr = StringIO()
        sys.stderr = cerr
        code = ' '.join(m.text.split(' ')[1:])
        try:
            exec(code)
        except Exception as e:
            bot.send_message(cid, send_exception(e), parse_mode="Markdown")
        else:
            if cout.getvalue():
                bot.send_message(cid, str(cout.getvalue()))
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        
@bot.message_handler(commands=['restart'])
def command_restart(m):
	if m.from_user.id in admins:
		try:
			os.execl(sys.executable, sys.executable, *sys.argv)
		except:
			bot.send_message(cid, "Mal código tete")
	else:
		bot.send_message(cid, "Comando reservado a SU.")






bot.skip_pending = True
bot.polling(none_stop=True)
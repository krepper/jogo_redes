#!/usr/bin/env python
# -*- coding: utf-8 -*-
from game.dados import *
import socket
import math
import random

'''
====================
	  FUNCOES
====================
'''

'''
# PODER
'''

def destruirPoder(poder, jogo):
	jogo.poderes.remove(poder)


'''
# MOVER_JOGO
'''

def mover_player(player):
	if player.x < 0 or player.x > LARGURA:
		return "POSICAO INVALIDA"
	else: 
		player.x = player.x + player.dx

		if player.x > PAREDE_DIREITA:
			player.x = PAREDE_DIREITA
		elif player.x < PAREDE_ESQUERDA:
			player.x = PAREDE_ESQUERDA	

		return player

def voar(player):
	if player.y < 0 or player.y > 580:
		pass
	else:
		player.y = player.y + player.dy

		if player.y < PAREDE_CIMA:
			player.y = PAREDE_CIMA
		elif player.y > 565:
			player.y = 565
		
		return player

def aumentar_ki(player):
	if player.mp < 100:
		player.mp = player.mp + player.dmp
	
	if player.mp > 100:
		player.mp = 100

def mover_poder(poder, jogo):
	if(poder.x < 0 or poder.x > LARGURA):
		destruirPoder(poder, jogo)
	else:
		poder.x = poder.x + poder.dx

		if(poder.x > LARGURA):
			destruirPoder(poder, jogo)
		elif(poder.x < 0):
			destruirPoder(poder, jogo)
	

def mover_jogo(jogo):

	try:
		mover_player(jogo.jogador)
		voar(jogo.jogador)
		aumentar_ki(jogo.jogador)

		for poder in jogo.poderes:
			mover_poder(poder, jogo)
	except:
		return jogo
 
	return jogo

'''
# DESENHA_JOGO
'''

def desenha_jogador(j):
	try:
		img = None
		personagem = None

		# SE DIRECT +1 ->
		# SE DIRECT -1 <-

		if j.id == 0:
			personagem = IMG_GOKU
		elif j.id == 1:
			personagem = IMG_VEGETA

		if(j.dx == 0):
			img = personagem[0] # PARADO
		elif(j.dx > 0 or j.dx < 0):
			img = personagem[1] # INDO
		if(j.dmp > 0):
			img = personagem[2] # ATIRANDO

		if(j.direct == -1):
			img = pg.transform.flip(img, True, False)

		TELA.blit(img, (j.x - IMG_P1.get_width()/2, j.y - IMG_P1.get_height()/2))

	except:
		print(j)

def desenha_poder(poder, jogador):
	if poder.id_dono == 0:
		personagem = IMG_GOKU
	elif poder.id_dono == 1:
		personagem = IMG_VEGETA

	img = personagem[4]

	if(poder.dx < 0):
		img = pg.transform.flip(img, True, False)

	TELA.blit(img, (poder.x - img.get_width()/2, poder.y - img.get_height()/2))

def desenha_jogo(jogo):
	TELA.blit(IMG_BACKGROUND, (0,0))

	for jogador in jogo.jogadores:
		desenha_jogador(jogador)

	try:
		for poder in jogo.poderes:
			desenha_poder(poder, jogo.jogador)
	except:
		pass

	fonte = pg.font.SysFont("monospace", 40)

	## DESENHA LADO GOKU
	try:
		TELA.blit(IMG_LIFE, (X_LIFE, Y_LIFE))
		TELA.blit(IMG_KI, (X_LIFE, Y_LIFE-35))
		textoP1 = fonte.render(str(jogo.jogadores[0].hp), 1, (255, 255, 255))
		textoP1_M = fonte.render(str(jogo.jogadores[0].mp), 1, (255, 255, 255))
		TELA.blit(textoP1, (X_LIFE+32, Y_LIFE-5))		
		TELA.blit(textoP1_M, (X_LIFE+32, Y_LIFE-40))		
	except: 
		TELA.blit(IMG_DISCONNECT, (X_LIFE+32, Y_LIFE))

	## DESENHA LADO VEGETA
	try:
		TELA.blit(IMG_LIFE, (X_LIFE2, Y_LIFE))
		TELA.blit(IMG_KI, (X_LIFE2, Y_LIFE-35))
		textoP2 = fonte.render(str(jogo.jogadores[1].hp), 1, (255, 255, 255))
		textoP2_M = fonte.render(str(jogo.jogadores[1].mp), 1, (255, 255, 255))
		TELA.blit(textoP2, (X_LIFE2-72, Y_LIFE-5))
		TELA.blit(textoP2_M, (X_LIFE2-72, Y_LIFE-40))
	except: 
		TELA.blit(IMG_DISCONNECT, (X_LIFE2-32, Y_LIFE))

'''
# TRATA_TECLA
'''

def trata_tecla_player(player, tecla):
	if (tecla == pg.K_LEFT) or (tecla == pg.K_LEFT and pg.K_SPACE):
		player.dx = -DX
		player.direct = -1
	elif (tecla == pg.K_RIGHT) or (tecla == pg.K_RIGHT and pg.K_SPACE):
		player.dx = DX
		player.direct = 1
	elif (tecla == pg.K_UP) or (tecla == pg.K_UP and pg.K_SPACE):
		player.dy = -DY
	elif (tecla == pg.K_DOWN) or (tecla == pg.K_DOWN and pg.K_SPACE):
		player.dy = DY
	elif (tecla == pg.K_w) and (player.dx == 0):
		player.dmp = KI_UP
		
	return player

def trata_solta_tecla_player(player, tecla):
	if(tecla == pg.K_RIGHT or tecla == pg.K_LEFT):
		player.dx = 0
	if(tecla == pg.K_DOWN or tecla == pg.K_UP):
		player.dy = 0
	elif(tecla == pg.K_w):
		player.dmp = 0
	return player

def trata_tecla_poderes(jogo, tecla):
	if (tecla == pg.K_SPACE):
		jogo.poderes = soltarPoder(jogo.poderes, jogo.jogador)
		jogo.jogador.mp -= 15
		
		if jogo.jogador.mp < 0:
			jogo.jogador.mp = 0

	return jogo

def trata_tecla(jogo, tecla):
	jogo.jogador = trata_tecla_player(jogo.jogador, tecla)
	jogo = trata_tecla_poderes(jogo, tecla)
	return jogo

def trata_solta_tecla(jogo, tecla):
	jogo.jogador = trata_solta_tecla_player(jogo.jogador, tecla)
	return jogo



	
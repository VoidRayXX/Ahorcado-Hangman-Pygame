import pygame
from math import sqrt
from random import choice

#funciones auxiliares
def dibujar(win,blanco,botones,imagenes,estado,negro,Radio,fuente,victorias,derrotas):
	win.fill(blanco)
	
	#dibujar botones
	for boton in botones:
		x,y,letra,visible = boton
		if visible:
			pygame.draw.circle(win,negro,(x,y),Radio,3)
			texto = fuente.render(letra,1,negro)
			win.blit(texto,(x - texto.get_width()/2 , y - texto.get_height()/2))

	win.blit(imagenes[estado],(150,100))
	msj1 = "Victorias: " + str(victorias)
	msj2 = "Derrotas: " + str(derrotas)
	texto1 = fuente.render(msj1,1,negro)
	texto2 = fuente.render(msj2,1,negro)
	win.blit(texto1,(350,25))
	win.blit(texto2,(600,25))
	pygame.display.update()

def elegirPalabra(palabras):
	if len(palabras) > 0:
		word = choice(palabras)
		palabras.remove(word)
		return word
	return "Ya no hay más palabras:("

def getPalabra(palabras):
	palabra = elegirPalabra(palabras)
	lista_palabra = []
	if ' ' not in palabra:
		for i in range(len(palabra)):
			lista_palabra.append('_ ')
	return lista_palabra,palabra
	
def trabajarPalabra(l,fuente,win,negro):
	#l = lista
	msj = ''
	for i in l:
		msj += i
	texto = fuente.render(msj,1,negro)
	win.blit(texto,(375,250))
	pygame.display.update()

def evaluar(letra,palabra_correcta,l):
	nueva_lista = list(l)
	if letra in palabra_correcta:
		indices = []
		for i in range(len(palabra_correcta)):
			if palabra_correcta[i] == letra:
				indices.append(i)
		for x in indices:
			nueva_lista[x] = letra + ' '
		if evaluarVictoria(nueva_lista):
			return 'victoria',nueva_lista
		return '',nueva_lista
	else:
		return "incorrecto",nueva_lista

def evaluarVictoria(lista):
	if '_ ' in lista:
		return False
	return True

def evaluarDerrota(fase):
	if fase == 6:
		return True
	return False

def crearBotones():
	Radio = 20
	Separacion = 15
	botones = []
	inicio_x = round((Ancho - 13*(Separacion + Radio * 2))/2)
	inicio_y = 400
	A = 65
	for i in range(26):
		x = inicio_x + Separacion * 2 + ((Separacion + Radio * 2) * (i % 13))
		y = inicio_y + (i//13) * (Separacion + Radio * 2)
		botones.append([x,y,chr(A +i),True])
	return botones

def continuar(win,blanco,fuente,negro):
	#dibujar las opciones en pantalla
	win.fill(blanco)
	msj = "¿Te gustaría seguir jugando?"
	texto = fuente.render(msj,1,negro)
	win.blit(texto,(200,100))
	radio = 50
	opciones = [(200,250,"SI"),(600,250,"NO")]
	for boton in opciones:
		x,y,opcion = boton
		pygame.draw.circle(win,negro,(x,y),radio,5)
		texto = fuente.render(opcion,1,negro)
		win.blit(texto,(x - texto.get_width()/2 , y - texto.get_height()/2))
	pygame.display.update()

	while True:
		for evento in pygame.event.get():
			
			if evento.type == pygame.QUIT:
				return False,False
			
			if evento.type == pygame.MOUSEBUTTONDOWN:
				clickX,clickY = pygame.mouse.get_pos()
				
				for boton in opciones:
					x,y,opcion = boton
					dist = sqrt(((x - clickX)**2 + (y - clickY)**2))
					if dist <= radio:
						if opcion == 'SI':
							return True,True
						else:
							return False,False

def delay(valor):
	time_final = pygame.time.get_ticks()
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return False
		nuevo_time = pygame.time.get_ticks()
		if nuevo_time - time_final >= valor:
			return True

def msjResultado(fuente,msj):
	texto = fuente.render(msj,1,negro)
	win.blit(texto,(425,300))
	pygame.display.update()

#variables constantes
pygame.init()
Ancho = 800
Largo = 500
win = pygame.display.set_mode((Ancho,Largo))
pygame.display.set_caption("Ahorcado")
blanco = (255,255,255)
negro = (0,0,0)
fps = 60
reloj = pygame.time.Clock()

#obtener imagenes
imagenes = []
for i in range(7):
	imagen = pygame.image.load("hangman" + str(i) + '.png')
	imagenes.append(imagen)

#variables de los botones
Radio = 20
botones = crearBotones()

#fuente de texto
fuente = pygame.font.SysFont("comicsans",40)

#variables del juego
estado = 0
nuevo_juego = True
jugando = True
victorias = 0
derrotas = 0

#lista de palabras
palabras = ["MATEMATICAS","FISICA","PROGRAMACION","ETICA","INSTITUTO","PYTHON","PRUEBA","UNIVERSIDAD","ESPERANZA","LIBRO","HELICOPTERO", "ASTRONAUTA",
		"SANGRE","SUERTE","FANTASMA","ESTRATEGIA","AUTOMOVIL","VELERO","INGLATERRA","INFIERNO","INVIERNO","ETERNO","MALVADO","DICCIONARIO","COMPUTADOR","DIARIO",
		"AMENAZA","EXTRATERRESTE","VIAJERO","TRIVIAL","EFIMERO","HIELO","AMOR","PAREJA","VERANO","FINLANDIA","PRIMAVERA","VACACIONES","LANZAMIENTO", "PRINCIPE",
		"GUERRA","TECNOLOGICO","DEFENSA","ATAQUE","KAISER","PIZZA","INGENIERIA","CALCULO","MAPA","BARCO","PREUNIVERSITARIO","RETORNO","GIGANTE","QUIMERICA","REBELDE",
		"VENERABLE","OLVIDADO","TENEBROSO","ABSOLUTO","IMPLACABLE","CONSIDERABLE","ALEATORIO","TOKIO","SANTIAGO","WASHINGTON","MOSCU","RITMO","JAZZ","ROCK","VIEJO",
		"EFICIENTE","VIENTO","LATIFUNDISTA","TERRORISTA","MONEDA","VALIENTE","INTEGRO","CALIENTE","CALISTENIA","FRIO","VELOCIDAD","ACELERACION","MENSAJE","ITALIA",
		"ROCA","JAZMIN","SECRETO","BONSAI","PEPSI","INFORMATICA","PANDEMIA","VIRUS","MUERTE","VERTICE","CUARENTENA","PROYECTO","MISTERIO","MOLOTOV","ILUSION","MOSCA",
		"PROGRESO","INNOVACION","PALETA","POLERA","TERMOMETRO","KARATE","FEDERICO","VENGADOR","MERCURIO","OXIGENO","AZUL","HIDROGENO","TRIANGULO","FUTURO","VACIO"]

#ciclo principal del juego
while nuevo_juego:
	reloj.tick(fps)
	cambio = True
	lista,word = getPalabra(palabras)
	
	if not jugando:
		nuevo_juego,jugando = continuar(win,blanco,fuente,negro)
		if nuevo_juego:
			botones = crearBotones()
			estado = 0
	
	if nuevo_juego and len(lista) == 0:
		dibujar(win,blanco,botones,imagenes,estado,negro,Radio,fuente,victorias,derrotas)
		trabajarPalabra(lista,fuente,win,negro)
		texto = fuente.render(word,1,negro)
		win.blit(texto,(400,250))
		pygame.display.update()
		pausa = delay(3000)
		nuevo_juego = False
		jugando = False
	
	while jugando:

		#cambio es necesario ya que de lo contrario se dibujaría cada segundo
		if cambio:
			dibujar(win,blanco,botones,imagenes,estado,negro,Radio,fuente,victorias,derrotas)
			trabajarPalabra(lista,fuente,win,negro)
		
		cambio = False
		
		#revisa los eventos del juegp, como los clicks
		for evento in pygame.event.get():
			#si el jugador presiona la x para cerrar el juego
			if evento.type == pygame.QUIT:
				nuevo_juego = False
				jugando = False
			#si el jugador clickea alguna parte de la pantalla
			if evento.type == pygame.MOUSEBUTTONDOWN:
				clickX,clickY = pygame.mouse.get_pos()
				#se determina si es que apretó un boton o no, comparandolo con el radio de los botones
				for boton in botones:
					x,y,letra,visible = boton
					dist = sqrt(((x - clickX)**2 + (y - clickY)**2))
					if dist <= Radio:
						boton[3] = False
						evaluacion,lista = evaluar(letra,word,lista)
						
						if evaluacion == 'victoria':
							victorias += 1
							jugando = False
							dibujar(win,blanco,botones,imagenes,estado,negro,Radio,fuente,victorias,derrotas)
							trabajarPalabra(lista,fuente,win,negro)
							msj = "Felicitaciones, ganaste!"
							msjResultado(fuente,msj)
							pausa = delay(2500)
							if not pausa:
								nuevo_juego = False
								jugando = False
						
						elif evaluacion == 'incorrecto':
							cambio = True
							estado += 1

						else:
							cambio = True
						
						if evaluarDerrota(estado):
							derrotas += 1
							jugando = False
							#le muestra al jugador la palabra correcta
							lista = []
							for letra in word:
								lista.append(letra + ' ')
							dibujar(win,blanco,botones,imagenes,estado,negro,Radio,fuente,victorias,derrotas)
							trabajarPalabra(lista,fuente,win,negro)
							msj = "Lo siento, perdiste"
							msjResultado(fuente,msj)
							pausa = delay(2500)
							if not pausa:
								nuevo_juego = False
								jugando = False
pygame.quit()
# interfaz.py
import pygame
import pygame_gui
import os

class Interfaz:
    def __init__(self, resolucion, manager_ui, ruta_fuente):
        self.resolucion = resolucion
        self.ruta_fuente = ruta_fuente
        
        # Guardamos la referencia del manager único
        self.manager = manager_ui

        # Elementos de la interfaz que se guardarán como atributos
        self.label_titulo = None
        self.boton_iniciar = None
        self.boton_pruebas = None
        self.boton_salir = None
        self.boton_volver = None

    def crear_menu_inicio(self):
        # Genera los componentes del menu
        ancho_titulo, alto_titulo = 500, 100
        x_titulo = self.resolucion[0] // 2 - ancho_titulo // 2
        y_titulo = 60
        
        # Cargamos la fuente para el renderizado del cartel
        if os.path.exists(self.ruta_fuente):
            fuente_titulo = pygame.font.Font(self.ruta_fuente, 30)
        else:
            fuente_titulo = pygame.font.SysFont("sans", 30, bold=True)

        # Creamos una superficie transparente donde poner el fondo de la bandera
        superficie_cartel = pygame.Surface((ancho_titulo, alto_titulo), pygame.SRCALPHA)

        # Dibujamos las tres franjas horizontales de la bandera (Celeste - Blanco - Celeste)
        pygame.draw.rect(superficie_cartel, (116, 172, 223), (0, 0, ancho_titulo, int(alto_titulo * 0.35)))
        pygame.draw.rect(superficie_cartel, (255, 255, 255), (0, int(alto_titulo * 0.35), ancho_titulo, int(alto_titulo * 0.30)))
        pygame.draw.rect(superficie_cartel, (116, 172, 223), (0, int(alto_titulo * 0.65), ancho_titulo, int(alto_titulo * 0.35)))

        # Renderizado del texto del título centrado sobre la bandera
        texto_renderizado = fuente_titulo.render("ISAAC ARGENTO v0.1", True, (10, 20, 40))
        texto_rect = texto_renderizado.get_rect(center=(ancho_titulo // 2, alto_titulo // 2))
        superficie_cartel.blit(texto_renderizado, texto_rect)

        # Configurado todo, se pasa al manager de UI
        self.label_titulo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((x_titulo, y_titulo), (ancho_titulo, alto_titulo)),
            image_surface=superficie_cartel,
            manager=self.manager
        )

        # Botones principales del menú
        self.boton_iniciar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.resolucion[0] // 2 - 120, 230), (240, 50)),
            text="JUGAR",
            manager=self.manager
        )

        self.boton_pruebas = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.resolucion[0] // 2 - 120, 300), (240, 50)),
            text="ENTORNO PRUEBAS HUD",
            manager=self.manager
        )

        self.boton_salir = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.resolucion[0] // 2 - 120, 370), (240, 50)),
            text="SALIR",
            manager=self.manager
        )

    def destruir_menu_inicio(self):
        """Elimina de forma segura los widgets del menú de la memoria del manager."""
        if self.label_titulo: self.label_titulo.kill()
        if self.boton_iniciar: self.boton_iniciar.kill()
        if self.boton_pruebas: self.boton_pruebas.kill()
        if self.boton_salir: self.boton_salir.kill()

    def crear_entorno_pruebas(self):
        self.boton_volver = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.resolucion[0] - 160, self.resolucion[1] - 60), (140, 40)),
            text="VOLVER AL MENÚ",
            manager=self.manager
        )

    def dibujar_prototipo_hud(self, pantalla):
        # Contenedor gris del HUD superior
        pygame.draw.rect(pantalla, (20, 20, 25), (0, 0, self.resolucion[0], 60))
        
        # Prototipo de corazones de vida (3 círculos rojos de prueba)
        for i in range(3):
            pygame.draw.circle(pantalla, (220, 40, 40), (30 + (i * 35), 30), 12)
            
        # Contador de monedas provisionales
        if os.path.exists(self.ruta_fuente):
            fuente_hud = pygame.font.Font(self.ruta_fuente, 18)
            texto_monedas = fuente_hud.render("MONEDAS: 99", True, (255, 215, 0))
            pantalla.blit(texto_monedas, (150, 20))
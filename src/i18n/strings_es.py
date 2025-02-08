"""Spanish strings for the application."""

STRINGS = {
    # Window and display
    'window.title': 'Simulación de Vida',
    'window.fps': 'FPS: {value}',
    'window.resolution': '{width}x{height}',

    # Game state strings
    'state.paused': 'PAUSADO',
    'state.running': 'EJECUTANDO',
    'state.press_h_for_help': 'Presiona H para ayuda',
    'state.controls': 'CONTROLES',
    'state.speed': 'Velocidad: {speed}x',
    'state.grid': 'Cuadrícula: {status}',
    'state.grid.on': 'ACTIVADA',
    'state.grid.off': 'DESACTIVADA',
    'state.language': 'Idioma: {lang}',
    
    # Control descriptions
    'controls.pause': 'Pausar/Reanudar simulación',
    'controls.help': 'Mostrar/Ocultar ayuda',
    'controls.grid': 'Alternar cuadrícula',
    'controls.speed': 'Ajustar velocidad',
    'controls.speed_up': 'Aumentar velocidad',
    'controls.speed_down': 'Disminuir velocidad',
    'controls.quit': 'Salir de la simulación',
    'controls.escape': 'Volver a la simulación',
    'controls.reset': 'Reiniciar simulación',
    'controls.language': 'Cambiar idioma',

    # Language names (keep these in their native form)
    'language.en': 'English',
    'language.es': 'Español',
    
    # Error messages
    'error.initialization': 'Error al inicializar la simulación',
    'error.renderer': 'Error al inicializar el renderizador',
    'error.display': 'No se pudo establecer el modo de pantalla: {error}',
    'error.font': 'Error al cargar la fuente: {error}',
    'error.file': 'No se pudo cargar el archivo: {path}',

    # Status messages
    'status.initializing': 'Inicializando simulación...',
    'status.loading': 'Cargando...',
    'status.saving': 'Guardando estado...',
    'status.ready': 'Listo',
    'status.plants': 'Plantas: {count}',
    'status.ground': 'Celdas de tierra: {count}',
    'status.time': 'Tiempo: {seconds:.1f}s',

    # Menu items
    'menu.file': 'Archivo',
    'menu.file.new': 'Nueva Simulación',
    'menu.file.save': 'Guardar Estado',
    'menu.file.load': 'Cargar Estado',
    'menu.file.quit': 'Salir',
    'menu.view': 'Ver',
    'menu.view.grid': 'Mostrar Cuadrícula',
    'menu.view.stats': 'Mostrar Estadísticas',
    'menu.help': 'Ayuda',
    'menu.help.controls': 'Controles',
    'menu.help.about': 'Acerca de',

    # Dialog titles
    'dialog.confirm': 'Confirmar',
    'dialog.warning': 'Advertencia',
    'dialog.error': 'Error',
    'dialog.quit': '¿Salir de la Simulación?',
    'dialog.reset': '¿Reiniciar Simulación?',
    
    # Dialog messages
    'dialog.quit.message': '¿Estás seguro de que quieres salir?',
    'dialog.reset.message': '¿Estás seguro de que quieres reiniciar? Se perderá todo el progreso.',
    'dialog.unsaved.message': 'Tienes cambios sin guardar. ¿Quieres guardar antes de continuar?',

    # Buttons
    'button.ok': 'Aceptar',
    'button.cancel': 'Cancelar',
    'button.yes': 'Sí',
    'button.no': 'No',
    'button.save': 'Guardar',
    'button.load': 'Cargar',
    'button.reset': 'Reiniciar',
    'button.close': 'Cerrar',

    # Statistics
    'stats.title': 'Estadísticas',
    'stats.fps': 'FPS: {value}',
    'stats.runtime': 'Tiempo de ejecución: {hours:02d}:{minutes:02d}:{seconds:02d}',
    'stats.cells': 'Total de Celdas: {value}',
    'stats.plants': 'Celdas de Plantas: {value}',
    'stats.ground': 'Celdas de Tierra: {value}',
    'stats.updates': 'Actualizaciones: {value}',
    'stats.memory': 'Uso de Memoria: {value:.1f} MB',

    # About section
    'about.title': 'Acerca de Life Simulation',
    'about.version': 'Versión {version}',
    'about.description': 'Una simulación de vida basada en una cuadrícula hexagonal que demuestra patrones y comportamientos celulares.',
    'about.copyright': '© 2024 Life Simulation Project',
    'about.license': 'Bajo Licencia MIT',
    'about.credits': 'Creado con Python y Pygame',
} 
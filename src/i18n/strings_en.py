"""Default English strings for the application."""

STRINGS = {
    # Window and display
    'window.title': 'Life Simulation',
    'window.fps': 'FPS: {value}',
    'window.resolution': '{width}x{height}',

    # Game state strings
    'state.paused': 'PAUSED',
    'state.running': 'RUNNING',
    'state.press_h_for_help': 'Press H for help',
    'state.controls': 'CONTROLS',
    'state.speed': 'Speed: {speed}x',
    'state.grid': 'Grid: {status}',
    'state.grid.on': 'ON',
    'state.grid.off': 'OFF',
    'state.language': 'Language: {lang}',
    
    # Control descriptions
    'controls.pause': 'Pause/Resume simulation',
    'controls.help': 'Show/Hide help',
    'controls.grid': 'Toggle grid visibility',
    'controls.speed': 'Adjust simulation speed',
    'controls.speed_up': 'Increase simulation speed',
    'controls.speed_down': 'Decrease simulation speed',
    'controls.quit': 'Quit simulation',
    'controls.escape': 'Return to simulation',
    'controls.reset': 'Reset simulation',
    'controls.language': 'Change language',

    # Language names (keep these in their native form)
    'language.en': 'English',
    'language.es': 'Español',
    
    # Error messages
    'error.initialization': 'Failed to initialize simulation',
    'error.renderer': 'Failed to initialize renderer',
    'error.display': 'Could not set display mode: {error}',
    'error.font': 'Failed to load font: {error}',
    'error.file': 'Could not load file: {path}',

    # Status messages
    'status.initializing': 'Initializing simulation...',
    'status.loading': 'Loading...',
    'status.saving': 'Saving state...',
    'status.ready': 'Ready',
    'status.plants': 'Plants: {count}',
    'status.ground': 'Ground cells: {count}',
    'status.time': 'Time: {seconds:.1f}s',

    # Menu items
    'menu.file': 'File',
    'menu.file.new': 'New Simulation',
    'menu.file.save': 'Save State',
    'menu.file.load': 'Load State',
    'menu.file.quit': 'Quit',
    'menu.view': 'View',
    'menu.view.grid': 'Show Grid',
    'menu.view.stats': 'Show Statistics',
    'menu.help': 'Help',
    'menu.help.controls': 'Controls',
    'menu.help.about': 'About',

    # Dialog titles
    'dialog.confirm': 'Confirm',
    'dialog.warning': 'Warning',
    'dialog.error': 'Error',
    'dialog.quit': 'Quit Simulation?',
    'dialog.reset': 'Reset Simulation?',
    
    # Dialog messages
    'dialog.quit.message': 'Are you sure you want to quit?',
    'dialog.reset.message': 'Are you sure you want to reset? All progress will be lost.',
    'dialog.unsaved.message': 'You have unsaved changes. Do you want to save before continuing?',

    # Buttons
    'button.ok': 'OK',
    'button.cancel': 'Cancel',
    'button.yes': 'Yes',
    'button.no': 'No',
    'button.save': 'Save',
    'button.load': 'Load',
    'button.reset': 'Reset',
    'button.close': 'Close',

    # Statistics
    'stats.title': 'Statistics',
    'stats.fps': 'FPS: {value}',
    'stats.runtime': 'Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}',
    'stats.cells': 'Total Cells: {value}',
    'stats.plants': 'Plant Cells: {value}',
    'stats.ground': 'Ground Cells: {value}',
    'stats.updates': 'Updates: {value}',
    'stats.memory': 'Memory Usage: {value:.1f} MB',

    # About section
    'about.title': 'About Life Simulation',
    'about.version': 'Version {version}',
    'about.description': 'A hexagonal grid-based life simulation demonstrating cellular patterns and behaviors.',
    'about.copyright': '© 2024 Life Simulation Project',
    'about.license': 'Licensed under MIT License',
    'about.credits': 'Created with Python and Pygame',
} 
"""Integration tests for i18n with game state management."""

import unittest
import pygame
from src.game_state import GameStateManager, GameState
from src.i18n.string_provider import StringProvider
from src.i18n.language_manager import Language
from src import i18n


class MockGameStringProvider(StringProvider):
    """Mock string provider for testing."""
    
    def get_string(self, key: str, default: str = None) -> str:
        """Return mock translations for game-related strings."""
        translations = {
            'controls.pause': 'MOCK_PAUSE',
            'controls.help': 'MOCK_HELP',
            'controls.grid': 'MOCK_GRID',
            'controls.speed': 'MOCK_SPEED',
            'controls.escape': 'MOCK_ESCAPE',
            'controls.quit': 'MOCK_QUIT',
            'state.paused': 'MOCK_PAUSED_STATE',
            'state.press_h_for_help': 'MOCK_PRESS_H',
            'state.controls': 'MOCK_CONTROLS_TITLE',
            'state.speed': 'MOCK_SPEED: {speed}',
            'state.grid': 'MOCK_GRID: {status}',
            'state.grid.on': 'MOCK_ON',
            'state.grid.off': 'MOCK_OFF',
        }
        return translations.get(key, f"MOCK_{key}" if default is None else default)


class TestI18NGameStateIntegration(unittest.TestCase):
    """Test cases for i18n integration with game state."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        # Store the initial language
        self.initial_language = i18n.get_current_language()
        # Set up our mock provider
        self.mock_provider = MockGameStringProvider()
        i18n.set_string_provider(self.mock_provider)
        # Create game state manager with mock translations
        self.manager = GameStateManager()

    def test_control_descriptions(self):
        """Test that control descriptions are properly translated."""
        expected_controls = [
            ('P', 'MOCK_PAUSE'),
            ('H', 'MOCK_HELP'),
            ('G', 'MOCK_GRID'),
            ('+/-', 'MOCK_SPEED'),
            ('ESC', 'MOCK_ESCAPE'),
            ('Q', 'MOCK_QUIT'),
        ]
        
        self.assertEqual(len(self.manager.controls), len(expected_controls))
        for actual, expected in zip(self.manager.controls, expected_controls):
            self.assertEqual(actual, expected)

    def test_grid_status_translation(self):
        """Test that grid status messages are properly translated."""
        # Test with grid on
        self.manager.show_grid = True
        grid_text = i18n.get_string('state.grid', 
                                  status=i18n.get_string('state.grid.on'))
        self.assertEqual(grid_text, 'MOCK_GRID: MOCK_ON')
        
        # Test with grid off
        self.manager.show_grid = False
        grid_text = i18n.get_string('state.grid',
                                  status=i18n.get_string('state.grid.off'))
        self.assertEqual(grid_text, 'MOCK_GRID: MOCK_OFF')

    def test_speed_display_translation(self):
        """Test that speed display is properly translated."""
        # Test at default speed
        speed_text = i18n.get_string('state.speed', speed='1.0')
        self.assertEqual(speed_text, 'MOCK_SPEED: 1.0')
        
        # Test after speed adjustment
        self.manager.adjust_speed(0.5)
        speed_text = i18n.get_string('state.speed', speed='1.5')
        self.assertEqual(speed_text, 'MOCK_SPEED: 1.5')

    def test_state_messages_translation(self):
        """Test that state-specific messages are properly translated."""
        # Test paused state message
        self.manager.toggle_pause()
        paused_text = i18n.get_string('state.paused')
        help_prompt = i18n.get_string('state.press_h_for_help')
        self.assertEqual(paused_text, 'MOCK_PAUSED_STATE')
        self.assertEqual(help_prompt, 'MOCK_PRESS_H')
        
        # Test help state message
        self.manager.toggle_help()
        controls_title = i18n.get_string('state.controls')
        self.assertEqual(controls_title, 'MOCK_CONTROLS_TITLE')

    def test_language_switch_effect(self):
        """Test that switching languages affects the game state display."""
        # First check with mock language
        self.assertEqual(self.manager.controls[0][1], 'MOCK_PAUSE')
        
        # Switch to Spanish
        i18n.switch_language(Language.SPANISH)
        new_manager = GameStateManager()
        self.assertEqual(new_manager.controls[0][1], 'Pausar/Reanudar simulación')

    def test_format_string_consistency(self):
        """Test that formatted strings maintain consistency across translations."""
        # Test in Spanish
        i18n.switch_language(Language.SPANISH)
        speed_es = i18n.get_string('state.speed', speed='2.0')
        
        # Test with mock provider
        i18n.set_string_provider(self.mock_provider)
        speed_mock = i18n.get_string('state.speed', speed='2.0')
        
        # Both should have the speed value in them
        self.assertIn('2.0', speed_es)
        self.assertIn('2.0', speed_mock)
        
        # The strings should be different
        self.assertNotEqual(speed_es, speed_mock)
        
        # Verify specific text in each version
        self.assertIn('Velocidad:', speed_es)
        self.assertIn('MOCK_SPEED:', speed_mock)

    def tearDown(self):
        """Clean up after each test method."""
        # Restore initial language
        i18n.switch_language(self.initial_language)
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 
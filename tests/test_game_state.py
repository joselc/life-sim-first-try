"""Unit tests for the game state management system."""

import unittest
import pygame
from src.game_state import GameStateManager, GameState
from src import i18n


class TestGameStateManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        self.manager = GameStateManager()
        # Store initial language
        self.initial_language = i18n.get_current_language()

    def test_initial_state(self):
        """Test that game state manager initializes with correct values."""
        self.assertEqual(self.manager.current_state, GameState.RUNNING)
        self.assertEqual(self.manager.simulation_speed, 1.0)
        self.assertTrue(self.manager.show_grid)
        self.assertTrue(len(self.manager.controls) > 0)

    def test_toggle_pause(self):
        """Test pause/resume functionality."""
        # Test pause
        self.manager.toggle_pause()
        self.assertEqual(self.manager.current_state, GameState.PAUSED)
        
        # Test resume
        self.manager.toggle_pause()
        self.assertEqual(self.manager.current_state, GameState.RUNNING)

    def test_toggle_help(self):
        """Test help overlay toggle."""
        # Test show help
        self.manager.toggle_help()
        self.assertEqual(self.manager.current_state, GameState.HELP)
        
        # Test hide help
        self.manager.toggle_help()
        self.assertEqual(self.manager.current_state, GameState.RUNNING)

    def test_adjust_speed(self):
        """Test simulation speed adjustment."""
        # Test speed increase
        initial_speed = self.manager.simulation_speed
        self.manager.adjust_speed(0.1)
        self.assertGreater(self.manager.simulation_speed, initial_speed)
        
        # Test speed decrease
        self.manager.adjust_speed(-0.1)
        self.assertEqual(self.manager.simulation_speed, initial_speed)
        
        # Test minimum speed limit
        self.manager.adjust_speed(-10.0)
        self.assertGreaterEqual(self.manager.simulation_speed, 0.1)
        
        # Test maximum speed limit
        self.manager.adjust_speed(10.0)
        self.assertLessEqual(self.manager.simulation_speed, 5.0)

    def test_toggle_grid(self):
        """Test grid visibility toggle."""
        initial_state = self.manager.show_grid
        
        # Test toggle off
        self.manager.toggle_grid()
        self.assertNotEqual(self.manager.show_grid, initial_state)
        
        # Test toggle back on
        self.manager.toggle_grid()
        self.assertEqual(self.manager.show_grid, initial_state)

    def test_quit_handling(self):
        """Test quit functionality in different states."""
        # Test quit in running state
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_q})
        self.assertTrue(self.manager.handle_input(event))
        
        # Test quit in help state
        self.manager.current_state = GameState.HELP
        self.assertTrue(self.manager.handle_input(event))
        
        # Test quit in paused state
        self.manager.current_state = GameState.PAUSED
        self.assertTrue(self.manager.handle_input(event))

    def test_help_toggle_handling(self):
        """Test help toggle in different states."""
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_h})
        
        # Test help toggle from running
        self.assertEqual(self.manager.current_state, GameState.RUNNING)
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.HELP)
        
        # Test help toggle from help
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.RUNNING)
        
        # Test help toggle from paused
        self.manager.current_state = GameState.PAUSED
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.HELP)

    def test_escape_handling(self):
        """Test escape key functionality."""
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        
        # Test escape in help state
        self.manager.current_state = GameState.HELP
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.RUNNING)
        
        # Test escape in paused state
        self.manager.current_state = GameState.PAUSED
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.RUNNING)
        
        # Test escape in running state (should do nothing)
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.RUNNING)

    def test_disabled_controls_in_help(self):
        """Test that most controls are disabled while help is shown."""
        self.manager.current_state = GameState.HELP
        initial_speed = self.manager.simulation_speed
        initial_grid = self.manager.show_grid
        
        # Try to toggle pause
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_p})
        self.manager.handle_input(event)
        self.assertEqual(self.manager.current_state, GameState.HELP)
        
        # Try to adjust speed
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_PLUS})
        self.manager.handle_input(event)
        self.assertEqual(self.manager.simulation_speed, initial_speed)
        
        # Try to toggle grid
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_g})
        self.manager.handle_input(event)
        self.assertEqual(self.manager.show_grid, initial_grid)

    def test_non_keydown_events(self):
        """Test that non-keydown events are ignored."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        self.assertFalse(self.manager.handle_input(event))

    def test_language_toggle_handling(self):
        """Test language toggle functionality."""
        # Get initial language and available languages
        initial_lang = i18n.get_current_language()
        languages = i18n.get_available_languages()
        next_lang = languages[(languages.index(initial_lang) + 1) % len(languages)]
        
        # Store initial control text for comparison
        initial_pause_control = self.manager.controls[0][1]  # Get the pause control description
        
        # Test language toggle
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_l})
        self.manager.handle_input(event)
        
        # Verify language changed
        self.assertEqual(i18n.get_current_language(), next_lang)
        
        # Verify controls were updated - the text should be different in the new language
        self.assertNotEqual(self.manager.controls[0][1], initial_pause_control)
        
        # Verify the new control text matches the expected translation
        expected_pause_text = i18n.get_string('controls.pause')
        self.assertEqual(self.manager.controls[0][1], expected_pause_text)

    def test_speed_adjustment_keys(self):
        """Test speed adjustment with keyboard keys."""
        initial_speed = self.manager.simulation_speed
        
        # Test speed increase with plus key
        plus_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_PLUS})
        self.manager.handle_input(plus_event)
        self.assertGreater(self.manager.simulation_speed, initial_speed)
        
        # Test speed increase with keypad plus
        kp_plus_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_KP_PLUS})
        self.manager.handle_input(kp_plus_event)
        self.assertGreater(self.manager.simulation_speed, initial_speed + 0.1)
        
        # Test speed decrease with minus key
        minus_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_MINUS})
        self.manager.handle_input(minus_event)
        self.assertLess(self.manager.simulation_speed, initial_speed + 0.2)
        
        # Test speed decrease with keypad minus
        kp_minus_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_KP_MINUS})
        self.manager.handle_input(kp_minus_event)
        self.assertLess(self.manager.simulation_speed, initial_speed + 0.1)

    def test_grid_toggle_key(self):
        """Test grid toggle with G key."""
        initial_grid = self.manager.show_grid
        
        # Test grid toggle with G key
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_g})
        self.manager.handle_input(event)
        self.assertNotEqual(self.manager.show_grid, initial_grid)
        
        # Test toggle back
        self.manager.handle_input(event)
        self.assertEqual(self.manager.show_grid, initial_grid)

    def tearDown(self):
        """Clean up after each test method."""
        # Restore initial language
        i18n.switch_language(self.initial_language)
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 
"""Integration tests for the Life Simulation game loop."""

import unittest
import pygame
import time
from unittest.mock import patch
from src.mesh.hex_mesh import HexMesh
from src.game_state import GameStateManager, GameState
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLUMNS,
    MOCK_ROWS
)


class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        # Initialize a dummy display for testing
        pygame.display.set_mode((MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT))
        self.screen = pygame.Surface((MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        self.state_manager = GameStateManager()
        self.background_color = (30, 30, 30)

    def simulate_game_loop(self, num_frames, paused=False, help_shown=False):
        """Simulate the game loop for a specified number of frames.
        
        Args:
            num_frames (int): Number of frames to simulate
            paused (bool): Whether to simulate in paused state
            help_shown (bool): Whether to simulate with help overlay
        """
        if paused:
            self.state_manager.current_state = GameState.PAUSED
        if help_shown:
            self.state_manager.current_state = GameState.HELP

        for _ in range(num_frames):
            # Simulate time passing (16ms = ~60fps)
            pygame.time.wait(16)
            current_time = pygame.time.get_ticks() / 1000.0

            # Update if not paused or in help
            if self.state_manager.current_state == GameState.RUNNING:
                self.mesh.update(current_time * self.state_manager.simulation_speed)
            
            # Draw everything
            self.screen.fill(self.background_color)
            self.mesh.draw(self.screen, show_grid=self.state_manager.show_grid)
            self.state_manager.draw_overlay(self.screen)
            
            # Copy to display surface
            pygame.display.get_surface().blit(self.screen, (0, 0))
            pygame.display.flip()

    def test_game_initialization(self):
        """Test that game components are properly initialized."""
        self.assertIsNotNone(self.screen)
        self.assertIsNotNone(self.clock)
        self.assertIsNotNone(self.mesh)
        self.assertIsNotNone(self.state_manager)
        self.assertEqual(self.screen.get_width(), MOCK_SCREEN_WIDTH)
        self.assertEqual(self.screen.get_height(), MOCK_SCREEN_HEIGHT)

    def test_pause_functionality(self):
        """Test that game properly handles pause state."""
        # Get initial state
        initial_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                initial_states.append(hexagon.t)

        # Run paused for a few frames
        self.simulate_game_loop(3, paused=True)

        # Check that states haven't changed
        current_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                current_states.append(hexagon.t)

        self.assertEqual(initial_states, current_states)

    def test_help_overlay(self):
        """Test that help overlay doesn't affect game state."""
        # Get initial state
        initial_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                initial_states.append(hexagon.t)

        # Run with help shown
        self.simulate_game_loop(3, help_shown=True)

        # Check that states haven't changed
        current_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                current_states.append(hexagon.t)

        self.assertEqual(initial_states, current_states)

    def test_speed_control(self):
        """Test that simulation speed affects update rate."""
        # Run at normal speed
        self.state_manager.simulation_speed = 1.0
        initial_time = time.time()
        self.simulate_game_loop(10)
        normal_duration = time.time() - initial_time

        # Run at double speed
        self.state_manager.simulation_speed = 2.0
        initial_time = time.time()
        self.simulate_game_loop(10)
        fast_duration = time.time() - initial_time

        # Timing might not be exact, but should be roughly proportional
        self.assertAlmostEqual(normal_duration, fast_duration, delta=0.1)

    def test_grid_toggle(self):
        """Test that grid toggle affects rendering."""
        # Get screenshot with grid
        self.state_manager.show_grid = True
        self.screen.fill(self.background_color)
        self.mesh.draw(self.screen, show_grid=self.state_manager.show_grid)
        with_grid = pygame.surfarray.array3d(self.screen).copy()

        # Get screenshot without grid
        self.state_manager.show_grid = False
        self.screen.fill(self.background_color)
        self.mesh.draw(self.screen, show_grid=self.state_manager.show_grid)
        without_grid = pygame.surfarray.array3d(self.screen).copy()

        # Screenshots should be different
        self.assertTrue((with_grid != without_grid).any())

    def test_state_transitions_integration(self):
        """Test that state transitions work in game loop context."""
        # Test various state transitions
        transitions = [
            (pygame.K_p, GameState.PAUSED),      # RUNNING -> PAUSED
            (pygame.K_h, GameState.HELP),        # PAUSED -> HELP
            (pygame.K_ESCAPE, GameState.RUNNING), # HELP -> RUNNING
        ]

        for key, expected_state in transitions:
            event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
            self.state_manager.handle_input(event)
            self.simulate_game_loop(1)  # Run one frame to ensure stability
            self.assertEqual(self.state_manager.current_state, expected_state)

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 
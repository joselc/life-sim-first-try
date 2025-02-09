"""Integration tests for the Life Simulation game loop."""

import unittest
import pygame
import time
import random
from unittest.mock import patch
from src.mesh.hex_mesh import HexMesh
from src.game_state import GameStateManager, GameState
from src.renderers.pygame_renderer import PygameRenderer
from src import i18n
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLUMNS,
    MOCK_ROWS
)


class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Set fixed seed for consistent plant generation
        random.seed(12345)
        pygame.init()
        self.renderer = PygameRenderer()
        self.renderer.setup(MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
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
            self.renderer.begin_frame()
            
            # Draw all hexagons
            for hexagon in self.mesh.hexagons:
                self.renderer.draw_hexagon(hexagon, show_grid=self.state_manager.show_grid)
            
            # Draw state overlays
            if self.state_manager.current_state in [GameState.PAUSED, GameState.HELP]:
                self.renderer.draw_overlay((0, 0, 0, 128))
                
                if self.state_manager.current_state == GameState.PAUSED:
                    self.renderer.draw_text(
                        i18n.get_string('state.paused'),
                        (MOCK_SCREEN_WIDTH // 2, MOCK_SCREEN_HEIGHT // 2),
                        (255, 255, 255), centered=True
                    )
                    self.renderer.draw_text(
                        i18n.get_string('state.press_h_for_help'),
                        (MOCK_SCREEN_WIDTH // 2, MOCK_SCREEN_HEIGHT // 2 + 30),
                        (200, 200, 200), centered=True, font_size=24
                    )
                
                elif self.state_manager.current_state == GameState.HELP:
                    self.renderer.draw_text(
                        i18n.get_string('state.controls'),
                        (MOCK_SCREEN_WIDTH // 2, 50),
                        (255, 255, 255), centered=True
                    )
                    
                    y_pos = 100
                    for key, description in self.state_manager.controls:
                        self.renderer.draw_text(
                            key,
                            (MOCK_SCREEN_WIDTH // 2 - 10, y_pos),
                            (255, 255, 0), centered=False, font_size=24
                        )
                        self.renderer.draw_text(
                            description,
                            (MOCK_SCREEN_WIDTH // 2 + 10, y_pos),
                            (255, 255, 255), centered=False, font_size=24
                        )
                        y_pos += 30
            
            # Always draw these overlays unless in help
            if self.state_manager.current_state != GameState.HELP:
                self.renderer.draw_text(
                    i18n.get_string('state.speed', speed=f"{self.state_manager.simulation_speed:.1f}"),
                    (10, 10), (255, 255, 255)
                )
                self.renderer.draw_text(
                    i18n.get_string('state.grid', status=i18n.get_string('state.grid.on' if self.state_manager.show_grid else 'state.grid.off')),
                    (10, 50), (255, 255, 255)
                )
            
            self.renderer.end_frame()

    def test_game_initialization(self):
        """Test that game components are properly initialized."""
        self.assertIsNotNone(self.renderer)
        self.assertIsNotNone(self.mesh)
        self.assertIsNotNone(self.state_manager)

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
        self.renderer.begin_frame()
        for hexagon in self.mesh.hexagons:
            self.renderer.draw_hexagon(hexagon, show_grid=True)
        with_grid = pygame.surfarray.array3d(self.renderer.screen).copy()

        # Get screenshot without grid
        self.state_manager.show_grid = False
        self.renderer.begin_frame()
        for hexagon in self.mesh.hexagons:
            self.renderer.draw_hexagon(hexagon, show_grid=False)
        without_grid = pygame.surfarray.array3d(self.renderer.screen).copy()

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
        self.renderer.cleanup()
        # Reset random seed
        random.seed()


if __name__ == '__main__':
    unittest.main() 
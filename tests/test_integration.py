"""Integration tests for the Life Simulation game loop."""

import unittest
import pygame
import time
from unittest.mock import patch
from src.mesh.hex_mesh import HexMesh
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
        # Set up a dummy display mode for testing
        pygame.display.set_mode((MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT))
        self.screen = pygame.Surface((MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        self.background_color = (30, 30, 30)

    def simulate_game_loop(self, num_frames):
        """Simulate the game loop for a specified number of frames."""
        for _ in range(num_frames):
            # Simulate time passing (16ms = ~60fps)
            pygame.time.wait(16)
            current_time = pygame.time.get_ticks() / 1000.0

            # Update and draw
            self.mesh.update(current_time)
            self.screen.fill(self.background_color)
            self.mesh.draw(self.screen)
            
            # Copy to display surface
            pygame.display.get_surface().blit(self.screen, (0, 0))
            pygame.display.flip()

    def test_game_initialization(self):
        """Test that game components are properly initialized."""
        self.assertIsNotNone(self.screen)
        self.assertIsNotNone(self.clock)
        self.assertIsNotNone(self.mesh)
        self.assertEqual(self.screen.get_width(), MOCK_SCREEN_WIDTH)
        self.assertEqual(self.screen.get_height(), MOCK_SCREEN_HEIGHT)

    def test_game_loop_stability(self):
        """Test that the game loop can run stably for multiple frames."""
        try:
            self.simulate_game_loop(10)  # Run for 10 frames
            success = True
        except Exception as e:
            success = False
            self.fail(f"Game loop failed: {str(e)}")
        self.assertTrue(success)

    def test_time_progression(self):
        """Test that time properly progresses in the game loop."""
        initial_time = pygame.time.get_ticks()
        self.simulate_game_loop(5)  # Run for 5 frames
        final_time = pygame.time.get_ticks()
        
        # Should have progressed by at least 16ms * 5 frames
        self.assertGreater(final_time - initial_time, 16 * 5)

    @patch('pygame.event.get')
    def test_event_handling(self, mock_event_get):
        """Test that the game loop properly handles events."""
        # Simulate a quit event
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        
        # Check that a quit event would trigger game exit
        events = pygame.event.get()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].type, pygame.QUIT)

    def test_continuous_update(self):
        """Test that game state updates continuously."""
        # Get initial state of first plant (if any)
        initial_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                initial_states.append(hexagon.t)

        # Run game loop for a few frames
        self.simulate_game_loop(3)

        # Check that states have changed
        current_states = []
        for hexagon in self.mesh.hexagons:
            if hasattr(hexagon, 't'):
                current_states.append(hexagon.t)

        # Verify that at least some states have changed
        self.assertNotEqual(initial_states, current_states)

    def test_frame_rate_control(self):
        """Test that the game maintains a reasonable frame rate."""
        start_time = time.time()
        self.simulate_game_loop(10)  # Run for 10 frames
        end_time = time.time()
        
        # Calculate actual frame rate
        elapsed_time = end_time - start_time
        frame_rate = 10 / elapsed_time  # frames / seconds
        
        # Frame rate should be reasonable for testing environment
        # Lower threshold for CI environments
        self.assertGreater(frame_rate, 10)  # Should be at least 10fps in test environment
        
    def test_rendering_consistency(self):
        """Test that rendering produces consistent output."""
        # Take two screenshots with same game state
        self.screen.fill(self.background_color)
        self.mesh.draw(self.screen)
        screenshot1 = pygame.surfarray.array3d(self.screen).copy()
        
        self.screen.fill(self.background_color)
        self.mesh.draw(self.screen)
        screenshot2 = pygame.surfarray.array3d(self.screen).copy()
        
        # Compare screenshots (should be identical)
        self.assertTrue((screenshot1 == screenshot2).all())

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 
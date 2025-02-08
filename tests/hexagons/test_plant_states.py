"""Unit tests for the plant state management system."""

import unittest
from src.hexagons.plant_states import PlantState, PlantStateManager


class TestPlantStateManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = PlantStateManager()

    def test_initialization(self):
        """Test that state manager initializes with correct values."""
        self.assertEqual(self.manager.state, PlantState.SEED)
        self.assertEqual(self.manager.time_in_state, 0.0)
        self.assertEqual(self.manager.health, 1.0)
        self.assertEqual(self.manager.growth, 0.0)

    def test_seed_to_growing_transition(self):
        """Test transition from seed to growing state after SEED_DURATION."""
        self.assertEqual(self.manager.state, PlantState.SEED)
        # Update with less than SEED_DURATION
        self.manager.update(0.1)
        self.assertEqual(self.manager.state, PlantState.SEED)
        # Update past SEED_DURATION
        self.manager.update(self.manager.SEED_DURATION)
        self.assertEqual(self.manager.state, PlantState.GROWING)
        self.assertEqual(self.manager.time_in_state, 0.0)

    def test_growth_progression(self):
        """Test that growth progresses correctly over time."""
        # Get to growing state
        self.manager.update(self.manager.SEED_DURATION + 0.1)
        self.assertEqual(self.manager.state, PlantState.GROWING)

        # Partial growth
        self.manager.update(self.manager.GROWTH_THRESHOLD / 2)
        self.assertEqual(self.manager.state, PlantState.GROWING)
        self.assertAlmostEqual(self.manager.growth, 0.5, places=2)

        # Complete growth
        self.manager.update(self.manager.GROWTH_THRESHOLD / 2)
        self.assertEqual(self.manager.state, PlantState.MATURE)
        self.assertEqual(self.manager.growth, 1.0)

    def test_mature_to_dying_transition(self):
        """Test transition from mature to dying state."""
        # Get to mature state
        self.manager.update(self.manager.SEED_DURATION + 0.1)  # Seed -> Growing
        self.manager.update(self.manager.GROWTH_THRESHOLD)  # Complete growth
        self.assertEqual(self.manager.state, PlantState.MATURE)

        # Not enough time passed for dying
        self.manager.update(self.manager.MATURE_MAX_TIME - 0.1)
        self.assertEqual(self.manager.state, PlantState.MATURE)

        # Enough time passed, should start dying
        self.manager.update(0.2)  # Push over the threshold
        self.assertEqual(self.manager.state, PlantState.DYING)

    def test_dying_progression(self):
        """Test that health decreases correctly while dying."""
        # Get to dying state
        self.manager.update(self.manager.SEED_DURATION + 0.1)  # Seed -> Growing
        self.manager.update(self.manager.GROWTH_THRESHOLD)  # Complete growth
        self.manager.update(self.manager.MATURE_MAX_TIME + 0.1)  # Start dying
        self.assertEqual(self.manager.state, PlantState.DYING)
        self.assertEqual(self.manager.health, 1.0)

        # Half-way through dying
        self.manager.update(self.manager.DYING_DURATION / 2)
        self.assertAlmostEqual(self.manager.health, 0.5, places=2)

        # Complete death
        self.manager.update(self.manager.DYING_DURATION / 2)
        self.assertEqual(self.manager.state, PlantState.DEAD)
        self.assertEqual(self.manager.health, 0.0)

    def test_color_factor(self):
        """Test that color factor is appropriate for each state."""
        # Seed state
        self.assertEqual(self.manager.color_factor, 0.0)

        # Growing state
        self.manager.update(self.manager.SEED_DURATION + 0.1)  # Start growing
        self.manager.update(self.manager.GROWTH_THRESHOLD / 2)  # Half growth
        self.assertAlmostEqual(self.manager.color_factor, 0.5, places=2)

        # Mature state
        self.manager.update(self.manager.GROWTH_THRESHOLD / 2)  # Complete growth
        self.assertEqual(self.manager.color_factor, 1.0)

        # Dying state
        self.manager.update(self.manager.MATURE_MAX_TIME + 0.1)  # Start dying
        self.manager.update(self.manager.DYING_DURATION / 2)  # Half dead
        self.assertAlmostEqual(self.manager.color_factor, 0.5, places=2)

        # Dead state
        self.manager.update(self.manager.DYING_DURATION / 2)  # Complete death
        self.assertEqual(self.manager.color_factor, 0.0)

    def test_time_tracking(self):
        """Test that time in state is tracked correctly."""
        # Time in seed state
        initial_time = 0.5
        self.manager.update(initial_time)
        self.assertEqual(self.manager.time_in_state, initial_time)

        # Time in growing state (after transition)
        self.manager.update(self.manager.SEED_DURATION)  # Trigger transition
        self.assertEqual(self.manager.time_in_state, 0.0)  # Should reset after transition

        # Accumulate more time
        growth_time = 0.3
        self.manager.update(growth_time)
        self.assertEqual(self.manager.time_in_state, growth_time)

    def test_state_sequence(self):
        """Test that states always follow the correct sequence."""
        states_seen = []
        last_state = None
        
        # Run through entire lifecycle with smaller time steps
        while self.manager.state != PlantState.DEAD:
            current_state = self.manager.state
            # Only record state when it changes
            if current_state != last_state:
                states_seen.append(current_state)
                last_state = current_state
            self.manager.update(0.5)  # Larger time step for quicker transitions

        # Add final state
        if self.manager.state not in states_seen:
            states_seen.append(PlantState.DEAD)
        
        # Verify sequence
        expected_sequence = [
            PlantState.SEED,
            PlantState.GROWING,
            PlantState.MATURE,
            PlantState.DYING,
            PlantState.DEAD
        ]
        
        self.assertEqual(states_seen, expected_sequence)


if __name__ == '__main__':
    unittest.main() 
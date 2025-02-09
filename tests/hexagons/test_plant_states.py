"""Unit tests for the plant state management system."""

import unittest
from unittest.mock import patch
from src.hexagons.plant_states import PlantState, PlantStateManager
from src.config import SEED_SURVIVAL_THRESHOLD, PLANT_FLOWERING_PROBABILITY


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
        self.assertEqual(self.manager.seed_survival_threshold, SEED_SURVIVAL_THRESHOLD)
        self.assertEqual(self.manager.flowering_probability, PLANT_FLOWERING_PROBABILITY)

    def test_seed_survival_check(self):
        """Test that seed survival check works correctly."""
        # Test with random value below threshold (survives)
        with patch('random.random', return_value=0.5):
            self.manager.seed_survival_threshold = 0.7
            self.assertTrue(self.manager._check_seed_survival())

        # Test with random value above threshold (dies)
        with patch('random.random', return_value=0.8):
            self.manager.seed_survival_threshold = 0.7
            self.assertFalse(self.manager._check_seed_survival())

        # Test edge cases
        with patch('random.random', return_value=0.0):
            self.manager.seed_survival_threshold = 0.1
            self.assertTrue(self.manager._check_seed_survival())  # Just survives

        with patch('random.random', return_value=1.0):
            self.manager.seed_survival_threshold = 0.9
            self.assertFalse(self.manager._check_seed_survival())  # Just dies

    def test_seed_survival_transition(self):
        """Test state transitions based on seed survival."""
        # Test survival case
        with patch('random.random', return_value=0.5):
            self.manager.seed_survival_threshold = 0.7  # Will survive
            self.assertEqual(self.manager.state, PlantState.SEED)
            self.manager.update(self.manager.SEED_DURATION + 0.1)  # Trigger check
            self.assertEqual(self.manager.state, PlantState.GROWING)
            self.assertEqual(self.manager.time_in_state, 0.0)

        # Test death case
        manager2 = PlantStateManager()  # Fresh instance for death test
        with patch('random.random', return_value=0.9):
            manager2.seed_survival_threshold = 0.7  # Will die
            self.assertEqual(manager2.state, PlantState.SEED)
            manager2.update(manager2.SEED_DURATION + 0.1)  # Trigger check
            self.assertEqual(manager2.state, PlantState.DYING)
            self.assertEqual(manager2.time_in_state, 0.0)

    def test_seed_death_progression(self):
        """Test that a dying seed progresses through states correctly."""
        with patch('random.random', return_value=0.9):  # Will die
            self.manager.seed_survival_threshold = 0.7
            
            # Progress to dying state
            self.manager.update(self.manager.SEED_DURATION + 0.1)
            self.assertEqual(self.manager.state, PlantState.DYING)
            self.assertEqual(self.manager.health, 1.0)  # Starts with full health
            
            # Half-way through dying
            self.manager.update(self.manager.DYING_DURATION / 2)
            self.assertEqual(self.manager.state, PlantState.DYING)
            self.assertAlmostEqual(self.manager.health, 0.5, places=2)
            
            # Complete death
            self.manager.update(self.manager.DYING_DURATION / 2)
            self.assertEqual(self.manager.state, PlantState.DEAD)
            self.assertEqual(self.manager.health, 0.0)

    def test_seed_survival_threshold_validation(self):
        """Test that seed survival threshold validates input correctly."""
        # Test valid values
        valid_values = [0.0, 0.5, 1.0]
        for value in valid_values:
            self.manager.seed_survival_threshold = value
            self.assertEqual(self.manager.seed_survival_threshold, value)

        # Test invalid values
        invalid_values = [-0.1, 1.1, -1, 2]
        for value in invalid_values:
            with self.assertRaises(ValueError):
                self.manager.seed_survival_threshold = value

    def test_seed_survival_threshold_persistence(self):
        """Test that seed survival threshold persists through state changes."""
        # Change threshold
        new_threshold = 0.8
        self.manager.seed_survival_threshold = new_threshold
        
        # Progress through states
        self.manager.update(self.manager.SEED_DURATION + 0.1)  # To GROWING
        self.assertEqual(self.manager.seed_survival_threshold, new_threshold)
        
        self.manager.update(self.manager.GROWTH_THRESHOLD)  # To MATURE
        self.assertEqual(self.manager.seed_survival_threshold, new_threshold)
        
        self.manager.update(self.manager.MATURE_MAX_TIME + 0.1)  # To DYING
        self.assertEqual(self.manager.seed_survival_threshold, new_threshold)
        
        self.manager.update(self.manager.DYING_DURATION)  # To DEAD
        self.assertEqual(self.manager.seed_survival_threshold, new_threshold)

    def test_seed_to_growing_transition(self):
        """Test transition from seed to growing state after SEED_DURATION."""
        with patch('random.random', return_value=0.5):  # Will survive with default threshold of 0.7
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
        with patch('random.random', return_value=0.5):  # Will survive with default threshold
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
        # Start in mature state
        with patch('random.random', return_value=0.9):  # Won't flower
            self.manager.state = PlantState.MATURE
            self.manager.time_in_state = self.manager.MATURE_MAX_TIME * 0.8  # Past flowering check
            self.manager.flowering_probability = 0.3

            # Update past max time
            self.manager.update(self.manager.MATURE_MAX_TIME * 0.5)  # Push well past max time
            self.assertEqual(self.manager.state, PlantState.DYING)
            self.assertEqual(self.manager.time_in_state, 0.0)

    def test_dying_progression(self):
        """Test that dying state progresses correctly."""
        # Start in dying state
        self.manager.state = PlantState.DYING
        self.manager.time_in_state = 0.0
        self.manager.health = 1.0

        # Update halfway through dying duration
        self.manager.update(self.manager.DYING_DURATION / 2)
        self.assertEqual(self.manager.state, PlantState.DYING)
        self.assertAlmostEqual(self.manager.health, 0.5, places=2)

        # Complete death
        self.manager.update(self.manager.DYING_DURATION / 2)
        self.assertEqual(self.manager.state, PlantState.DEAD)
        self.assertEqual(self.manager.health, 0.0)

    def test_color_factor(self):
        """Test that color factor returns correct values for each state."""
        # Test SEED state
        self.assertEqual(self.manager.color_factor, 0.0)

        # Test GROWING state
        self.manager.state = PlantState.GROWING
        self.manager.growth = 0.5
        self.assertEqual(self.manager.color_factor, 0.5)

        # Test MATURE state
        self.manager.state = PlantState.MATURE
        self.assertEqual(self.manager.color_factor, 1.0)

        # Test FLOWERING state
        self.manager.state = PlantState.FLOWERING
        self.assertEqual(self.manager.color_factor, 1.0)

        # Test DYING state
        self.manager.state = PlantState.DYING
        self.manager.health = 0.7
        self.assertEqual(self.manager.color_factor, 0.7)

        # Test DEAD state
        self.manager.state = PlantState.DEAD
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
        with patch('random.random', return_value=0.5):  # Will survive with default threshold
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

    def test_flowering_probability_validation(self):
        """Test that flowering probability validates input correctly."""
        # Test valid values
        valid_values = [0.0, 0.5, 1.0]
        for value in valid_values:
            self.manager.flowering_probability = value
            self.assertEqual(self.manager.flowering_probability, value)

        # Test invalid values
        invalid_values = [-0.1, 1.1, -1, 2]
        for value in invalid_values:
            with self.assertRaises(ValueError):
                self.manager.flowering_probability = value

    def test_flowering_check(self):
        """Test that flowering check works correctly."""
        # Test with random value below threshold (will flower)
        with patch('random.random', return_value=0.2):
            self.manager.flowering_probability = 0.3
            self.assertTrue(self.manager._check_flowering())

        # Test with random value above threshold (won't flower)
        with patch('random.random', return_value=0.4):
            self.manager.flowering_probability = 0.3
            self.assertFalse(self.manager._check_flowering())

    def test_mature_to_flowering_transition(self):
        """Test transition from mature to flowering state."""
        # Get to mature state
        with patch('random.random', return_value=0.5):  # Will survive seed phase
            self.manager.update(self.manager.SEED_DURATION + 0.1)  # Seed -> Growing
            self.manager.update(self.manager.GROWTH_THRESHOLD)  # Complete growth
            self.assertEqual(self.manager.state, PlantState.MATURE)

            # Update to just before flowering check point (75% of mature time)
            self.manager.update(self.manager.MATURE_MAX_TIME * 0.74)
            self.assertEqual(self.manager.state, PlantState.MATURE)

            # Update past flowering check point with high probability
            with patch('random.random', return_value=0.2):  # Will flower
                self.manager.flowering_probability = 0.3
                self.manager.update(self.manager.MATURE_MAX_TIME * 0.02)  # Just past check point
                self.assertEqual(self.manager.state, PlantState.FLOWERING)
                self.assertEqual(self.manager.time_in_state, 0.0)

    def test_no_flowering_transition(self):
        """Test that plant can go directly to dying if not flowering."""
        # Start in mature state
        with patch('random.random', return_value=0.9):  # Won't flower
            self.manager.state = PlantState.MATURE
            self.manager.time_in_state = self.manager.MATURE_MAX_TIME * 0.8  # Past flowering check
            self.manager.flowering_probability = 0.3

            # Update past max time
            self.manager.update(self.manager.MATURE_MAX_TIME * 0.5)  # Push well past max time
            self.assertEqual(self.manager.state, PlantState.DYING)
            self.assertEqual(self.manager.time_in_state, 0.0)

    def test_flowering_duration(self):
        """Test that flowering state lasts for the correct duration."""
        # Get to flowering state
        with patch('random.random', return_value=0.2):  # Will survive and flower
            self.manager.flowering_probability = 0.3
            self.manager.update(self.manager.SEED_DURATION + 0.1)  # Seed -> Growing
            self.manager.update(self.manager.GROWTH_THRESHOLD)  # Complete growth
            self.manager.update(self.manager.MATURE_MAX_TIME * 0.76)  # Trigger flowering check
            self.assertEqual(self.manager.state, PlantState.FLOWERING)

            # Update with less than flowering duration
            self.manager.update(self.manager.FLOWERING_DURATION * 0.9)
            self.assertEqual(self.manager.state, PlantState.FLOWERING)

            # Update past flowering duration
            self.manager.update(self.manager.FLOWERING_DURATION * 0.2)
            self.assertEqual(self.manager.state, PlantState.DYING)

    def test_flowering_state_sequence(self):
        """Test that flowering follows the correct state sequence."""
        with patch('random.random', return_value=0.2):  # Will survive and flower
            self.manager.flowering_probability = 0.3
            states_seen = []
            last_state = None

            # Run through entire lifecycle with smaller time steps
            while self.manager.state != PlantState.DEAD:
                current_state = self.manager.state
                # Only record state when it changes
                if current_state != last_state:
                    states_seen.append(current_state)
                    last_state = current_state
                self.manager.update(0.5)

            # Add final state if not already recorded
            if self.manager.state not in states_seen:
                states_seen.append(PlantState.DEAD)

            # Verify sequence includes flowering
            expected_sequence = [
                PlantState.SEED,
                PlantState.GROWING,
                PlantState.MATURE,
                PlantState.FLOWERING,
                PlantState.DYING,
                PlantState.DEAD
            ]

            self.assertEqual(states_seen, expected_sequence)


if __name__ == '__main__':
    unittest.main() 
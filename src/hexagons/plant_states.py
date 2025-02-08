"""Plant states and state management for the life simulation."""

from enum import Enum, auto


class PlantState(Enum):
    """States that a plant can be in during its lifecycle.
    
    States:
        SEED: Initial state, not yet grown
        GROWING: Plant is growing but not mature
        MATURE: Plant is fully grown and healthy
        DYING: Plant is losing health and will eventually die
        DEAD: Plant has died and will be replaced by ground
    """
    SEED = auto()
    GROWING = auto()
    MATURE = auto()
    DYING = auto()
    DEAD = auto()


class PlantStateManager:
    """Manages state transitions and behaviors for plants.
    
    This class handles the rules for how plants transition between states
    and what behaviors they exhibit in each state.
    
    Attributes:
        state (PlantState): Current state of the plant
        time_in_state (float): How long the plant has been in current state
        health (float): Plant's health from 0.0 to 1.0
        growth (float): Plant's growth progress from 0.0 to 1.0
    """
    
    # State transition thresholds
    GROWTH_THRESHOLD = 1.0  # Time needed to reach mature state
    MATURE_MAX_TIME = 5.0   # Maximum time before dying starts
    DYING_DURATION = 3.0    # How long it takes to die
    
    def __init__(self):
        """Initialize the plant state manager."""
        self.state = PlantState.SEED
        self.time_in_state = 0.0
        self.health = 1.0
        self.growth = 0.0
    
    def update(self, dt: float) -> None:
        """Update the plant's state based on time passed.
        
        Args:
            dt (float): Time passed since last update in seconds
        """
        self.time_in_state += dt
        
        if self.state == PlantState.SEED:
            # Start growing immediately
            self.state = PlantState.GROWING
            self.time_in_state = 0.0
            
        elif self.state == PlantState.GROWING:
            # Update growth progress
            self.growth = min(1.0, self.time_in_state / self.GROWTH_THRESHOLD)
            if self.growth >= 1.0:
                self.state = PlantState.MATURE
                self.time_in_state = 0.0
                
        elif self.state == PlantState.MATURE:
            # After max time, start dying
            if self.time_in_state > self.MATURE_MAX_TIME:
                self.state = PlantState.DYING
                self.time_in_state = 0.0
                
        elif self.state == PlantState.DYING:
            # Gradually reduce health until death
            self.health = max(0.0, 1.0 - (self.time_in_state / self.DYING_DURATION))
            if self.health <= 0:
                self.state = PlantState.DEAD
                self.time_in_state = 0.0
    
    @property
    def color_factor(self) -> float:
        """Get the color interpolation factor based on state.
        
        Returns:
            float: Factor from 0.0 to 1.0 for color interpolation
        """
        if self.state == PlantState.GROWING:
            return self.growth
        elif self.state == PlantState.MATURE:
            return 1.0
        elif self.state == PlantState.DYING:
            return self.health
        elif self.state == PlantState.DEAD:
            return 0.0
        return 0.0 
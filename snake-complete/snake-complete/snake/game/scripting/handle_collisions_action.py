import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point


class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score and moves the food if the snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score = cast.get_first_actor("scores")
        food = cast.get_first_actor("foods")

        snake1 = cast.get_first_actor("snake")
        head1 = snake1.get_head()
        
        snake2 = cast.get_second_actor("snake")
        head2 = snake2.get_head()

        if head1.get_position().equals(food.get_position()):
            points = food.get_points()
            snake1.grow_tail(points)
            score.add_points(points)
            food.reset()

        if head2.get_position().equals(food.get_position()):
            points = food.get_points()
            snake2.grow_tail(points)
            score.add_points(points)
            food.reset()
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        snake1 = cast.get_first_actor("snake")
        head1 = snake1.get_segments()[0]
        segments1 = snake1.get_segments()[1:]

        snake2 = cast.get_second_actor("snake")
        head2 = snake2.get_segments()[0]
        segments2 = snake2.get_segments()[1:]
        
        for segment in segments1:
            if head1.get_position().equals(segment.get_position()):
                x = int(constants.MAX_X / 2)
                y = int(constants.MAX_Y / 2)
                position = Point(x, y)

                message = Actor()
                message.set_text("Game Over! Green Snake Wins!")
                message.set_position(position)
                cast.add_actor("messages", message)
                self._is_game_over = True

            elif head2.get_position().equals(segment.get_position()):
                x = int(constants.MAX_X / 2)
                y = int(constants.MAX_Y / 2)
                position = Point(x, y)

                message = Actor()
                message.set_text("Game Over! Green Snake Wins!")
                message.set_position(position)
                cast.add_actor("messages", message)
                self._is_game_over = True
        
        for segment in segments2:
            if head2.get_position().equals(segment.get_position()):
                x = int(constants.MAX_X / 2)
                y = int(constants.MAX_Y / 2)
                position = Point(x, y)

                message = Actor()
                message.set_text("Game Over! Red Snake Wins!")
                message.set_position(position)
                cast.add_actor("messages", message)
                self._is_game_over = True

            elif head1.get_position().equals(segment.get_position()):
                x = int(constants.MAX_X / 2)
                y = int(constants.MAX_Y / 2)
                position = Point(x, y)

                message = Actor()
                message.set_text("Game Over! Red Snake Wins!")
                message.set_position(position)
                cast.add_actor("messages", message)
                self._is_game_over = True
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snake1 = cast.get_first_actor("snake")
            segments1 = snake1.get_segments()

            snake2 = cast.get_second_actor("snake")
            segments2 = snake2.get_segments()
            
            food = cast.get_first_actor("foods")

            for segment in segments1:
                segment.set_color(constants.WHITE)
            food.set_color(constants.WHITE)

            for segment in segments2:
                segment.set_color(constants.WHITE)
            food.set_color(constants.WHITE)
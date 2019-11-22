
import random

from maze import Goody, Baddy, Position, UP, DOWN, LEFT, RIGHT, STAY, \
    STEP, PING


class StaticGoody(Goody):

    ''' A static goody - does not move from its initial position '''

    def take_turn(self, _obstruction, _ping_response):
        ''' Stay where we are '''

        return STAY


class RandomGoody(Goody):

    ''' A random-walking goody '''

    def take_turn(self, obstruction, _ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''

        possibilities = [PING]
        for direction in [UP, DOWN, LEFT, RIGHT]:  # STEP.keys()
            if not obstruction[direction]:
                possibilities.append(direction)
        return random.choice(possibilities)


class GreedyGoody(Goody):

    ''' A goddy that pings once and then walks towards the other goody.  '''

    last_ping_response = None

    def vector_len_2(self, vector):
        return vector.x * vector.x + vector.y * vector.y

    def take_turn(self, obstruction, ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''

        if ping_response is not None:
            self.last_ping_response = ping_response

        if self.last_ping_response is None:

            # If we don't know where the other goody is, then send a ping so that we can find out.


            return PING

        (friend, ) = [player for player in
                      self.last_ping_response.keys()
                      if isinstance(player, Goody) and player
                      is not self]
        (foe, ) = [player for player in self.last_ping_response.keys()
                   if isinstance(player, Baddy)]

        # For the four possible moves, find the resulting distance to our friend after each one:

        last_known_friend_position = self.last_ping_response[friend]
        len_and_dirs = []

        for direction in [UP, DOWN, LEFT, RIGHT]:  # STEP.keys()

            # Choose the one that takes us closest to the our friend

            if not obstruction[direction]:

                # STEP[direction] turns the direction label into a vector (dx, dy) which we can add
                # to a Position (another vector):

                new_vector = last_known_friend_position \
                    - STEP[direction]
                entry = [direction, new_vector,
                         self.vector_len_2(new_vector)]
                len_and_dirs.append(entry)

        len_and_dirs.sort(key=lambda len_and_dir: len_and_dir[2])


        return len_and_dirs[0][0]


class WhateverGoody(Goody):

    last_ping_response = None

    ping_probability = 0.25

    strength = .65

    scaling = 20

    new_direction = (1, 0)



    def vector_len_2(self, vector):
        return vector.x * vector.x + vector.y * vector.y

    def vector_norm(self, vector):
        return (vector[0] ** 2 + vector[1] ** 2) ** .5

    def vector_add(self, v1, v2):
        return (v1[0] + v2[0], v1[1] + v2[1])

    def vector_diff(self, v1, v2):
        return (v1[0] - v2[0], v1[1] - v2[1])

    def vector_mult(self, vector, mult):
        return (vector[0] * mult ,vector[1] * mult)

    def take_turn(self, obstruction, ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''

        if ping_response is not None:
            self.last_ping_response = ping_response
            (last_friend_location, ) = [self.last_ping_response[player]
                    for player in self.last_ping_response.keys()
                    if isinstance(player, Goody) and player is not self]
            print(last_friend_location)
            x0=last_friend_location.x
            y0 = last_friend_location.y

            (last_enemy_location, ) = [self.last_ping_response[player]
                    for player in self.last_ping_response.keys()
                    if isinstance(player, Baddy)]
            x2 = last_enemy_location.x
            y2 = last_enemy_location.y


            x1 = 0
            y1 = 0

            attraction_direction = \
                self.vector_diff((x0,y0), (0,0))

            L = ((x1 - x2)*(x1 - x0) + (y1 - y2)*(y1 - y0)) / ((x1 - x0) ** 2+ (y1 - y0) ** 2)

            x = L * x0 + (1 - L) * x1
            y = L * y0 + (1 - L) * y1

            repulsion_vector_unmod = (x - x2, y - y2)
            repulsion_length = ((x - x2) ** 2 + (y - y2) ** 2) ** .5
            inverse_length = self.scaling / (1 + repulsion_length)
            repulsion_vector = self.vector_mult(repulsion_vector_unmod,
                    inverse_length)
            print(repulsion_vector)
            new_direction_unmod = self.vector_add(repulsion_vector,
                    attraction_direction)
            self.new_direction = self.vector_mult(new_direction_unmod, 1
                    / self.vector_norm(new_direction_unmod))

        if random.random() < self.ping_probability:
            return PING

        sampled = random.random()
        strength = self.strength
        if sampled < self.new_direction[0] ** 2 * strength:
            move = (LEFT if self.new_direction[0] < 0 else RIGHT)
        elif sampled < self.new_direction[0] ** 2:
            move = (RIGHT if self.new_direction[0] < 0 else LEFT)
        elif sampled < self.new_direction[0] ** 2 + self.new_direction[1] ** 2 \
            * strength:
            move = (DOWN if self.new_direction[1] < 0 else UP)
        else:
            move = (UP if self.new_direction[1] < 0 else DOWN)

        if not obstruction[move]:
	        return move
        else:
            possibilities = []
            for direction in [UP, DOWN, LEFT, RIGHT]:
                if not obstruction[direction]:
                    possibilities.append(direction)
            if len(possibilities)==0:
                return STAY
            return random.choice(possibilities)



			

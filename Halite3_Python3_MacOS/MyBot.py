#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging





""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
states = {}
intendedMoves = []

""" <<<Helper Functions>>> """

def selectState(ship):
    if states[] == null:
        return searching

    if states[ship.id] == "return":
        if ship.halite_amount > 500:
            return "return"
        else:
            return "searching"
    else:
        if ship.halite_amount > 750:
            return "return"
        else:
            return "searching"


def action(game_map, ship, state, me):
    if state == "searching":
        if game_map[ship.position].halite_amount > 250:
            return ship.stay_still()
        else:
            n = game_map[ship.position.directional_offset(Direction.North)].halite_amount
            s = game_map[ship.position.directional_offset(Direction.South)].halite_amount
            e = game_map[ship.position.directional_offset(Direction.East)].halite_amount
            w = game_map[ship.position.directional_offset(Direction.West)].halite_amount
            c = game_map[ship.position].halite_amount


            if s == max(n,e,w,s,c) and ship.position.directional_offset(Direction.South) not in intendedMoves:
                intendedMoves.append(ship.position.directional_offset(Direction.South))
                move =  ship.move(Direction.South)
            elif n == max(n,e,w,s,c) and ship.position.directional_offset(Direction.North) not in intendedMoves:
                intendedMoves.append(ship.position.directional_offset(Direction.North))
                move = ship.move(Direction.North)
            elif e == max(n,e,w,s,c) and ship.position.directional_offset(Direction.East) not in intendedMoves:
                intendedMoves.append(ship.position.directional_offset(Direction.East))
                move = ship.move(Direction.East)
            elif w == max(n,e,w,s,c) and ship.position.directional_offset(Direction.West) not in intendedMoves:
                intendedMoves.append(ship.position.directional_offset(Direction.West))
                move = ship.move(Direction.West)
            else:
                intendedMoves.append(ship.position)
                move = ship.stay_still()

            logging.info("Bot {} move {}".format(ship.id, move))

            return move



    elif state == "return":
        return ship.move(game_map.naive_navigate(ship, me.shipyard.position))



# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))






""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    for ship in me.get_ships():
        #state selector
        states[ship.id] = selectState(ship)

        #action based on state
        command_queue.append(action(game_map, ship, states[ship.id], me))

    intendedMoves = []

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)










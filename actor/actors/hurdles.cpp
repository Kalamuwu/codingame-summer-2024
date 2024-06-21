#ifndef HURDLES_ACTOR_H
#define HURDLES_ACTOR_H

#include <iostream>
#include <stdio.h>
#include <string.h>

#include "../macros.h"
#include "actor.hpp" // HurdlesActor
#include "../costs.hpp" // Costs

#define GPU_BOARD_LENGTH 30
#define BOARD_EMPTY '.'
#define BOARD_HURDLE '#'

HurdlesActor::HurdlesActor(const uint8_t p_idx)
    : Actor (p_idx)
{
}

Costs HurdlesActor::getCosts(const std::string gpu, const int16_t* registers)
{
    // calculate where we're at and if we're stunned
    int16_t myPos = registers[player_idx];
    int16_t myStun = registers[player_idx + 3];
    // short-circuit if we're stunned
    if (myStun)
    {
        DEBUG("Stunned this turn, skipping!\n");
        return Costs(0);
    }

    // calculate where everyone else is, their stun, and give up if the gap is too large
    int16_t p2Pos = registers[p2_idx];
    int16_t p3Pos = registers[p3_idx];
    int16_t p2Stun = registers[p2_idx + 3];
    int16_t p3Stun = registers[p3_idx + 3];
    //if (p2Pos - myPos > THRESH_GIVE_UP || p3Pos - myPos > THRESH_GIVE_UP)
    //{
    //    DEBUG("Gap too large, giving up!\n");
    //    return Costs(0);
    //}

    // transform gpu track to workable data array -- skip ahead to where
    // we're at, fill the rest with empty
    // note that this is a c-style string, the first N chars are
    // meaningful to the program but the last is a '\0' so that the entire
    // array can simply be printed with no further processing
    uint8_t board[GPU_BOARD_LENGTH+1];
    for (int i = 0; i < GPU_BOARD_LENGTH; i++)
    {
        const int shiftedi = i+myPos;
        if (shiftedi < GPU_BOARD_LENGTH)
            board[i] = gpu.at(shiftedi);
        else
            board[i] = BOARD_EMPTY;
    }
    board[GPU_BOARD_LENGTH] = '\0';
    DEBUG("Shifted board: %s\n", board);

    // board[0] is current tile
    if (board[1] == BOARD_HURDLE)
    {
        DEBUG("Next tile is hurdle, voting UP\n");
        return Costs(-1.0, 3.0, 3.0, 3.0);
    }
    else if (board[2] == BOARD_HURDLE)
    {
        DEBUG("One tile before hurdle, voting LEFT\n");
        return Costs(3.0, 3.0, -1.0, 3.0);
    }
    else if (board[3] == BOARD_HURDLE)
    {
        DEBUG("Two tiles before hurdle, voting DOWN/UP\n");
        return Costs(-2.0, -2.0, -1.0, 3.0);
    }
    DEBUG("No hurdle within range, voting RIGHT\n");
    return Costs(-2.0, -2.0, -1.0, -3.0);
}

void HurdlesActor::reset()
{
    DEBUG("Resetting HurdlesActor\n");
}

#endif // HURDLES_ACTOR_H

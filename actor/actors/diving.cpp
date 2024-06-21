#ifndef DIVING_ACTOR_H
#define DIVING_ACTOR_H

#include <iostream>
#include <stdio.h>
#include <string.h>

#include "../macros.h"
#include "actor.hpp" // DivingActor
#include "../costs.hpp" // Costs

DivingActor::DivingActor(const uint8_t p_idx)
    : Actor(p_idx)
{
}


Costs DivingActor::getCosts(const std::string gpu, const int16_t* registers)
{
    // calculate player points...
    const int8_t myPoints = registers[player_idx];
    const int8_t p2Points = registers[p2_idx];
    const int8_t p3Points = registers[p3_idx];

    // ...and combos...
    const int8_t myCombo = registers[player_idx + 3];
    const int8_t p2Combo = registers[p2_idx + 3];
    const int8_t p3Combo = registers[p3_idx + 3];

    // ...and calculate the turns remaining...
    const int8_t turnsLeft = gpu.length();
    if (turnsLeft == 0)
    {
        DEBUG("No turns left, skipping\n");
        return Costs(0);
    }

    // translate gpu to usable array
    //TODO

    // calculate next action
    if (gpu.at(0) == 'U')
    {
        DEBUG("Next action UP\n");
        return Costs(-1.0, 1.0, 1.0, 1.0) * (myCombo+1);
    }
    else if (gpu.at(0) == 'D')
    {
        DEBUG("Next action DOWN\n");
        return Costs(1.0, -1.0, 1.0, 1.0) * (myCombo+1);
    }
    else if (gpu.at(0) == 'L')
    {
        DEBUG("Next action LEFT\n");
        return Costs(1.0, 1.0, -1.0, 1.0) * (myCombo+1);
    }
    else if (gpu.at(0) == 'R')
    {
        DEBUG("Next action RIGHT\n");
        return Costs(1.0, 1.0, 1.0, -1.0) * (myCombo+1);
    }

    DEBUG("ERROR: Unknown GPU character '%c'\n", gpu.at(0));
    return Costs(0);
}

void DivingActor::reset()
{
    DEBUG("Resetting DivingActor\n");
}

#endif // DIVING_ACTOR_H

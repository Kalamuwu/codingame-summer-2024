#ifndef SKATING_ACTOR_H
#define SKATING_ACTOR_H

#include <iostream>
#include <stdio.h>
#include <string.h>

#include "../macros.h"
#include "actor.hpp" // SkatingActor
#include "../costs.hpp" // Costs

SkatingActor::SkatingActor(const uint8_t p_idx)
    : Actor (p_idx)
{
}

Costs SkatingActor::getCosts(const std::string gpu, const int16_t* registers)
{
    // calculate player locations...
    const int8_t myPos = registers[player_idx];
    const int8_t p2Pos = registers[p2_idx];
    const int8_t p3Pos = registers[p3_idx];

    // ...and risks
    const int8_t myRisk = registers[player_idx + 3];
    const int8_t p2Risk = registers[p2_idx + 3];
    const int8_t p3Risk = registers[p3_idx + 3];

    // short-circuit -- stunned
    if (myRisk < 0)
    {
        DEBUG("Stunned, skipping!\n");
        return Costs(0);
    }

    // turn gpu risk order into usable values
    const int index_UP    = gpu.find('U');
    const int index_DOWN  = gpu.find('D');
    const int index_LEFT  = gpu.find('L');
    const int index_RIGHT = gpu.find('R');

    // quick error checks
    if (index_UP    == std::string::npos
     || index_DOWN  == std::string::npos
     || index_LEFT  == std::string::npos
     || index_RIGHT == std::string::npos)
    {
        DEBUG("ERROR: One or more risk values was npos!\n");
        return Costs(0);
    }

    // turn indexes into risk amounts
    const int8_t risk_UP    = index_UP    - 1;
    const int8_t risk_DOWN  = index_DOWN  - 1;
    const int8_t risk_LEFT  = index_LEFT  - 1;
    const int8_t risk_RIGHT = index_RIGHT - 1;

    // TODO process all this

    return Costs(0);
}

void SkatingActor::reset()
{
    DEBUG("Resetting SkatingActor\n");
}

#endif // SKATING_ACTOR_H

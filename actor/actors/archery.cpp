#ifndef ARCHERY_ACTOR_H
#define ARCHERY_ACTOR_H

#include <iostream>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "../macros.h"
#include "actor.hpp" // ArcheryActor
#include "../costs.hpp" // Costs

ArcheryActor::ArcheryActor(const uint8_t p_idx)
    : Actor (p_idx)
{
}

Costs ArcheryActor::getCosts(const std::string gpu, const int16_t* registers)
{
    // calculate player locations
    int8_t myX = registers[player_idx + 0];
    int8_t myY = registers[player_idx + 1];
    int8_t p2X = registers[p2_idx + 0];
    int8_t p2Y = registers[p2_idx + 1];
    int8_t p3X = registers[p3_idx + 0];
    int8_t p3Y = registers[p3_idx + 1];

    // short-circuit -- on 0,0
    if (abs(myX) + abs(myY) == 0)
    {
        DEBUG("On bullseye! Voting NONE\n");
        return Costs(0);
    }

    // calculate turns left, for scaling costs
    int8_t turnsLeft = gpu.length();
    if (turnsLeft == 0)
    {
        DEBUG("No turns left, skipping\n");
        return Costs(0);
    }

    // turn gpu wind strengths into a usable array
    //TODO

    // calculate Euclidean distance, for scoring
    const double myEuclideanDist = sqrt(myX*myX + myY*myY);
    const double p2EuclideanDist = sqrt(p2X*p2X + p2Y*p2Y);
    const double p3EuclideanDist = sqrt(p3X*p3X + p3Y*p3Y);

    // calculate Manhattan distance, for who's "winning" right now
    const double myManhattanDist = abs(myX) + abs(myY);
    const double p2ManhattanDist = abs(p2X) + abs(p2Y);
    const double p3ManhattanDist = abs(p3X) + abs(p3Y);

    // "want" scalar (scaler) based on how much time is left and how large
    // the gap is between us and the best of the opponents
    const double bestOfOppDist = (p2EuclideanDist<p3EuclideanDist)? p2EuclideanDist : p3EuclideanDist;
    const double scaler = turnsLeft * (myEuclideanDist / bestOfOppDist);

    // calculate which way we need to go, scaled by the number of turns left
    if (myX > abs(myY))
    {
        DEBUG("X deviance more than Y, majorly LEFT\n");
        return Costs(0.0, 0.0, -1.0, 1.0) * scaler;
    }
    else if (-myX > abs(myY))
    {
        DEBUG("X deviance more than Y, majorly RIGHT\n");
        return Costs(0.0, 0.0, 1.0, -1.0) * scaler;
    }
    else if (myY > abs(myX))
    {
        DEBUG("Y deviance more than X, majorly DOWN\n");
        return Costs(1.0, -1.0, 0.0, 0.0) * scaler;
    }
    // (-myY > abs(myX))
    DEBUG("Y deviance more than X, majorly UP\n");
    return Costs(-1.0, 1.0, 0.0, 0.0) * scaler;
}

void ArcheryActor::reset()
{
    DEBUG("Resetting ArcheryActor\n");
}

#endif // ARCHERY_ACTOR_H

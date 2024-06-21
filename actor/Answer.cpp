#include <iostream>
#include <stdio.h>
#include <string>

#include "macros.h"

#define N_GAMES 4
#define N_MEDALS 3
#define N_PLAYERS 3
#define N_TICKS 100

#if TIME_OUTPUT
    #include <time.h>
    // CLOCK_MS_DIFF: returns the difference, in ms, between two clocks.
    #define CLOCK_MS_DIFF(start, finish) \
        ((double)(finish - start)) * 1000 / CLOCKS_PER_SEC
#endif

// Macro definition USE_TUNABLES should be provided by compiler flags.
#ifndef INPUT_TUNABLES
#define INPUT_TUNABLES false
#endif

#define NUM_TUNABLE_POLYNOMIALS 3
#define NUM_TUNABLE_DOUBLES 1

#include "costs.hpp" // Costs
#include "actors/actor.hpp" // HurdlesActor, ArcheryActor, SkatingActor,
                            // DivingActor
#include "polynomial.hpp" // Polynomial

int main()
{
    #if TIME_OUTPUT
        clock_t clock_programStart = clock();
    #endif

    // initial information
    int player_idx;
    std::cin >> player_idx; std::cin.ignore();
    int nGames;  // prefer N_GAMES macro
    std::cin >> nGames; std::cin.ignore();

    // initialize score weights
    Polynomial weights[N_GAMES];
    #if INPUT_TUNABLES
        // read in tunable weights from command command line
        for (int i = 0; i < N_GAMES; i++)
            std::cin >> weights[i].a
                     >> weights[i].b
                     >> weights[i].c
                     >> weights[i].d;
        std::cin.ignore();
        // declare OK
        std::cout << "INITIALIZED" << std::endl;
    #else
        #warning NOT using built-in tunables! Results will be invalid!
        // built-in, hard-coded tunables
        weights[0] = Polynomial( -0.48562301469285085,  14.560719309039953,  11.501279122760458,  15.919786940425276); // HurdlesActor
        weights[1] = Polynomial(  0.015640058614165953,  0.03477142832844393, -2.6045582061099912, -3.6463286061008153); // ArcheryActor
        weights[2] = Polynomial(  0.09721789666247926,  7.419701990195123,  1.65630939318324, -4.116144837869353); // SkatingActor
        weights[3] = Polynomial(  1.8492198786838454,  15.839304318465024, -12.07666784285157,  9.434974481354772); // DivingActor
    #endif





    // initialize actors
    Actor* actors[N_GAMES];
    actors[0] = new HurdlesActor(player_idx);
    actors[1] = new ArcheryActor(player_idx);
    actors[2] = new SkatingActor(player_idx);
    actors[3] = new DivingActor( player_idx);

    #if TIME_OUTPUT
        clock_t clock_initFinish = clock();
        double ms_init = CLOCK_MS_DIFF(clock_programStart, clock_initFinish);
        fprintf(stderr, "Init took %.3f ms\n", ms_init);
        // container for loop timings
        double actorTimes[N_GAMES] = {0};
    #endif

    // game loop
    for (int tick = 0; tick < N_TICKS; tick++) {

        #if TIME_OUTPUT
            clock_t clock_loopStart = clock();
        #endif

        // read in score information
        int32_t playerScores[N_PLAYERS];
        int8_t playerMedals[N_PLAYERS][N_GAMES][N_MEDALS];
        for (int i = 0; i < N_PLAYERS; i++) {
            std::cin >> playerScores[i];
            for (int k = 0; k < N_GAMES; k++)
                for (int j = 0; j < N_MEDALS; j++)
                    std::cin >> playerMedals[i][k][j];
        }
        std::cin.ignore();
        //TODO do something with this

        // For each game...
        Costs netCosts;
        for (int i = 0; i < N_GAMES; i++) {

            #if PRINT_FINAL_COSTS
                // Debug -- show all final move costs
                fprintf(stderr, "======================================\n");
                fprintf(stderr, "Starting round %d\n", tick);
            #endif

            // ...read in its game information...
            std::string gpu;
            int16_t regs[7];
            std::cin >> gpu >> regs[0] >> regs[1] >> \
                               regs[2] >> regs[3] >> \
                               regs[4] >> regs[5] >> \
                               regs[6];
            std::cin.ignore();

            #if TIME_OUTPUT
                clock_t clock_actorProcessingStart = clock();
            #endif

            // ...decide if it's good...
            Costs costs = Costs(0);
            if (gpu.compare("GAME_OVER") != 0)
                // ...and either forward it accordingly...
                costs = actors[i]->getCosts(gpu, regs);
            else
                // ...or reset if needed.
                actors[i]->reset();

            // accumulate weights
            const Costs weightedVoteCosts = weights[i].evaluate(costs);
            const Costs finalCosts = costs * weightedVoteCosts;

            #if PRINT_FINAL_COSTS
                // Debug -- show all final move costs
                fprintf(stderr, "Costs for game %d:\n", i);
                fprintf(stderr,
                    "Move   Base   Weight  NET\n"
                    " UP    %+6.2f *%+6.2f =%+6.2f\n"
                    " DOWN  %+6.2f *%+6.2f =%+6.2f\n"
                    " LEFT  %+6.2f *%+6.2f =%+6.2f\n"
                    " RIGHT %+6.2f *%+6.2f =%+6.2f\n"
                    "--------------------------------------\n",
                    costs.UP,    weightedVoteCosts.UP,    finalCosts.UP,
                    costs.DOWN,  weightedVoteCosts.DOWN,  finalCosts.DOWN,
                    costs.LEFT,  weightedVoteCosts.LEFT,  finalCosts.LEFT,
                    costs.RIGHT, weightedVoteCosts.RIGHT, finalCosts.RIGHT);
            #endif

            #if TIME_OUTPUT
                clock_t clock_actorProcessingStop = clock();
                double ms_actorProcessing = CLOCK_MS_DIFF(
                    clock_actorProcessingStart,
                    clock_actorProcessingStop);
                actorTimes[i] = ms_actorProcessing;
            #endif

            // Finally, Sum up costs across all these games...
            netCosts += finalCosts;
        }

        #if PRINT_FINAL_COSTS
            // Debug -- show all final move costs
            fprintf(stderr, "NET COSTS:\n");
            fprintf(stderr, " UP    %+6.2f\n DOWN  %+6.2f\n" \
                            " LEFT  %+6.2f\n RIGHT %+6.2f\n",
                            netCosts.UP,   netCosts.DOWN,
                            netCosts.LEFT, netCosts.RIGHT);
        #endif

        // ...and pick the option with the lowest cost.
        // Prefers UP, then DOWN, then LEFT, then RIGHT, if tie.
        if      (netCosts.UP <= netCosts.DOWN
              && netCosts.UP <= netCosts.LEFT
              && netCosts.UP <= netCosts.RIGHT)
            printf("UP\n");
        else if (netCosts.DOWN <= netCosts.UP
              && netCosts.DOWN <= netCosts.LEFT
              && netCosts.DOWN <= netCosts.RIGHT)
            printf("DOWN\n");
        else if (netCosts.LEFT <= netCosts.UP
              && netCosts.LEFT <= netCosts.DOWN
              && netCosts.LEFT <= netCosts.RIGHT)
            printf("LEFT\n");
        else // (netCosts.RIGHT <= netCosts.UP
        //    && netCosts.RIGHT <= netCosts.DOWN
        //    && netCosts.RIGHT <= netCosts.LEFT)
            printf("RIGHT\n");

        #if TIME_OUTPUT
            clock_t clock_loopStop = clock();
            const double ms_gameloop = CLOCK_MS_DIFF(
                clock_loopStart,
                clock_loopStop);
            const double ms_net = actorTimes[0] + actorTimes[1]
                                + actorTimes[2] + actorTimes[3];

            fprintf(stderr, "======================================\n");
            fprintf(stderr, "Loop %d total took:  %.3f ms\n", tick, ms_gameloop);
            fprintf(stderr, "  HurdlesActor took:  %.3f ms\n", actorTimes[0]);
            fprintf(stderr, "  ArcheryActor took:  %.3f ms\n", actorTimes[1]);
            fprintf(stderr, "  SkatingActor took:  %.3f ms\n", actorTimes[2]);
            fprintf(stderr, "  DivingActor took:   %.3f ms\n", actorTimes[3]);
            fprintf(stderr, "  Net intermediate:   %.3f ms\n", ms_gameloop - ms_net);
        #endif

    }

}

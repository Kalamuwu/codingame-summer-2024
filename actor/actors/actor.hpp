#ifndef ACTOR_H
#define ACTOR_H

#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "../costs.hpp" // Costs

#if PRINT_ACTOR_DEBUGS
#define DEBUG(...) fprintf(stderr, __VA_ARGS__)
#else
#define DEBUG(...) /* noop */
#endif

class Actor
{
public:
    Actor(const uint8_t p_idx) : player_idx(p_idx)
    {
        p2_idx = (p_idx + 1) % 3;
        p3_idx = (p_idx + 2) % 3;
    };

    /**
     * getCosts: Returns the costs for potentially taking each of the four actions.
     */
    virtual inline Costs getCosts(const std::string gpu, const int16_t* registers) = 0;

    /**
     * getCosts: Returns the costs for potentially taking each of the four actions.
     */
    inline Costs getCosts(const std::string gpu, const int16_t reg0, const int16_t reg1, \
                                                 const int16_t reg2, const int16_t reg3, \
                                                 const int16_t reg4, const int16_t reg5, \
                                                 const int16_t reg6)
    {
        // Wrap the registers in an array and pass to other definition.
        const int16_t regs[7] = { reg0, reg1, reg2, reg3, reg4, reg5, reg6 };
        return getCosts(gpu, regs);
    }

    /**
     * reset: Resets the game state to the beginning of a game.
     */
    virtual void reset() = 0;

    uint8_t player_idx, p2_idx, p3_idx;
};

class HurdlesActor : public Actor
{
public:
    HurdlesActor(const uint8_t p_idx);
    inline Costs getCosts(const std::string gpu, const int16_t* registers) override;
    void reset() override;
};

class ArcheryActor : public Actor
{
public:
    ArcheryActor(const uint8_t p_idx);
    inline Costs getCosts(const std::string gpu, const int16_t* registers) override;
    void reset() override;
};

class SkatingActor : public Actor
{
public:
    SkatingActor(const uint8_t p_idx);
    inline Costs getCosts(const std::string gpu, const int16_t* registers) override;
    void reset() override;
};

class DivingActor : public Actor
{
public:
    DivingActor(const uint8_t p_idx);
    inline Costs getCosts(const std::string gpu, const int16_t* registers) override;
    void reset() override;
};

#endif // ACTOR_H

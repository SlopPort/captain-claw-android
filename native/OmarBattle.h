#pragma once

// Encounter rules independent of rendering and physics; damage comes through
// HealthComponent's real projectile/melee contacts.
struct OmarBattle {
    enum Hit { Other, Fire, Ice, Bullet, DuckSword };
    int health = 200;
    int bullets = 0;
    bool fireShield = true;
    bool secondPhase() const { return health <= 100; }
    bool defeated() const { return health == 0; }
    void reset() { *this = OmarBattle(); }
    bool strike(Hit hit) {
        if (defeated()) return false;
        if (!secondPhase()) {
            const Hit counter = fireShield ? Ice : Fire;
            if (hit == counter) {
                health -= 25;
                fireShield = !fireShield;
                return true;
            }
            if (hit == (fireShield ? Fire : Ice)) {
                health = health + 25 > 200 ? 200 : health + 25;
            }
        } else if (hit == Bullet) {
            if (bullets < 3) ++bullets;
        } else if (hit == DuckSword && bullets == 3) {
            health -= 25;
            bullets = 0;
            return true;
        }
        return false;
    }
};

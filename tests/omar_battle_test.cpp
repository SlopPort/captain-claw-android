#include "../native/OmarBattle.h"
#include <cassert>
#include <cstdio>

int main() {
    OmarBattle boss;
    assert(!boss.strike(OmarBattle::Bullet) && boss.health == 200);
    assert(!boss.strike(OmarBattle::DuckSword));
    assert(boss.strike(OmarBattle::Ice) && boss.health == 175 && !boss.fireShield);
    // Wrong element restores one hit, without changing the shield.
    assert(!boss.strike(OmarBattle::Ice) && boss.health == 200 && !boss.fireShield);
    assert(boss.strike(OmarBattle::Fire));
    assert(boss.strike(OmarBattle::Ice));
    assert(boss.strike(OmarBattle::Fire));
    assert(boss.strike(OmarBattle::Ice) && boss.secondPhase());
    assert(boss.health == 100);
    assert(!boss.strike(OmarBattle::Fire) && boss.health == 100);
    for (int round = 0; round < 4; ++round) {
        assert(!boss.strike(OmarBattle::DuckSword));
        for (int bullet = 0; bullet < 3; ++bullet) {
            assert(!boss.strike(OmarBattle::Bullet));
            assert(boss.bullets == bullet+1);
            if (bullet < 2) assert(!boss.strike(OmarBattle::DuckSword));
        }
        assert(!boss.strike(OmarBattle::Other));
        assert(boss.strike(OmarBattle::DuckSword));
        assert(boss.health == 75-round*25 && boss.bullets == 0);
    }
    assert(boss.defeated() && !boss.strike(OmarBattle::DuckSword));
    boss.reset();
    assert(boss.health == 200 && boss.bullets == 0 && boss.fireShield && !boss.secondPhase());
    puts("PASS Omar: counter elements, healing, two phases, bullet gate, defeat, reset");
}

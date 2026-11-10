"""Original-supported Gabriel action timing fixture; OpenAI Codex (LLM).

Real arena, player protection and teleport only. No boss health edits, cannon
callback invocation, or campaign-completion claims. User files are restored.
"""
import argparse
import json
import os
import re
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def assess(log):
    actions = []
    for line in log.splitlines():
        action = re.search(r"Pazur Gabriel action: action=(\d+) pirates=(\d+) prelude=(\d+) tick=(\d+)",line)
        event = re.search(r"Pazur Gabriel event: event=(bombs|cannon|summon)(?: pirates=(\d+))? tick=(\d+)",line)
        if action:
            kind, pirates, prelude, tick = map(int,action.groups())
            assert pirates <= 2,(kind,pirates)
            assert prelude == (0 if kind == 2 else 500),(kind,prelude)
            actions.append(dict(kind=kind,pirates=pirates,prelude=prelude,tick=tick,events=[]))
        elif event and actions:
            kind,pirates,tick = event.groups()
            if pirates: assert int(pirates) <= 2,pirates
            actions[-1]["events"].append(dict(kind=kind,tick=int(tick),pirates=int(pirates) if pirates else None))
    assert len(actions) >= 6,actions
    completed = actions[:-1]
    for action in completed:
        assert len(action["events"]) == 1,action
        event = action["events"][0]
        assert event["kind"] == {1:"bombs",2:"summon",3:"cannon"}[action["kind"]],action
        elapsed = event["tick"]-action["tick"]
        target = 590 if action["kind"] == 2 else 630
        assert target-85 <= elapsed <= target+85,(action,elapsed)
    for before,after in zip(actions,actions[1:]):
        # idle1 takes2420ms, exceeding the concurrent1000ms original idle gate.
        minimum = 3010 if before["kind"] == 2 else 3570
        assert after["tick"]-before["tick"] >= minimum-85,(before,after)
    observed = {event["kind"] for action in completed for event in action["events"]}
    assert observed == {"bombs","summon","cannon"},observed
    return dict(passed=True,actions=actions,all_three_actions_observed=True,
                pirate_limit_observed=any(action["pirates"]==2 for action in actions))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",required=True)
    parser.add_argument("--seconds",type=float,default=60)
    args=parser.parse_args()
    if not os.environ.get("ANDROID_SERIAL"):
        parser.error("Select the authorized device with ANDROID_SERIAL")
    result=dict(passed=False,apk_sha256=installed_apk_sha256(),natural_playthrough=False,
                player_protected=True,boss_hp_edited=False)
    with CampaignSession(args.report,level=8,apk_support=True) as session:
        try:
            session.command("invincible 1")
            session.command("teleport 31631 5167")
            time.sleep(24)
            # The stager is far from the final ship-deck geometry. Observe the
            # real arena with Claw near its button, so pirates do not chase an
            # off-arena diagnostic position and immediately disappear.
            marker=len(session.logs())
            session.command("campaignmap")
            buttons=re.findall(r'name=Level8_GabrielButton x=([-\d.]+) y=([-\d.]+)',session.logs()[marker:])
            assert buttons,'Real Gabriel button position missing'
            x,y=map(float,buttons[-1])
            session.command(f"campaignposition {x-65} {y-35}")
            result['player_positioned_in_real_arena']=True
            # Let any arena-local introduction finish before measuring commands.
            time.sleep(24)
            start=len(session.logs())
            time.sleep(args.seconds)
            result.update(assess(session.logs()[start:]))
            assert "Fatal signal" not in session.logs() and "FATAL EXCEPTION" not in session.logs()
        finally:
            (session.report/"results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
            print(json.dumps(result),flush=True)


if __name__ == "__main__":
    main()

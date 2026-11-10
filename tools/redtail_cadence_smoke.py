"""Red Tail shared decision-gate fixture; OpenAI Codex (LLM).

Protected real arena with positional setup, not campaign or original runtime
parity evidence. No boss HP edits. CampaignSession restores user files.
"""
import argparse
import json
import os
import re
import statistics
import time
from campaign_session import CampaignSession
from android_package import installed_apk_sha256


def assess_decisions(log, animation, frame):
    cycles = []
    decision = None
    for line in log.splitlines():
        if "actor=Level13_RedTail " not in line:
            continue
        tick = re.search(r" tick=(\d+)", line)
        if not tick:
            continue
        tick = int(tick[1])
        if "Pazur attack decision:" in line:
            decision = dict(tick=tick, delay_ms=int(re.search(r" delay=(\d+)", line)[1]))
        elif "Pazur attack cycle:" in line:
            action = re.search(r" animation=(\S+)", line)[1]
            cycles.append(dict(tick=tick, animation=action, prelude_ms=int(re.search(r" delay=(\d+)", line)[1]), decision=decision, hits=[]))
            decision = None
        elif "Pazur attack frame:" in line and cycles:
            cycles[-1]["hits"].append(dict(tick=tick, frame=int(re.search(r" frame=(\d+)", line)[1])))
    paired = [cycle for cycle in cycles if cycle["decision"]]
    assert len(paired) >= 3, cycles
    assert all(1000 <= cycle["decision"]["delay_ms"] <= 1500 for cycle in paired), paired
    assert all(cycle["prelude_ms"] == 0 for cycle in paired), paired
    assert all(len(cycle["hits"]) <= 1 for cycle in paired), paired
    for before, after in zip(paired, paired[1:]):
        # Selected gate runs during the previous attack. Allow one update of
        # clock ordering, rather than adding its delay before either animation.
        elapsed = after["decision"]["tick"] - before["decision"]["tick"]
        assert elapsed >= before["decision"]["delay_ms"] - 45, (before, after)
    selected = [cycle for cycle in paired if cycle["animation"] == animation and cycle["hits"]]
    assert len(selected) >= 3, paired
    assert all(cycle["hits"][0]["frame"] == frame for cycle in selected), selected
    offsets = [cycle["hits"][0]["tick"] - cycle["tick"] for cycle in selected]
    expected_offset = 50 if animation == "strike8" else 210
    assert all(max(0, expected_offset-85) <= value <= expected_offset+85 for value in offsets), offsets
    return dict(passed=True, animation=animation, expected_frame=frame, cycles=paired,
                first_event_offsets_ms=offsets, median_offset_ms=statistics.median(offsets))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--mode", choices=("melee", "ranged", "both"), default="both")
    args = parser.parse_args()
    if not os.environ.get("ANDROID_SERIAL"):
        parser.error("Select the authorized device with ANDROID_SERIAL")
    result = dict(passed=False, apk_sha256=installed_apk_sha256(), natural_playthrough=False,
                  player_protected=True, boss_hp_edited=False, cases=[])
    with CampaignSession(args.report, level=13, apk_support=True) as session:
        try:
            session.command("invincible 1")
            session.command("teleport 37176 2021")
            time.sleep(23)
            def boss():
                start = len(session.logs())
                session.command("campaignmap")
                matches = re.findall(r"kind=boss .*name=(\S+) x=([-\d.]+) y=([-\d.]+) hp=(-?\d+)", session.logs()[start:])
                assert matches, "No live Red Tail found"
                name, x, y, hp = matches[-1]
                assert name == "Level13_RedTail", name
                return float(x), float(y), int(hp)
            result["boss_hp_initial"] = boss()[2]
            phases = [("melee",55,"strike8",1),("ranged",250,"strike4",3)]
            for mode, distance, animation, frame in phases:
                if args.mode not in (mode,"both"):
                    continue
                start = len(session.logs())
                deadline = time.monotonic()+10
                while time.monotonic() < deadline:
                    x,y,hp = boss()
                    session.command(f"campaignposition {x-distance} {y-5}")
                    time.sleep(.3)
                result["cases"].append(assess_decisions(session.logs()[start:],animation,frame))
            assert "Fatal signal" not in session.logs() and "FATAL EXCEPTION" not in session.logs()
            result["passed"] = True
        finally:
            (session.report/"results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
            print(json.dumps(result),flush=True)


if __name__ == "__main__":
    main()

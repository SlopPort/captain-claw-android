"""Coverage-contract checks: unknown flows/names must not become complete code.

OpenAI Codex (LLM). Synthetic protocol facts, no commercial executable data.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from rea_code_region import successors
from rea_registry_seeds import registrations, join_review_status


class RegionFlowTests(unittest.TestCase):
    def instruction(self, kind, conditional=False, destinations=(), status='decoded'):
        return dict(address='0x1000', length=2, status=status,
                    flow=dict(kind=kind, conditional=conditional, direct_destinations=list(destinations)))

    def test_conditional_includes_taken_and_fallthrough(self):
        edges, gaps = successors(self.instruction('jump', True, ['0x1010']))
        self.assertEqual(set(edges), {0x1002, 0x1010}); self.assertFalse(gaps)

    def test_unconditional_jump_does_not_invent_fallthrough(self):
        self.assertEqual(successors(self.instruction('jump', False, ['0x1010'])), ([0x1010], []))

    def test_computed_jump_without_targets_retains_gap(self):
        edges, gaps = successors(self.instruction('jump'))
        self.assertFalse(edges); self.assertIn('jump-destination-unresolved', gaps)

    def test_call_is_not_a_callee_body_or_proven_return(self):
        edges, gaps = successors(self.instruction('call', destinations=['0x8000']))
        self.assertEqual(edges, [0x1002]); self.assertTrue(gaps)

    def test_undecodable_does_not_guess_next_instruction(self):
        edges, gaps = successors(self.instruction('unavailable', status='undecodable'))
        self.assertFalse(edges); self.assertIn('instruction-not-decoded', gaps)

    def test_return_and_terminal_stop(self):
        for kind in ('return', 'terminal'):
            self.assertEqual(successors(self.instruction(kind)), ([], []))


class RegistryTests(unittest.TestCase):
    def test_explicit_function_review_survives_regeneration(self):
        rows = [dict(callback='0x2000')]
        join_review_status(rows, [dict(address='0x2000', semantic_status='partial')], {})
        self.assertEqual(rows[0]['semantic_status'], 'partial')
        self.assertEqual(rows[0]['semantic_review_source'], 'function-ledger')

    def test_region_review_keeps_distinct_provenance(self):
        rows = [dict(callback='0x2000')]
        join_review_status(rows, [], {'0x2000': dict(semantic_status='partial')})
        self.assertEqual(rows[0]['semantic_status'], 'partial')
        self.assertEqual(rows[0]['semantic_review_source'], 'bounded-region')

    def test_independent_region_does_not_become_native_instruction_review(self):
        rows = [dict(callback='0x2000')]
        join_review_status(rows, [], {'0x2000': dict(semantic_status='partial', decoder='capstone-independent')})
        self.assertEqual(rows[0]['semantic_review_decoder'], 'capstone-independent')

    def test_acquisition_without_review_stays_unreviewed(self):
        rows = [dict(callback='0x2000', status='literal-callback-observed')]
        join_review_status(rows, [dict(address='0x2000', dossier={'acquired': True})], {})
        self.assertEqual(rows[0]['semantic_status'], 'unreviewed')
        self.assertNotIn('semantic_review_source', rows[0])

    def test_removed_decision_does_not_keep_stale_source(self):
        rows = [dict(callback='0x2000', semantic_review_source='bounded-region')]
        join_review_status(rows, [], {})
        self.assertEqual(rows[0]['semantic_status'], 'unreviewed')
        self.assertNotIn('semantic_review_source', rows[0])

    def assembly(self, callback='0x2000'):
        return ['0x1000: PUSH 0x0', '0x1002: PUSH 0x3000', '0x1007: PUSH '+callback,
                '0x100c: MOV EDX, dword ptr [ECX]', '0x100e: CALL dword ptr [EDX + 0x1c]']

    def test_missing_defined_string_preserves_callback(self):
        row = registrations(self.assembly(), [])[0]
        self.assertEqual(row['callback'], '0x2000'); self.assertIsNone(row['name'])

    def test_register_argument_is_not_invented_literal(self):
        row = registrations(self.assembly('EAX'), [])[0]
        self.assertNotIn('callback', row)

    def test_string_must_match_actual_push_source_and_address(self):
        row = registrations(self.assembly(), [dict(source_address='0x1002', address='0x3333', value='example')])[0]
        self.assertNotIn('callback', row)


if __name__ == '__main__':
    unittest.main()

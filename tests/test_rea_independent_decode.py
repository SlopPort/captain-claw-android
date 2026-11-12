"""Synthetic decoder/traversal contracts; no commercial bytes. Codex (LLM)."""
from pathlib import Path
import hashlib
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from rea_decode_region import decode
from rea_audit_inventory import validate_independent_region


class IndependentDecodeTests(unittest.TestCase):
    def run_bytes(self, data, **kwargs):
        return decode(bytes.fromhex(data),0x1000,[0x1000],**kwargs)

    def test_return_does_not_decode_trailing_data(self):
        value=self.run_bytes('c3 90')
        self.assertEqual(set(value['instructions']),{'0x1000'})
        self.assertFalse(value['gaps'])

    def test_conditional_explores_both_paths(self):
        value=self.run_bytes('74 01 c3 c3')
        self.assertEqual(set(value['instructions']),{'0x1000','0x1002','0x1003'})
        self.assertFalse(value['gaps'])

    def test_loop_is_conditional_control_flow(self):
        value=self.run_bytes('e2 fe c3')
        flow=value['instructions']['0x1000']['flow']
        self.assertTrue(flow['conditional'])
        self.assertEqual(flow['direct_destinations'],['0x1000'])
        self.assertIn('0x1002',value['instructions'])

    def test_direct_call_is_not_followed_or_proved_returning(self):
        value=self.run_bytes('e8 00 10 00 00 c3')
        self.assertEqual(set(value['instructions']),{'0x1000','0x1005'})
        self.assertEqual(value['instructions']['0x1000']['flow']['direct_destinations'],['0x2005'])
        self.assertTrue(value['gaps'])

    def test_computed_jump_retains_unknown_destination(self):
        value=self.run_bytes('ff e0 c3')
        self.assertEqual(set(value['instructions']),{'0x1000'})
        self.assertTrue(any(x['reason']=='jump-destination-unresolved' for x in value['gaps']))

    def test_outside_direct_jump_retains_gap(self):
        value=self.run_bytes('eb 20 c3')
        self.assertTrue(any(x['reason']=='edge-outside-selected-region' for x in value['gaps']))

    def test_truncated_instruction_is_not_guessed(self):
        value=self.run_bytes('0f')
        self.assertEqual(value['instructions']['0x1000']['status'],'undecodable')
        self.assertTrue(value['gaps'])

    def test_overlapping_instruction_starts_are_visible(self):
        value=self.run_bytes('74 01 b8 90 90 90 c3 c3')
        self.assertTrue(any(x['reason']=='overlapping-instruction-boundaries' for x in value['gaps']))

    def test_instruction_budget_retains_worklist(self):
        value=self.run_bytes('90 c3',maximum=1)
        self.assertEqual(value['pending'],['0x1001'])
        self.assertFalse(value['completed_bounded_worklist'])

    def test_exception_flow_is_not_a_fallthrough(self):
        value=self.run_bytes('cc c3')
        self.assertNotIn('0x1001',value['instructions'])
        self.assertTrue(value['gaps'])

    def test_invalid_seed_is_rejected(self):
        with self.assertRaises(ValueError):
            decode(b'\xc3',0x1000,[0x2000])


class ByteProvenanceTests(unittest.TestCase):
    def fixture(self):
        source=dict(operation='read_bytes',evidence_id='ev_synthetic',
            subject=dict(digest=dict(sha256='synthetic-target')),
            normalized_result=dict(address='0x1000',bytes_hex='c3',complete=True,
                                   requested_bytes=1,returned_bytes=1))
        region=dict(target_sha256='synthetic-target',start='0x1000',end='0x1000',
            byte_source=dict(evidence_id='ev_synthetic',sha256=hashlib.sha256(b'\xc3').hexdigest()),
            instructions={'0x1000':dict(byte_evidence_id='ev_synthetic',
                instruction=dict(address='0x1000',status='decoded',bytes='c3',length=1))})
        return region,source

    def test_exact_carrier_is_accepted(self):
        validate_independent_region(*self.fixture())

    def test_different_target_is_rejected(self):
        region,source=self.fixture();region['target_sha256']='other-target'
        with self.assertRaises(ValueError):validate_independent_region(region,source)

    def test_unbacked_instruction_cannot_add_coverage(self):
        region,source=self.fixture();region['instructions']['0x1000']['instruction']['bytes']='90'
        with self.assertRaises(ValueError):validate_independent_region(region,source)

    def test_incomplete_carrier_is_rejected(self):
        region,source=self.fixture();source['normalized_result']['complete']=False
        with self.assertRaises(ValueError):validate_independent_region(region,source)


if __name__=='__main__':
    unittest.main()

import json
from copy import deepcopy
import unittest
from scripts.check_research_contracts import ROOT, validate


class ResearchContractTests(unittest.TestCase):
    def setUp(self):
        self.ledger = json.loads((ROOT/'claims/claim_registry.json').read_text())
        self.register = json.loads((ROOT/'tracking/premise_register.json').read_text())

    def test_published_registry_resolves(self):
        self.assertEqual(validate(self.ledger, self.register), [])

    def test_open_physical_claim_cannot_be_promoted_by_status_change(self):
        mutant = deepcopy(self.ledger)
        next(c for c in mutant['claims'] if c['id'] == 'C-NATURE')['status'] = 'demonstrated'
        self.assertTrue(validate(mutant, self.register))

    def test_unknown_premise_and_missing_evidence_fail(self):
        mutant = deepcopy(self.ledger)
        mutant['claims'][0]['premises'].append('P-INVENTED')
        mutant['claims'][0]['evidence'].append('missing-evidence.json')
        self.assertGreaterEqual(len(validate(mutant, self.register)), 2)

    def test_case_changed_domain_cannot_bypass_release_policy(self):
        mutant = deepcopy(self.ledger)
        c = next(c for c in mutant['claims'] if c['id'] == 'C-NATURE')
        c.update(domain='PHYSICAL', status='demonstrated', premises=[])
        self.assertTrue(validate(mutant, self.register))


if __name__ == '__main__':
    unittest.main()

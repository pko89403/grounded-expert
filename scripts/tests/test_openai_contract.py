"""Check the OpenAI handoff against the canonical output contract."""
import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOST = REPO / "hosts/openai/skills/grounded-expert/SKILL.md"
SPEC = importlib.util.spec_from_file_location("openai_quote_check", REPO / "tools/check_quotes.py")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

PYTHON_URL = "https://docs.python.org/3/whatsnew/3.7.html"
PYTHON_QUOTE = "the insertion-order preservation nature of dict objects has been declared to be an official part of the Python language spec."


class OutputContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primary = CHECKER.load_primary(HOST)
        cls.fixtures = CHECKER.load_fixtures(REPO / "tools/fixtures")

    def answer(self, rows, level="quick", domain="python", no_primary=False):
        last = ("not run (quick)" if level == "quick" else "ran — nothing opposing found")
        suffix = " (no primary source)" if no_primary else ""
        return "\n".join([
            "Python 3.7부터 언어 사양으로 보장됩니다.",
            f"Level: {level}{suffix}", f"Domain: {domain}", CHECKER.HEADER,
            "|---|---|---|---|---|---|", *rows,
            "추가로 확인하지 못한 사항은 없습니다.", f"Disconfirming search: {last}",
        ])

    def row(self, tag="EXTRACTED", url=PYTHON_URL, quote=PYTHON_QUOTE, number=1):
        return (f'| {number} | dict 삽입 순서는 언어 사양입니다. | {tag} | "{quote}" | '
                f"What's New In Python 3.7, Summary | {url} |")

    def check(self, answer, fixtures=None):
        return CHECKER.check(answer, self.primary, self.fixtures if fixtures is None else fixtures)

    def test_canonical_contract_is_preserved_verbatim(self):
        def block(path):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("<output-contract>\n"), 1)
            return text.split("<output-contract>\n", 1)[1].split("\n</output-contract>", 1)[0]

        self.assertEqual(block(HOST), block(REPO / "plugin/SKILL.md"))
        self.assertEqual(self.primary, CHECKER.load_primary(REPO / "plugin/SKILL.md"))

    def test_korean_answer_preserves_checkable_english_fields(self):
        result = self.check(self.answer([self.row()]))
        self.assertEqual((result.invalid, result.unverified, result.ok), (0, 0, 1), result.lines)

    def test_secondary_quote_uses_via_tag_instead_of_extracted(self):
        # Synthetic secondary-page fixture, not a claim of a real retrieval.
        url, passage = "https://secondary.example/python", "A short test passage."
        fixtures = [CHECKER.Fixture("synthetic", [url], "full", passage)]
        bad = self.check(self.answer([self.row(url=url, quote=passage)]), fixtures)
        good = self.check(self.answer([
            self.row(tag="INFERRED (via secondary.example)", url=url, quote=passage)
        ], no_primary=True), fixtures)
        self.assertGreater(bad.invalid, 0, bad.lines)
        self.assertEqual((good.invalid, good.unverified, good.ok), (0, 0, 1), good.lines)

    def test_source_copy_has_its_own_secondary_tag(self):
        url, passage = "https://secondary.example/copy", "A short test passage."
        fixtures = [CHECKER.Fixture("synthetic-copy", [url], "full", passage)]
        result = self.check(self.answer([
            self.row(tag="INFERRED (copy via secondary.example)", url=url, quote=passage)
        ], no_primary=True), fixtures)
        self.assertEqual((result.invalid, result.unverified, result.ok), (0, 0, 1), result.lines)

    def test_secondary_only_answer_requires_no_primary_suffix(self):
        url, passage = "https://secondary.example/python", "A short test passage."
        fixtures = [CHECKER.Fixture("synthetic", [url], "full", passage)]
        result = self.check(self.answer([
            self.row(tag="INFERRED (via secondary.example)", url=url, quote=passage)
        ]), fixtures)
        self.assertEqual(result.invalid, 1, result.lines)
        self.assertTrue(any("no primary source" in line for line in result.lines), result.lines)

    def test_multiple_opposing_urls_use_commas_without_spaces(self):
        url, passage = "https://secondary.example/python", "A short test passage."
        fixtures = self.fixtures + [CHECKER.Fixture("synthetic", [url], "full", passage)]
        answer = self.answer([
            self.row(),
            self.row(tag="INFERRED (via secondary.example)", url=url, quote=passage, number=2),
        ], level="standard")
        last = "Disconfirming search: ran — nothing opposing found"
        valid = answer.replace(last, "Disconfirming search: found — https://opposing.example/a,https://opposing.example/b")
        invalid = valid.replace("/a,https", "/a https")
        self.assertEqual(self.check(valid, fixtures).invalid, 0)
        self.assertTrue(any("INVALID" in line and "last line" in line
                            for line in self.check(invalid, fixtures).lines))

    def test_parent_receipt_cannot_follow_final_line(self):
        result = self.check(self.answer([self.row()]) + "\n부모 에이전트의 검증 메모")
        self.assertTrue(any("INVALID" in line and "last line" in line for line in result.lines), result.lines)

    def test_no_web_fallback_omits_level_and_marks_unconfirmed(self):
        answer = "\n".join([
            "direct answer — no independent subagent; not externally verified",
            "검색 도구를 사용할 수 없어 외부 근거를 확인하지 못했습니다.",
            CHECKER.HEADER, "|---|---|---|---|---|---|",
            "| 1 | 요청한 사실을 확인하지 못했습니다. | not confirmed | - | - | - |",
            "외부 확인이 필요합니다.",
        ])
        result = self.check(answer)
        self.assertEqual((result.invalid, result.ok), (0, 1), result.lines)

    def test_aliases_and_fragments_cannot_fill_standard_floor(self):
        url = "https://www.rfc-editor.org/rfc/rfc9110.html"
        alias = "https://datatracker.ietf.org/doc/html/rfc9110"
        quote = "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request."
        result = self.check(self.answer([
            self.row(url=url + "#name-301-moved-permanently", quote=quote),
            self.row(url=alias, quote=quote, number=2),
        ], level="standard", domain="http"))
        self.assertEqual(result.ok, 2, result.lines)
        self.assertEqual(result.invalid, 1, result.lines)
        self.assertTrue(any("floor" in line and "1 distinct documents" in line for line in result.lines), result.lines)


if __name__ == "__main__":
    unittest.main()

"""tests/test_eval.py — the eval suite actually executes with real pass/fail."""
import pytest


@pytest.mark.asyncio
async def test_eval_suite_runs_and_reports(fresh_home_with_skills):
    """§STEP 1: the 10-15 task eval suite is implemented and actually executes,
    with real pass/fail results reported."""
    from eval.runner import run_eval
    class IO:
        def __init__(self): self.out = []
        def print(self,*a,**k): self.out.append(" ".join(str(x) for x in a))
        def input(self,p=''): return ""
        def confirm(self,p): return True
    io = IO()
    result = await run_eval(io, compare=False)
    assert "passed" in result
    # at least 12 of 15 should pass on a working build
    out_text = "\n".join(io.out)
    assert "TOTAL" in out_text
    # extract the total
    for line in io.out:
        if "TOTAL" in line:
            parts = line.split("/")
            if len(parts) >= 2:
                passed = int(parts[0].split()[-1])
                assert passed >= 12, f"eval only passed {passed}/15"


def test_eval_suite_has_10_to_15_tasks():
    """§16: a focused set of 10-15 golden tasks."""
    from eval.suite import get_suite
    suite = get_suite()
    assert 10 <= len(suite) <= 15
    # covers the required categories
    cats = {t.category for t in suite}
    assert "code_generation" in cats
    assert "research" in cats
    assert "multi_agent_handoff" in cats

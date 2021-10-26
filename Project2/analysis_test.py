# Test programs for my  analysis.py
# In case that the original one are not suitable for test, I rewrite a analysis_modified.py to test
import analysis_modified as mod

def test_User():
    assert mod.judgeUser("@intel") == (53.5, 3.0, 43.5, 56.5, 43.5)

def test_Topic():
    assert mod.judgeTopic("#StreetWomanFighter") == (4.6, 3.6, 91.8, 95.4, 4.6)

def test_Wrong():
    assert mod.report_wrong() == ("Useless input")

function assertEquals(val1, val2) {
	if (val1 !== val2) {
		throw new Error('assertEquals failed! ', val1, val2);
	}
}

function runTest_div_specials() {
	setSpecialDivOpts("foo", "onClick", {r:"abc1"});
	setSpecialDivOpts("bar", "onClick", {r:"abc2"});
	obj = getSpecialDivOpts("foo", "onClick");
	assertEquals(obj["r"], "abc1");
	obj = getSpecialDivOpts("bar", "onClick");
	assertEquals(obj["r"], "abc2");
	setSpecialDivOpts("bar", "onClick", {r:"abc3"});
	obj = getSpecialDivOpts("bar", "onClick");
	assertEquals(obj["r"], "abc3");
}
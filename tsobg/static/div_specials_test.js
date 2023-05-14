
function createError(text, values) {
	return new Error(text + '<font color="red">' + values.join(', ') + '</font>');
}

function assertEquals(val1, val2) {
	if (val1 !== val2) {
		throw createError('assertEquals failed! values: ', [val1, val2]);
	}
}

function assertTrue(val) {
	if ( ! val) {
		throw createError('assertTrue failed! value: ',  [val]);
	}
}

function assertFalse(val) {
	if (val) {
		throw createError('assertFalse failed! value: ', [val]);
	}
}

function runTest_div_specials() {
	// test special divOpts
	setSpecialDivOpts("foo", "onClick", {r:"abc1"});
	setSpecialDivOpts("bar", "onClick", {r:"abc2"});
	obj = getSpecialDivOpts("foo", "onClick");
	assertEquals(obj["r"], "abc1");
	obj = getSpecialDivOpts("bar", "onClick");
	assertEquals(obj["r"], "abc2");
	setSpecialDivOpts("bar", "onClick", {r:"abc3"});
	obj = getSpecialDivOpts("bar", "onClick");
	assertEquals(obj["r"], "abc3");

	// test div sub elements
	div1 = getDiv("foo1", true);
	butt1 = activateSubElement("foo1", "button", true);
	butt2 = activateSubElement("foo2", "button", true);
	img1 = activateSubElement("foo1", "img", true);
	img1.setAttribute('src', "test.png");
	butt1.innerHTML = "ok";
	assertFalse(Object.is(butt1, img1));
	butt1b = activateSubElement( "foo1", "button", true); // activate same button again (same id)
	assertTrue(Object.is(butt1, butt1b));
	assertFalse(Object.is(butt1, butt2));
	butt3 = activateSubElement( "foo3", "button", false); // try to activate another button
	assertEquals(butt3, null);
}
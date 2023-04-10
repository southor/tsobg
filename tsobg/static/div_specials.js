
// store div elements that was created by this file in a Map object, accessed by div id
var divs = null;

var specialDivOpts = null;
let specialDivOptsDefaults = {"tsobg-selectable":false, "tsobg-onClick":null};

function getSpecialDivOpts(divId, name) {
	let specialOpts = (specialDivOpts ? specialDivOpts.get(divId) : null) ?? specialDivOptsDefaults;
	return specialOpts["tsobg-" + name];
}

function setSpecialDivOpts(divId, name, value) {
	if (specialDivOpts === null) {
		specialDivOpts = new Map();
	}
	let specialOpts = specialDivOpts.get(divId) ?? Object.assign({}, specialDivOptsDefaults);
	specialOpts["tsobg-" + name] = value;
}

function readSpecialDivOpts(divId, opts, name) {
	var value;
	if (name in opts) {
		value = opts[name];
		setSpecialDivOpts(divId, name, value);
	} else {
		value = getSpecialDivOpts(divId, name);
	}
	return value;
}

/**
 * Get div from DOM, create div if it doesn't exist
 * @param { String } id The div id
 * @param { Boolean } create If div does not already exist it will be created if 'create' is true, otherwise null is returned
 * @param { String } defaultDivPositioning optional argument that sets changes default divPositioning which noramlly is "static". This argument will only have an effect if the div does not exist and has to be created
 * @return { Element } The div element or null
 */
function getDiv(id, create, defaultDivPositioning) {
	if (divs === null) {
		divs = new Map();
	}
	let div = divs.get(id) ?? document.getElementById(id);
	if (create && ! div) {
		log("info", "creating div: " + id);
		div = document.createElement("div");
		div.setAttribute('id', id);
		if (defaultDivPositioning) {
			div.style.position = defaultDivPositioning;
		}
		divs.set(id, div);
	}
	return div;
}


function deleteAllCreatedDivs() {
	if (divs !== null) {
		for (const [id, div] of divs.entries()) {
			const parentNode = div.parentNode;
			if (parentNode) {
				//log("removing " + id + " from document");
				parentNode.removeChild(div);
			}
		}
		divs.clear();
	}
}
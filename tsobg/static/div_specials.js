
// store div elements that was created by this file in a Map object, accessed by div id
var divsMap = null;
var buttonsMap = null;

var specialDivOpts = null;
let specialDivOptsDefaults = {"tsobg-trapClicks":false, "tsobg-selectable":false, "tsobg-onClick":null};

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
	if (divsMap === null) {
		divsMap = new Map();
	}
	let div = divsMap.get(id) ?? document.getElementById(id);
	if (create && ! div) {
		log("info", "creating div: " + id);
		div = document.createElement("div");
		div.setAttribute('id', id);
		if (defaultDivPositioning) {
			div.style.position = defaultDivPositioning;
		}
		divsMap.set(id, div);
	}
	return div;
}

function _activateElement(elementsMap, elementsName, id, create) {
	if (elementsMap === null) {
		elementsMap = new Map();
	}
	let element = elementsMap.get(id);
	if (create && ! element) {
		log("info", "creating " + elementsName + " element for divId: " + id);
		element = document.createElement(elementsName);
		elementsMap.set(id, element);
	}
	return element;
}

/**
 * Get div from DOM, create div if it doesn't exist
 * @param { String } divId The div id that button belongs to
 * @param { Boolean } create If div does not already exist it will be created if 'create' is true, otherwise null is returned
 * @return { Element } The button element or null
 */
function activateButtonElement(divId, create) {
	return _activateElement(buttonsMap, "button", divId, create);
}

function _deleteAllCreatedElements(elementsMap) {
	if (elementsMap !== null) {
		for (const [id, element] of elementsMap.entries()) {
			const parentNode = element.parentNode;
			if (parentNode) {
				parentNode.removeChild(element);
			}
		}
		elementsMap.clear();
	}
}

function deleteAllCreatedElements() {
	_deleteAllCreatedElements(buttonsMap);
	_deleteAllCreatedElements(divsMap);
}
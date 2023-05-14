
function log(level, ...msgArgs) {
	//console.log(level, msgArgs);
}

// ----------------------------------------- Div Elements storage -----------------------------------------

// store div elements that was created by this file in a Map object, accessed by div id
var divsMap = null;

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

// ----------------------------------------- Div Sub elements storage -----------------------------------------

var elementsMap = null;

/**
 * Get element from data structure, create element if it doesn't exist
 * @param { String } divId The div id that the element belongs to
 * @param { String } elementName The element name (for example "button" or "img")
 * @param { Boolean } create If element does not already exist it will be created if 'create' is true, otherwise null is returned
 * @return { Element } The element or null
 */
function activateSubElement(divID, elementName, create) {
	if (elementsMap === null) {
		elementsMap = new Map();
	}
	id = divID + "-" + elementName;
	var element = elementsMap.get(id);
	if ( ! element) {
		if (create) {
			log("info", "creating " + elementName + " element for divId: " + id);
			element = document.createElement(elementName);
			elementsMap.set(id, element);
		} else {
			element = null; // null instead of undefined
		}
	}
	return element;
}

// ----------------------------------------- Element storage reset/cleanup -----------------------------------------

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
	_deleteAllCreatedElements(elementsMap);
	_deleteAllCreatedElements(divsMap);
}

// ----------------------------------------- special Div opts (div attributes that need to be stored in its own storage) -----------------------------------------

var specialDivOpts = null;
let specialDivOptsDefaults = {"tsobg-trapClicks":false, "tsobg-selectable":false, "tsobg-onClick":null, "tsobg-buttonEnabled":true};

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
	specialDivOpts.set(divId, specialOpts)
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

function resetSpecialDivOpts() {
	specialDivOpts = null;
}





















// ----------------------------------------- Div Elements storage -----------------------------------------
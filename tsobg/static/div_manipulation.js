
var selectedIds = null;

function getSelectedIds() {
	if (selectedIds === null) {
		selectedIds = new Set();
	}
	return selectedIds;
}

function isSelected(divId) {
	selectedIds = getSelectedIds();
	return selectedIds.has(divId);
}

function getDivChildElement(div, tag) {
	const arr = div.getElementsByTagName(tag);
	return (arr.length >= 1) ? arr[0] : null;
}

function stopEventPropagation(e) {
	if (typeof e.stopPropagation != "undefined") {
		e.stopPropagation();
	} else if (typeof e.cancelBubble != "undefined") {
		e.cancelBubble = true;
	} else {
		errorStr = "Browser does not support stopPropagation function nor cancelBubble attribute."
		log("error", errorStr);
		alert("Error! " + errorStr);
	}
}

/**
 * @return true if object is then selected, false otehrwise
 */
function toggleDivSelected(divId) {
	highlightDivId = divId + "_highlight";
	selectedIds = getSelectedIds();
	if (selectedIds.has(divId)) {
		// deselect it
		selectedIds.delete(divId);
		if (getDiv(highlightDivId)) {
			setDiv(highlightDivId, {parent: null});
			console.log("highlight off");
		} else {
			console.log("highlight was never created in the first place");
		}
		return false;
	} else {
		// select it
		if ( ! getDiv(highlightDivId)) {
			// highlight div needs setup
			div = getDiv(divId, false);
			highlightOpts = {parent: divId, divPositioning: "absolute", left: "0px", top: "0px", width: div.clientWidth, height: div.clientHeight, border: "solid", borderColor: "red"};
		} else {
			// highlight div already setup
			highlightOpts = {parent: divId};
		}
		setDiv(highlightDivId, highlightOpts);
		selectedIds.add(divId);
		console.log("highlight on");
		return true;
	}
}

function isString(x) {
    return Object.prototype.toString.call(x) === '[object String]';
}

// helper function to get an element's exact position
function getElementPos(element) {
	var xPos = 0;
	var yPos = 0;
	while (element) {
		if (element.tagName == "BODY") {
			// deal with browser quirks with body/window/document and page scroll
			var xScrollPos = element.scrollLeft || document.documentElement.scrollLeft;
			var yScrollPos = element.scrollTop  || document.documentElement.scrollTop;
			xPos += (element.offsetLeft - xScrollPos + element.clientLeft);
			yPos += (element.offsetTop - yScrollPos + element.clientTop);
		} else {
			xPos += (element.offsetLeft - element.scrollLeft + element.clientLeft);
			yPos += (element.offsetTop - element.scrollTop + element.clientTop);
		}
		element = element.offsetParent;
	}
	return [xPos, yPos];
}

function getClickPos(element, event) {
	let divPos = getElementPos(element);
	let mouseX = Math.max(0, event.clientX - divPos[0]);
	let mouseY = Math.max(0, event.clientY - divPos[1]);
	return [mouseX, mouseY]
}

/**
 * Create a new actionObj where div related info has been added and all $ lookups has been resolved
 */
function resolvedActionObj(actionObj, divId, isSelected, mousePos) {
	function resolvedArg(arg, lookupObj) {
		if ( ! isString(arg)) return arg;
		if (arg.length === 0) return arg;
		if (arg[0] !== '$') return arg;
		return lookupObj[arg.substring(1)]
	}
	let actionReceiver = actionObj.receiver;
	let args = [...actionObj.args]; // make copy
	let kwargs = Object.assign({}, actionObj.kwargs); // make copy
	kwargs.receiver = actionReceiver
	kwargs.playerId = playerId
	kwargs.divId = divId;
	kwargs.isSelected = isSelected;
	kwargs.allSelected = getSelectedIds();
	for (let i=0; i<args.length; ++i) {
		args[i] = resolvedArg(args[i], kwargs);
	}
	//for (key in Object.keys(kwargs)) {
	//	kwargs[key] = resolvedArg(args[key]);
	//}
	kwargs.mousePos = mousePos;
	return {"receiver":actionReceiver, "args":args, "kwargs":kwargs}; // return a new actionObj
}

/**
 * Sets the onclick property for the div (or button)
 * @param {Element} div The div element to set
 * @param {boolean} trapClicks
 * @param {boolean} selectable
 * @param {function(string, any[])} onClickFunc The function that should be called, the function should have the form 'function(divId, actions)'
 * @param {Object} actionObj
 */
function setDivOnClick(div, trapClicks, selectable, onClickFunc, actionObj) {
	log("info", "setDivOnClick with actionObj: ", actionObj);
	if (selectable || onClickFunc) {
		div.onclick = function(event) {
			log("info", "divOnClick");
			let divId = div.getAttribute("id");
			var isSelected = false;
			if (selectable) {
				isSelected = toggleDivSelected(divId);
			}
			if (onClickFunc) {
				rActionObj = resolvedActionObj(actionObj, divId, isSelected, getClickPos(div, event));
				onClickFunc(rActionObj);
			}
			stopEventPropagation(event);
			return true;
		};
	} else if (trapClicks) {
		div.onclick = function(event) {
			stopEventPropagation(event);
			return false;
		};
	}
}

function setButtonOnClick(buttonElement, onClickFunc, actionObj) {
	log("info", "setButtonOnClick with actionObj: ", actionObj);
	if (onClickFunc) {
		let divId = buttonElement.parentElement.getAttribute("id");
		buttonElement.onclick = function(event) {
			rActionObj = resolvedActionObj(actionObj, divId, false, null);
			onClickFunc(rActionObj);
			stopEventPropagation(event); // TODO: is this needed for buttons?
			return true;
		};
	} else {
		buttonElement.onclick = function(event) {
			stopEventPropagation(event); // TODO: is this needed for buttons?
			return false;
		};
	}
}

// creates div sub element or enables/disables it
// If opts contains a string for key name then a sub element will be created of that element type if does not already exists.
// If name is not a member of opts or set to something falsey then if sub element exists it will be removed.
// Argument name: string element name (for example "button" or "img").
// returns element or null
function setDivSubElement(div, name, opts) {
	var element = getDivChildElement(div, name);
	if (name in opts) {
		let val = opts[name]; // Should be button caption or image filename
		if (val) {
			if ( ! element) {
				element = activateSubElement(div.getAttribute("id"), name, true);
				div.appendChild(element);
			}
			if (name == "img") element.setAttribute('src', val);
			else if (name == "button") element.innerHTML = val;
			else console.assert(false);
		} else {
			if (element) {
				div.removeChild(element);
			}
			element = null;
		}
	}
	return element;
}

// If val is Number it returns it as string and adds "px", else returns val as is
function addPXIfNeeded(val) {
	return (typeof val == "number") ? (val.toString() + "px") : val;
}

function setDivClickSettings(div, opts, sendActionFunc) {
	let divId = div.getAttribute("id");
	let buttonElement = setDivSubElement(div, "button", opts);
	let trapClicks = readSpecialDivOpts(divId, opts, "trapClicks");
	let selectable = readSpecialDivOpts(divId, opts, "selectable");
	let onClick = readSpecialDivOpts(divId, opts, "onClick");
	let buttonEnabled = readSpecialDivOpts(divId, opts, "buttonEnabled");
	var onClickFunc = null;
	var actionObj = null;
	if (onClick === "actions") {
		// TODO Trigger popup of actions to choose from (use "actions" property)
		onClickFunc = null;
	} else if ((typeof onClick === 'object') && onClick !== null) {
		actionObj = onClick
		onClickFunc = sendActionFunc;
	} else if (onClick === null) {
		onClickFunc = null;
	} else {
		console.log("error", "Received onClick property with invalid value: ", onClick);
		return;
	}
	if (buttonElement) {
		buttonElement.disabled = buttonEnabled ? false : true;
		setButtonOnClick(buttonElement, onClickFunc, actionObj);
		setDivOnClick(div, true, false, null, actionObj);
	} else {
		setDivOnClick(div, trapClicks, selectable, onClickFunc, actionObj);
	}
}

// If div does not exists it is created
function setDiv(id, opts, sendActionFunc) {
	log("info", "set div called with:", id, opts);
	let div = getDiv(id, true, "relative");

	if (opts.parent || opts.parent === null) {
		if (div.parentNode) {
			div.parentNode.removeChild(div);
			log("info", "removing div child");
		}
		if (opts.parent) {
			log("info", "setting div parent");
			getDiv(opts.parent, true, "relative").appendChild(div);
		}
	}

	if (opts.divPositioning) {
		div.style.position = opts.divPositioning;
	}

	if (opts.class) {
		div.setAttribute("class", opts.class);
	}

	if (opts.left) {
		div.style.left = addPXIfNeeded(opts.left);
	}

	if (opts.top) {
		div.style.top = addPXIfNeeded(opts.top);
	}
	
	if (opts.right) {
		div.style.right = addPXIfNeeded(opts.right);
	}
	
	if (opts.bottom) {
		div.style.bottom = addPXIfNeeded(opts.bottom);
	}

	if (opts.width) {
		div.style.width = addPXIfNeeded(opts.width);
	}

	if (opts.height) {
		div.style.height = addPXIfNeeded(opts.height);
	}

	if (opts.color) {
		div.style.backgroundColor = opts.color;
	}

	if (opts.border) {
		div.style.border = opts.border;
		div.style.borderWidth = "thin";
	}

	if (opts.borderColor) {
		div.style.borderColor = opts.borderColor;
	}

	if ("img" in opts) {
		setDivSubElement(div, "img", opts);
	}

	if (opts.text || opts.text === null) {
		let pElement = getDivChildElement(div, "p");
		if (opts.text) {
			if ( ! pElement) {
				log("info", "creating div paragraph");
				pElement = document.createElement("p");
				div.appendChild(pElement);
			}
			pElement.innerHTML = opts.text;
		} else {
			console.assert(opts.text === null);
			if (pElement) {
				pElement.innerHTML = "";
			}
		}
	}

	if ("selectable" in opts || "button" in opts || "onClick" in opts || "trapClicks" in opts || "buttonEnabled" in opts) {
		setDivClickSettings(div, opts, sendActionFunc);
	}
	
	return div;
}

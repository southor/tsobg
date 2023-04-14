

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

function log(level, ...msgArgs) {
	//console.log(level, msgArgs);
}


function getDivImgElement(div) {
	const arr = div.getElementsByTagName('img');
	return (arr.length >= 1) ? arr[0] : null;
}

function getDivParagraphElement(div) {
	const arr = div.getElementsByTagName('p');
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

/**
 * Create a new actionObj where div related info has been added and all $ lookups has been resolved
 */
function resolvedActionObj(actionObj, divId, isSelected) {
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
	return {"receiver":actionReceiver, "args":args, "kwargs":kwargs}; // return a new actionObj
}

/**
 * Sets the onclick property for the div
 * @param {Element} div The div element to set
 * @param {boolean} selectable
 * @param {function(string, any[])} onClickFunc The function that should be called, the function should have the form 'function(divId, actions)'
 * @param {Object} actionObj
 */
function setDivOnClick(div, selectable, onClickFunc, actionObj) {
	log("info", "setDivOnClick with actionObj: ", actionObj);
	if (selectable || onClickFunc) {
		div.onclick = function(e) {
			log("info", "divOnClick");
			let divId = div.getAttribute("id");
			var isSelected = false;
			if (selectable) {
				isSelected = toggleDivSelected(divId);
			}
			if (onClickFunc) {
				rActionObj = resolvedActionObj(actionObj, divId, isSelected);
				onClickFunc(rActionObj);
			}
			stopEventPropagation(e);
			return true;
		};
	} else {
		div.onclick = function(e) {
			stopEventPropagation(e);
			return false;
		};
	}
}

// updates div image and/or img actions according to opts
function setDivImg(div, opts) {
	if ("img" in opts) {
		let imgElement = getDivImgElement(div);
		if (opts.img) {
			if (imgElement) {
				imgElement.style.visibility = "visible";
			} else {
				log("info", "creating div img");
				imgElement = document.createElement("img");
				div.appendChild(imgElement);
			}
			imgElement.setAttribute('src', opts.img);
		} else {
			console.assert(opts.img === null);
			if (imgElement) {
				imgElement.style.visibility = "hidden";
			}
		}
	}
}

// If val is Number it returns it as string and adds "px", else returns val as is
function addPXIfNeeded(val) {
	return (typeof val == "number") ? (val.toString() + "px") : val;
}

function setDivClickSettings(div, opts, sendActionFunc) {
	let selectable = readSpecialDivOpts(div.getAttribute("id"), opts, "selectable");
	let onClick = readSpecialDivOpts(div.getAttribute("id"), opts, "onClick");
	var onClickFunc = null;
	var actionObj = null;
	if (onClick === "actions") {
		// TODO Trigger popup of actions to choose from (use "actions" property)
		onClickFunc = null;
	} else if (typeof onClick === 'object' && onClick !== null) {
		actionObj = onClick
		onClickFunc = sendActionFunc;
	} else if (onClick === null) {
		onClickFunc = null;
	} else {
		console.log("error", "Received onClick property with invalid value: ", onClick);
		return;
	}
	setDivOnClick(div, selectable, onClickFunc, actionObj);
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

	if ("selectable" in opts || "onClick" in opts) {
		setDivClickSettings(div, opts, sendActionFunc);
	}

	setDivImg(div, opts);

	if (opts.text || opts.text === null) {
		let pElement = getDivParagraphElement(div);
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
	
	return div;
}

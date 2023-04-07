

// store div elements that was created by this file in a Map object, accessed by div id
divs = null;
selectedIds = null;

function log(level, ...msgArgs) {
	//console.log(level, msgArgs);
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

function getSelectedIds() {
	if (selectedIds === null) {
		selectedIds = new Set();
	}
	return selectedIds;
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
 * Sets the onclick property for the div
 * @param {Element} div The div element to set
 * @param {function(string, any[])} onClickFunc The function that should be called, the function should have the form 'function(divId, actions)'
 * @param {any[]} actionObj
 */
function setDivOnClick(div, onClickFunc, actionObj) {
	log("info", "setDivOnClick with actionObj: ", actionObj);
	if (onClickFunc) {
		div.onclick = function(e) {
			log("info", "divOnClick");
			onClickFunc(div.getAttribute("id"), actionObj);
			stopEventPropagation(e);
			return true;
		};
	} else {
		div.onclick = function(e) {
			return false;
		};
	}
}

/**
 * Sets the onclick property for the an image located on top of a div
 * @param {Element} div The div element of the image to set
 * @param {function(string, any[])} onClickFunc The function that should be called, the function should have the form 'function(divId, actions)'
 * @param {any[]} actions An array of actions, these actions will be passed to the function every time the image is clicked
 */
function setImgOnClick(div, imgElement, onClickFunc, actions) {
	log("info", "setImgOnClick: ", actions);
	if (onClickFunc) {
		imgElement.onclick = function(e) {
			log("info", "imgOnClick");
			onClickFunc(div.getAttribute("id"), actions[0]);
			stopEventPropagation(e);
		};
	} else {
		div.onclick = function(e) {
			return false;
		};
	}
}

function toggleDivSelected(divId, _) {
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
	} else {
		// select it
		if ( ! getDiv(highlightDivId)) {
			// highlight div needs setup
			div = getDiv(divId, false);
			highlightOpts = {parent: divId, divPositioning: "absolute", left: "0px", top: "0px", width: div.style.width, height: div.style.height, border: "solid", borderColor: "red"};
		} else {
			// highlight div already setup
			highlightOpts = {parent: divId};
		}
		setDiv(highlightDivId, highlightOpts);
		selectedIds.add(divId);
		console.log("highlight on");
	}
}

// updates div image and/or img actions according to opts
function setDivImg(div, opts, onClickFunc) {
	let imgElement = null;
	
	if (opts.img || opts.img === null) {
		imgElement = getDivImgElement(div);
		if (opts.img) {
			if (imgElement) {
				imgElement.style.visibility = "visible";
			} else {
				log("info", "creating div img");
				imgElement = document.createElement("img");
				div.appendChild(imgElement);
				imgActions = div.getAttribute("data-imgActions");
				if (imgActions) {
					setImgOnClick(div, imgElement, onClickFunc, imgActions);
				}
			}
			imgElement.setAttribute('src', opts.img);
		} else {
			console.assert(opts.img === null);
			if (imgElement) {
				imgElement.style.visibility = "hidden";
			}
		}
	}

	if (opts.imgActions || opts.imgActions === null || opts.imgActions === []) {
		let imgActions = opts.imgActions;
		if ( ! imgElement) {
			imgElement = getDivImgElement(div);
		}
		if (imgActions) {
			div.setAttribute("data-imgActions", imgActions);
			if (imgElement) {
				setImgOnClick(div, imgElement, onClickFunc, imgActions);
			}
		} else {
			div.removeAttribute("data-imgActions", imgActions);
			if (imgElement) {
				imgElement.removeAttribute("onclick");
			}
		}
	}

	return imgElement;
}

// If val is Number it returns it as string and adds "px", else returns val as is
function addPXIfNeeded(val) {
	return (typeof val == "number") ? (val.toString() + "px") : val;
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

	if ("onClick" in opts) {
		oldOnClick = div.getAttribute("tsobg-onClick");
		newOnClick = opts.onClick
		if (newOnClick !== oldOnClick) {
			if (newOnClick === "select") {
				setDivOnClick(div, toggleDivSelected);
			} else if (newOnClick === "actions") {
				// TODO Trigger popup of actions to choose from (use "actions" property)
				setDivOnClick(div, null);
			} else if (Array.isArray(newOnClick)) {
				actionObj = newOnClick
				setDivOnClick(div, sendActionFunc, actionObj);
			} else if (newOnClick === null) {
				setDivOnClick(div, null);
			} else {
				log("error", "Received onClick property with invalid value: ", newOnClick);
			}
		}
		div.setAttribute("tsobg-onClick", newOnClick);
	}

	setDivImg(div, opts, sendActionFunc);

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

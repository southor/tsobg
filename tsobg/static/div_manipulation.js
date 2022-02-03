

// store created div elements in a Map object, accessed by div id
divs = null;

function log(level, ...msgArgs) {
	//console.log(level, msgArgs)
}

/**
 * Get div from DOM, create div if it doesn't exist
 * @param { String } id The div id
 * @param { String } defaultDivPositioning optional argument that sets changes default divPositioning which noramlly is "static". This argument will only have an effect if the div does not exist and has to be created
 */
function getDiv(id, defaultDivPositioning) {
	if (divs === null) {
		divs = new Map();
	}
	let div = divs.get(id) ?? document.getElementById(id);
	if ( ! div) {
		log("info", "creating div: " + id);
		div = document.createElement("div");
		div.setAttribute('id', id);
		if (defaultDivPositioning) {
			div.style.position = defaultDivPositioning;
		}
		divs.set(id, div);
	}
	return div
}


function parseSize(obj) {
	let x = "auto";
	let y = "auto";
	if (obj !== "auto") {
		x = obj[0];
		y = obj[1];
		if (x !== "auto") {
			x = x + 'px';
		}
		if (y !== "auto") {
			y = y + 'px';
		}
	}
	return [x, y];
}

function getDivImgElement(div) {
	const arr = div.getElementsByTagName('img');
	return (arr.length >= 1) ? arr[0] : null;
}

function getDivParagraphElement(div) {
	const arr = div.getElementsByTagName('p');
	return (arr.length >= 1) ? arr[0] : null;
}

function setImgOnClick(div, imgElement, onClickFunc, actions) {
	log("info", "setImgOnClick: ", actions);
	imgElement.onclick = function() {
		log("info", "setImgOnClick: ");
		onClickFunc(div.getAttribute("id"), actions);
	};
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
				actions = div.getAttribute("data-actions");
				if (actions) {
					setImgOnClick(div, imgElement, onClickFunc, actions);
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

	if (opts.actions || opts.actions === null || opts.actions === []) {
		let actions = opts.actions;
		if ( ! imgElement) {
			imgElement = getDivImgElement(div);
		}
		if (actions) {
			div.setAttribute("data-actions", actions);
			if (imgElement) {
				setImgOnClick(div, imgElement, onClickFunc, actions);
			}
		} else {
			div.removeAttribute("data-actions", actions);
			if (imgElement) {
				imgElement.removeAttribute("onclick");
			}
		}
	}

	return imgElement;
}

// If div does not exists it is created
function setDiv(id, opts, onClickFunc) {
	log("info", "set div called with:", id, opts);
	let div = getDiv(id, "relative");

	if (opts.parent || opts.parent === null) {
		if (div.parentNode) {
			div.parentNode.removeChild(div);
			log("info", "removing div child");
		}
		if (opts.parent) {
			log("info", "setting div parent");
			getDiv(opts.parent, "relative").appendChild(div);
		}
	}

	if (opts.divPositioning) {
		div.style.position = opts.divPositioning;
	}

	if (opts.class) {
		div.setAttribute("class", opts.class);
	}

	if (opts.pos) {
		const pos = parseSize(opts.pos);
		div.style.left = pos[0];
		div.style.top = pos[1];
		log("info", "setting div pos");
	}

	if (opts.size) {
		const size = parseSize(opts.size);
		div.style.width = size[0];
		div.style.height = size[1];
		log("info", "setting div size");
	}

	if (opts.border) {
		div.style.border = opts.border;
		div.style.borderWidth = "thin";
	}

	if (opts.color) {
		div.style.backgroundColor = opts.color;
	}

	setDivImg(div, opts, onClickFunc);

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

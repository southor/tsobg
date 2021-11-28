
function parseSize(obj) {
	var x = "auto";
	var y = "auto";
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

// If div does not exists it is created
function setDiv(id, opts) {
	console.log("set div called with:", id, opts);
	var div = document.getElementById(id);
	if ( ! div) {
		console.log("creating div");
		div = document.createElement("div");
		div.setAttribute('id', id);
		div.style.position = "absolute";
		div.style.backgroundColor = "transparent";
	}

	if (opts.parent || opts.parent === null) {
		if (div.parentNode) {
			div.parentNode.removeChild(div);
			console.log("removing div child");
		}
		if (opts.parent) {
			console.log("setting div parent");
			document.getElementById(opts.parent).appendChild(div);
		}
	}

	if (opts.pos) {
		const pos = parseSize(opts.pos);
		div.style.left = pos[0];
		div.style.top = pos[1];
		console.log("setting div pos");
	}

	if (opts.size) {
		const size = parseSize(opts.size);
		div.style.width = size[0];
		div.style.height = size[1];
		console.log("setting div size");
	}

	if (opts.img || opts.img === null) {
		var imgElement = getDivImgElement(div)
		if (opts.img) {
			if (imgElement) {
				imgElement.style.visibility = "visible"
			} else {
				console.log("creating div img");
				imgElement = document.createElement("img");
				div.appendChild(imgElement);
			}
			imgElement.setAttribute('src', opts.img);
		} else {
			console.assert(opts.img === null);
			if (imgElement) {
				imgElement.style.visibility = "hidden"
            }
		}
	}

	if (opts.border) {
		div.style.border = opts.border;
		div.style.borderWidth = "thin";
	}

	if (opts.color) {
		div.style.backgroundColor = opts.color;
	}
}

/*
function removeDiv(id) {
	var div = document.getElementById("id");
	div.parentNode.removeChild(div);
}
*/
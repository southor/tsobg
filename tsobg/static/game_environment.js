
/*
function createDiv(id, rect, parentId) {
	var div = document.createElement("div");
	div.setAttribute('id', id);
	div.style.position = "absolute";
	document.getElementById(parentId).appendChild(div);
	div.style.left = rect.x + 'px';
	div.style.top = rect.y + 'px';
	div.style.width = rect.w + 'px';
	div.style.height = rect.h + 'px';
}
*/

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
	if (opts.parent) {
		if (div.parentNode) {
			div.parentNode.removeChild(div);
			console.log("removing div child");
		}
		console.log("setting div parent");
		document.getElementById(opts.parent).appendChild(div);
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
	if (opts.img) {
		var arr = div.getElementsByTagName('img');
		var img;
		if (arr.length >= 1) {
			img = arr[0]
			console.log("getting existing div img");
		} else {
			console.log("creating div img");
			img = document.createElement("img");
			div.appendChild(img);
		}
		console.log("set div img src ", opts.img);
		img.setAttribute('src', opts.img);
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

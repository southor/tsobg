
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
		//div.style.border = "solid #707070";
		//div.style.padding = "0px";
		//div.style.margin = "0px";
		//console.log("padding: ", div.style.padding);
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
		div.style.left = opts.pos[0] + 'px';
		div.style.top = opts.pos[1] + 'px';
		console.log("setting div pos");
	}
	if (opts.size) {
		div.style.width = opts.size[0] + 'px';
		div.style.height = opts.size[1] + 'px';
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

function removeDiv(id) {
	var div = document.getElementById("id");
	div.parentNode.removeChild(div);
}

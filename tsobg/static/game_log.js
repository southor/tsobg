
logWindowDiv = null;
msgLog = [];
gameLog = [];


function ensureIndex(arr, i) {
	while (arr.length <= i) {
		arr.push(null);
	}
}

function getLogWindowDiv() {
	if (logWindowDiv === null) {
		logWindowDiv = setDiv("log_window", {class: "log-window"});
	}
	return logWindowDiv;
}

function addToGameLogUI(logId, text) {
	let parentDiv = getLogWindowDiv();
	let logDivId = "log_div_" + logId;
	let div = setDiv(logDivId, {class:"log-item", text: text});
	parentDiv.prepend(div);
}

function removeFromGameLogUI(logId) {
	let logDivId = "log_div_" + logId;
	setDiv(logDivId, {parent:null});
}

/*
function addMsg(stateN, level, text) {
	ensureIndex(msgLog, stateN);
	let msg = level + ": " + text
	if (msgLog[i] === null) {
		msgLog[i] = [msg];
	} else {
		// messages are only sent once from server to client, so we can assume message is not already stored in teh sub array
		msgLog[i].push(msg);
	}
	console.log(stateN, level, text);
}
*/

function textFirstUppercase(text) {
	return (text.length == 0) ? "" : level.charAt(0).toUpperCase() + level.slice(1); 
}

function combineMsgLevelAndText(level, text) {
	return textFirstUppercase(level) + ": " + text;
}

function addMsg(level, text) {
	console.log(level, text)
	msgLog.push([level, text]);
	let logText =  combineMsgLevelAndText(level, text);
	addToGameLogUI("msg" + msgLog.length, logText);
}

function assertLogObj(obj, stateN, text) {
	console.assert(Array.isArray(obj));
	console.assert(obj.length === 2);
	console.assert(obj[0] === stateN);
	console.assert(obj[1] === text);
}

// Crates string from stateN number with spaces behind to fill up to 4 characters
function stateNText(stateN) {
	let text = stateN.toString()
	console.assert(text.length >= 1);
	return text + "&nbsp;".repeat(4 - text.length)
}

function addToGameLog(logId, stateN, text) {
	ensureIndex(gameLog, logId);
	let obj = gameLog[logId];
	if (obj === null) {
		obj = [stateN, text];
		gameLog[logId] = obj;
		addToGameLogUI(logId, stateNText(stateN) + " " + text);
	} else {
		// logId already stored here (must have been received before), assert that is the same log data
		assertLogObj(obj, stateN, text);
	}
	console.log(logId, stateN, text);
}

// clear entries but not the log UI element
function deleteAllGamelogEntries() {
	gameLog = []
}

// clear effected entries and their UI counterparts
function clearFromGamelog(fromStateN) {
	for (let i=gameLog.length-1; i>0; --i) {
		if (gameLog[i][0] < fromStateN) {
			gameLog = gameLog.slice(0, i+1);
		}
		removeFromGameLogUI(i);
	}
}
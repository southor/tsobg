
def createDebugPageHTML(globals, varPath, token):
	currName = "globals"
	currValue = globals
	selfLinkTemplate = "<a href=/debug?token=" + token + "&var={path}>{linkText}</a>"
	# traverse down the var tree following varPath
	pathElements = varPath.split("/") if varPath else []
	backLinks = [selfLinkTemplate.format(path="", linkText=currName)]
	for i,name in enumerate(pathElements):
		t = type(currValue)
		backLinks.append(selfLinkTemplate.format(path="/".join(pathElements[0:i+1]), linkText=name))
		if t in [int, float, str]:
			break;
		elif t in [tuple, list]:
			currName = name
			currValue = currValue[int(name)]
		elif t in [dict]:
			currName = name
			currValue = currValue[name]
		elif hasattr(currValue, "__dict__"):
			currName = name
			currValue = vars(currValue)[name]
		else:
			break;
	# Collect dict of values from currValue
	t = type(currValue)
	if t in [bool, int, float, str]:
		varsToShow = {"": currValue}
	elif t in [tuple, list]:
		varsToShow = {str(k):v for k,v in enumerate(currValue)}
	elif t in [dict]:
		varsToShow = currValue
	elif hasattr(currValue, "__dict__"):
		varsToShow = vars(currValue)
	else:
		varsToShow = {"": currValue}
	contentHTML = " / ".join(backLinks)
	# Make html from list		
	contentHTML += "<ul>"
	for k,v in varsToShow.items():
		liHTML = '<li style="color:{}">' + k + ": "
		t = type(v)
		typeStr = str(t).replace("<", "[").replace(">", "]")
		linkPathElements = pathElements + [k]
		linkTemplate = selfLinkTemplate.format(path="/".join(linkPathElements), linkText="{linkText}") # readding linkText as a parameter that can be set later
		if t in [bool, int, float]:
			liHTML = liHTML.format("black")
			liHTML += str(v)
		elif t in [str]:
			liHTML = liHTML.format("black")
			liHTML += '"{}"'.format(v)
		elif t in [tuple, list]:
			liHTML = liHTML.format("black")
			collectionSizeText = " ({})".format(len(v))
			liHTML += " " + linkTemplate.format(linkText = typeStr + collectionSizeText)
		elif t in [dict]:
			liHTML = liHTML.format("black")
			collectionSizeText = " ({})".format(len(v.keys()))
			liHTML += " " + linkTemplate.format(linkText = typeStr + collectionSizeText)
		elif callable(v):
			liHTML = liHTML.format("rgb(0, 220, 0)")
			liHTML += str(v)
			liHTML += " " + typeStr
		elif hasattr(v, "__dict__"):
			liHTML = liHTML.format("blue")
			collectionSizeText = " ({})".format(len(vars(v).keys()))
			liHTML += " " + linkTemplate.format(linkText = typeStr + collectionSizeText)
		else:
			liHTML = liHTML.format("pink")
			liHTML += str(v)
			liHTML += " " + typeStr
		liHTML += "</li>"
		contentHTML += liHTML
	contentHTML += "</ul>"
	return contentHTML

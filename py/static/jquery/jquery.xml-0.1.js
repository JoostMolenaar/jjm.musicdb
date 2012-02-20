Array.prototype.isArray = true;

jQuery.xml = function(node) {
	if (typeof node == 'object' && node.isArray) {
		var result = document.createElement(node[0]);
		for (var i = 1; i < node.length; i++)
			if (typeof node[i] == 'object' && !node[i].isArray) 
				for (var attrName in node[i]) 
					result.setAttribute(attrName, node[i][attrName]);
			else 
				result.appendChild(m.xml(node[i]));
		return result;
	}
	else 
		return document.createTextNode(node);
}

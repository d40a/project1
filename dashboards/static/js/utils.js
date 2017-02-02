function Tag(attributes, innerHtml='') {
	// args: attributes - dictionary where key is tag's attribute and value is array of values
	var html = '<' + attributes.tag;
	for (var key in attributes) {
		for (var i = 0; i < attributes[key].length; i++) {
			if (i == 0) html += ' ' + key + '="'; 
			else html += ' ';
			html += attributes[key][i];
		}
		html += '"';
	}
	html += '>' + innerHtml + '</' + attributes.tag + '>';
	this.html = html;
	this.attributes = attributes;
};
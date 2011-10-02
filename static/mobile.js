String.prototype.format = function() {
	// better make sure the input is escaped!
	var result = this;
	for (var i = 0; i < arguments.length; i++) {
		result = result.replace(new RegExp('\\{'+i+'\\}','g'), arguments[i]);
	}
	return result;
};

String.prototype.xml = function() {
	return this
		.replace(/&/g, '&amp;')
		.replace(/"/g, '&quot;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;');
};

encodeGET = function(obj) {
	result = '';
	for (var key in obj) {
		result += result ? '&' : '';
		result += key + '=' + encodeURI(obj[key])
	}
	return result
};

decodeGET = function(str) {
	result = {}
	str.split('&').map(function(pair) {
		var kv = pair.split('=');
		result[kv[0]] = decodeURI(kv[1])
	});
	return result;
};

$(function(e) {
	var init = '#page=root',
		data = null,

		// hash functions
		getHash = function() { return decodeGET(location.hash.substr(1)); },
		putHash = function(hash) { location.hash = '#' + encodeGET(hash); },
		updateHash = function(chg) {
			var hash = getHash()
			for (var key in chg) {
				hash[key] = chg[key];
			}
			putHash(hash);
		},

		// general html generation functions
		uri = function(uri, name) { 
			return '<a href="{0}">{1}</a>'.format(uri, name.xml()); 
		},
		link = function(obj) { 
			return uri(obj.attr('uri'), obj.attr('name')); 
		},
		
		// utility functions
		getter = function(attrName) {
			return function(obj) {
				return $(obj).attr(attrName);
			};
		},
		
		// traversal functions
		findArtist = function(ref) { 
			return data.find('artist[uri='+ref+']'); 
		},
		findLabel = function(ref) { 
			return data.find('label[uri='+ref+']'); 
		},
		findFormat = function(ref) { 
			return data.find('format[uri='+ref+']'); 
		},

		// loading and processing input data
		loadData = function(done) {
			$.get('/musicdb/release.xml', function(newData) {
				d = data = $(newData);
				done($(newData));
			});
		},
		loadData2 = function(done) {
			$.get('/musicdb/release.json', function(data) {
				done(data);
			});
		},
		loadArtists = function(data) {
			$('#artists ul')
				.empty()
				.html(data
					.find('artist')
					.map(function() {
						return '<li><a href="{0}">{1}</a></li>'.format(
							$(this).attr('uri'),
							$(this).attr('name').xml());
					})
					.toArray()
					.join(''));
		},
		loadLabels = function(data) {
			$('#labels ul')
				.empty()
				.html(data
					.find('label')
					.map(function() {
						return '<li><a href="{0}">{1}</a></li>'.format(
							$(this).attr('uri'),
							$(this).attr('name').xml());
					})
					.toArray()
					.join(''));
		},
		loadFormats = function(data) {
			$('#formats ul')
				.empty()
				.html(data
					.find('format')
					.map(function() {
						return '<li><a href="{0}">{1}</a></li>'.format(
							$(this).attr('uri'),
							$(this).attr('name').xml());
					})
					.toArray()
					.join(''));
		},
		loadReleases = function(data) {
			$('#releases ul')
				.empty()
				.html(data
					.find('release')
					.map(function() {
						var a = $(this).find('a').toArray().map(getter('ref')).map(findArtist),
							an = a.map(getter('name')).map(function(a) { return a.xml(); }).join(' / '),
							al = a.map(link).join(' / '),
							ll = link(findLabel($(this).attr('label'))),
							fl = link(findFormat($(this).attr('format')));
						return '<li>{0}{1}{2}</li>'.format(
							uri($(this).attr('uri'), $(this).attr('name')),
							'<div>{0}</div>'.format(an),
							'<dl class="collapsed">{0}</dl>'.format([
								'<dt>Artists</dt><dd>{0}</dd>'.format(al),
								'<dt>Label</dt><dd>{0}</dd>'.format(ll),
								'<dt>Cat.No</dt><dd>{0}</dd>'.format($(this).attr('cat')),
								'<dt>Label</dt><dd>{0}</dd>'.format(fl),
								'<dt>Year</dt><dd>{0}</dd>'.format($(this).attr('year'))
							].join('')));
					})
					.toArray()
					.join(''));
		},
		delay = function(fn) {
			window.setTimeout(fn, 100);
		},
		status = function(s) {
			var e = $('#status');
			if (s) {
				e.text(s);
				e.show();
			} else {
				e.hide();
			}
		},
		reload = function() {
			delay(function() {
				status('Loading data');
				loadData(function(data) {
					status('Processing artists');
					delay(function() {
						loadArtists(data);
						status('Processing labels');
						delay(function() {
							loadLabels(data);
							status('Processing formats');
							delay(function() {
								loadFormats(data);
								status('Processing releases');
								delay(function() {
									loadReleases(data);
									status('');
								});
							});
						});
					});
				});
			});
		};

	$(window).hashchange(function(e) {
		$('.page').hide();
		$('#' + getHash().page)
			.show()
			.trigger('showpage');
	});
	
	$('.page ul').click(function(e) {
		var li = e.target.tagName == 'li' ? $(e.target) : $(e.target).closest('li');
		var a = li.find('a:first');
		li.trigger('itemclick', [a[0], e.target]);
		return false;
	});
	
	$('#root')
		.bind('itemclick', function(e, a) {
			updateHash({page:$(a).attr('href').substr(1)});
		});
	
	$('#releases')
		.bind('showpage', function(e) {
			var hash = getHash();
			if (hash.filter) {
				status('Filtering: ' + hash.title);
				$('#releases li').hide();
				$('#releases h1').text(hash.title);
				delay(function() {
					$('#releases li:has(a[href$='+hash.filter+'])').show();
					status();
				});
				
			}
			else {
				status('Filtering: all');
				$('#releases li').hide();
				$('#releases h1').text('Releases');
				delay(function() {
					$('#releases li').show();
					status();
				});
			};
		})
		.bind('itemclick', function(e, a, orig) {
			if (orig.tagName == 'a' && orig.href != a.href) {
				updateHash({
					filter:$(orig).attr('href'),
					title:$(orig).text()
				});
			} 
			else {
				$(e.target)
					.find('div:first')
						.toggleClass('collapsed')
					.end()
					.find('dl')
						.toggleClass('collapsed')
					.end();
			}
		});
	
	$('#artists')
		.bind('itemclick', function(e, a) {
			updateHash({
				page:'releases',
				filter:$(a).attr('href'),
				title:$(a).text()
			});
		});
	
	$('#labels')
		.bind('itemclick', function(e, a) {
			updateHash({
				page:'releases',
				filter:$(a).attr('href'),
				title:$(a).text()
			});
		});
	
	$('#formats')
		.bind('itemclick', function(e, a) {
			updateHash({
				page:'releases',
				filter:$(a).attr('href'),
				title:$(a).text()
			});
		});

	if (location.hash == init) {
		location = location.protocol + '//' + location.host + location.pathname;
	}
	else {
		location.hash = init;
	}
	
	reload();
});

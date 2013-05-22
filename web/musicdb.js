Array.prototype.isArray = true;

m = {
    /*
     * avoid hard-coding column numbers
     */
    ARTIST_COL: 0,
    RELEASE_COL: 1,
    FORMAT_COL: 2,
    LABEL_COL: 3,
    CATNO_COL: 4,
    YEAR_COL: 5,

    /*
     * handlers for form buttons
     */
    formButtons: {
        addArtist: {
            'add':      function() { m.showReleaseTable(); m.loadArtistList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        addLabel: {
            'add':      function() { m.showReleaseTable(); m.loadLabelList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        addFormat: {
            'add':      function() { m.showReleaseTable(); m.loadFormatList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        addRelease: {
            'add':      function() { m.loadReleaseTable(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        editArtist: {
            'update':   function() { m.loadReleaseTable(); m.loadArtistList(); },
            'delete':   function() { m.showReleaseTable(); m.loadArtistList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        editLabel: {
            'update':   function() { m.loadReleaseTable(); m.loadLabelList(); },
            'delete':   function() { m.showReleaseTable(); m.loadLabelList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        editFormat: {
            'update':   function() { m.loadReleaseTable(); m.loadFormatList(); },
            'delete':   function() { m.showReleaseTable(); m.loadFormatList(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        editRelease: {
            'update':   function() { m.loadReleaseTable(); },
            'delete':   function() { m.showReleaseTable(); },
            'cancel':   function() { m.showReleaseTable(); }
        },
        doLogin: {
            'login':    function() { m.showReleaseTable(); },
            'cancel':   function() { m.showReleaseTable(); }
        }
    },

    /*
     * actions for link clicks
     */
    actions: {
        // filter rows based on existence of href's in a column
        filter: function(data) {
            if ('c' in data && 'r' in data) {
                m.showReleaseTable();
                var count = $('#ReleaseTable tbody tr')
                    .hide()
                    .find('td:eq('+data.c+'):has(a[href='+data.r+'])')
                    .closest('tr')
                    .show()
                    .length;
                //console.log('filter: ' + count + ' ' + ;
                document.title = $('#Menu a[href="'+data.r+'"]').text() + ' (' + count + ') - MusicDB';
            }
        },
        // as actions.filter(), but also get related id's from server and show all those
        relatedFilter: function(data) {
            if ('c' in data && 'r' in data) {
                m.showReleaseTable();
                $('#ReleaseTable tbody tr').hide();
                var ref = data.r.replace('/musicdb/', '/musicdb/related/');
                $.get(ref, null, function(result, status, xhr) {
                    var count = 0;
                    $(result).find('*[uri]').each(function() {
                        count += $('#ReleaseTable tbody tr')
                            .find('td:eq('+data.c+'):has(a[href='+$(this).attr('uri')+'])')
                            .closest('tr')
                            .show()
                            .length
                    });
                    document.title = $('#Menu a[href="'+data.r+'"]').text() + ' (' + count + ') - MusicDB';
                });
            }
        },
        // show all rows
        showAll: function(data) {
            m.showReleaseTable();
            var count = $('#ReleaseTable tbody tr').show().length;
            document.title = 'All (' + count + ') - MusicDB';
        },
        // load a form
        loadForm: function(data) {
            if ('n' in data && 'r' in data) {
                m.hideReleaseTable();
                var btn = m.formButtons[data.n];
                $('#Forms').load(data.r, function(responseText, textStatus, xhr) {
                    if (textStatus == 'error')
                        return;
                    $('#Forms')
                        .find('button').each(function() {
                            var buttonName = $(this).attr('name');
                            if (buttonName in btn)
                                $(this).data({Click:{type:'Button', key:buttonName, handler:btn[buttonName]}});
                            else
                                $(this).hide();
                        }).end()
                        .find('#DiscogsLink').data({Click:{type:'Discogs'}}).end()
                        .find('input:eq(0)').focus();
                    m.fixupMultipleSelect();
                    document.title = $('#Forms h1').text() + ' - MusicDB';
                });
            }
        }
    },

    /*
     * event handlers for click events (mostly/entirely consists of replacing location.hash)
     */
    onFilterClick: function(e) {
        var $elem = $(e.target);
        var data = $elem.data('Click');
        var href = $elem.attr('href');
        var hash = m.getHash();
        if (hash.a == 'filter' && hash.r == href && hash.c == data.col && hash.c != m.FORMAT_COL) {
            m.setHash({a:'relatedFilter', r:href, c:data.col});
        }
        else {
            m.setHash({a:'filter', r:href, c:data.col});
        }
    },
    onRelatedFilterClick: function(e) {
        var $elem = $(e.target);
        var data = $elem.data('Click');
        var href = $elem.attr('href');
        m.setHash({a:'relatedFilter', r:href, c:data.col}) 
    },
    onButtonClick: function(e) {
        var $elem = $(e.target),
            data = $elem.data('Click'),
            hash = m.decodeGET(location.hash);
        if ($elem.attr('type') == 'reset') {
            data.handler();
            location.hash = unescape(hash.p);
        } else {
            var $form = $elem.closest('form'),
                action = $form.attr('action'),
                values = $form.serialize()+'&'+data.key+'=';
            //$.post(form.attr('action'), form.serialize()+'&'+data.key+'=', data.handler);
            $.post(action, values, function() {
                data.handler();
                location.hash = unescape(hash.p);
            });
        }
    },
    onLoadFormClick: function(e) {
        var elem = $(e.target);
        var name = elem.data('Click').name;
        var href = elem.attr('href');
        location.hash = m.encodeGET({a:'loadForm', n:name, r:href, p:escape(location.hash.substring(1))});
    },
    onShowAllLinkClick: function(e) {
        location.hash = m.encodeGET({a:'showAll'});
    },
    onLoadFormHoverIn: function(e) {
        // why do I get the event on the <A> and not the <LI> ?
        $(e.target).parent().find('a:eq(1)').show();
    },
    onLoadFormHoverOut: function(e) {
        $(e.target).parent().find('a:eq(1)').fadeOut();
    },

    /*
     * reloading data lists
     */
    loadArtistList: function() { $('#ArtistList').load('/musicdb/artist.xml?xslt=artist.xsl', null, m.initArtistList); },
    loadLabelList: function() { $('#LabelList').load('/musicdb/label.xml?xslt=label.xsl', null, m.initLabelList); },
    loadFormatList: function() { $('#FormatList').load('/musicdb/format.xml?xslt=format.xsl', null, m.initFormatList); },
    loadReleaseTable: function() { $('#Main').load('/musicdb/release.xml?xslt=release.xsl', null, m.initReleaseTable); },
    
    /*
     * (re)initializing data lists
     */
    initArtistList: function() {
        $('#ArtistList li')
            .hover(m.onLoadFormHoverIn, m.onLoadFormHoverOut)
            .find('a:eq(0)')
                .data({Click:{type:'Filter', col:m.ARTIST_COL}})
            .end()
            .find('a:eq(1)')
                .data({Click:{type:'LoadForm', name:'editArtist'}})
                .hide()
            .end();
    },
    initLabelList: function() {
        $('#LabelList li')
            .hover(m.onLoadFormHoverIn, m.onLoadFormHoverOut)
            .find('a:eq(0)')
                .data({Click:{type:'Filter', col:m.LABEL_COL}})
            .end()
            .find('a:eq(1)')
                .data({Click:{type:'LoadForm', name:'editLabel'}})
                .hide()
            .end();
    },
    initFormatList: function() {
        $('#FormatList li')
            .hover(m.onLoadFormHoverIn, m.onLoadFormHoverOut)
            .find('a:eq(0)')
                .data({Click:{type:'Filter', col:m.FORMAT_COL}})
            .end()
            .find('a:eq(1)')
                .data({Click:{type:'LoadForm', name:'editFormat'}})
                .hide()
            .end();
    },
    initReleaseTable: function() {
        $('#ReleaseTable')
            .find('tbody tr')
                .find('td:eq('+m.ARTIST_COL +') a').data({Click:{type:'Filter', col:m.ARTIST_COL}}).end()
                .find('td:eq('+m.RELEASE_COL+') a').data({Click:{type:'LoadForm', name:'editRelease'}}).end()
                .find('td:eq('+m.FORMAT_COL +') a').data({Click:{type:'Filter', col:m.FORMAT_COL}}).end()
                .find('td:eq('+m.LABEL_COL  +') a').data({Click:{type:'Filter', col:m.LABEL_COL}}).end()
            .end()
            .tablesorter({sortList:[[m.YEAR_COL,0], [m.LABEL_COL,0], [m.CATNO_COL,0]]});
        m.showReleaseTable();
        m.doHash();
    },

    /*
     * attach events to menu
     */
    initMenuList: function() {
        $('#AddArtistLink').data({Click:{type:'LoadForm', name:'addArtist'}});
        $('#AddLabelLink').data({Click:{type:'LoadForm', name:'addLabel'}});
        $('#AddFormatLink').data({Click:{type:'LoadForm', name:'addFormat'}});
        $('#AddReleaseLink').data({Click:{type:'LoadForm', name:'addRelease'}});
        $('#LoginLink').data({Click:{type:'LoadForm', name:'doLogin'}});
        $('#ShowAllLink').data({Click:{type:'ShowAllLink'}});
    },
    initMenu: function() {
        $('#Menu').accordion('destroy');
        $('#Menu').accordion({header:'h1', fillSpace:true});
    },
    
    /*
     * set up timer for watching location.hash
     */
    initBackForwardButtons: function() {
        var current = location.hash;
        addEventListener('hashchange', function(e) {
            if (current != location.hash) {
                current = location.hash;
                m.doHash();
            }
        });
    },

    /*
     * encoding and decoding GET parameter strings
     */
    decodeGET: function(args) {
        var result = {};
        args.split('&')
            .map(function(s) { return s.split('=', 2); })
            .map(function(t) { result[t[0]] = unescape(t[1]); });
        return result;
    },
    encodeGET: function(obj) {
        var result = '';
        for (var name in obj) 
            result += (result ? '&' : '')+name+'='+escape(obj[name]);
        return result;
    },

    /*
     * location.hash utility functions
     */
    getHash: function() {
        return m.decodeGET(location.hash.substr(1))
    },
    setHash: function(h) {
        location.hash = m.encodeGET(h);
    },

    /*
     * generating pieces of (X|HT|XHT)ML
     */
    xml: function(node) {
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
    },

    /*
     * replace multi-select list by a more user-friendly multi-select dropdown
     * 
     * form
     * |----label
     * `----select[multiple]
     *      `----option
     * 
     * form
     * |----label
     * `----div
     *      |----select
     *      |    `----option
     *      |----div
     *      |    |----input[hidden]
     *      |    |----span
     *      |    `----a
     *      `----div
     *           |----input[hidden]
     *           |----span
     *           `----a
     */
    fixupMultipleSelect: function() {
        $('#Forms form select[multiple]').each(function() {
            var $select = $(this).wrap(m.xml(['div', {style:'display:inline-block'}])),
                selectName = $select.attr('name');
            $select
                // hook change event handler
                .change(function() {
                    $select.find('option[selected]').each(function() {
                        var $option = $(this);
                        $select.parent()
                            // add div element for each selected item
                            .append(m.xml(['div',
                                ['input', {type:'hidden', name:selectName, value:$option.attr('value')}],
                                ['span', $option.text()],
                                ['a', {href:'#', style:'float:right'}, 'remove']]))
                            // hook click event handler (should probably just use .data)
                            .find('a:last').click(function() {
                                var $parent = $(this).parent(),
                                    $input = $parent.find('input'),
                                    $span = $parent.find('span'),
                                    $options = $select.find('option');
                                for (var i = 1; i < $options.length; i++) {
                                    var $option = $($options[i]);
                                    if ($option.text().toUpperCase() > $span.text().toUpperCase()) {
                                        $option.before(m.xml(['option', {value:$input.attr('value')}, $span.text()]));
                                        $parent.remove();
                                        break;
                                    }
                                }
                                return false;
                            });
                        $option.remove();
                    });
                })
                // run event handler to initialize list
                .change()
                // make it a normal dropdown and don't send value
                .removeAttr('name')
                .removeAttr('multiple')
                // deselect all items
                .find('option').removeAttr('selected').end();
        });
    },

    /*
     * process information in location.hash
     */
    doHash: function() {
        if (!location.hash)
            return;
        var data = m.decodeGET(location.hash.substr(1));
        if ('a' in data)
            m.actions[data.a](data);
    },
    
    /*
     * return event handler for an event name
     */
    dispatcher: function(eventName) {
        return function(e) {
            var event = $(e.target).data(eventName);
            if (!event)
                return;
            var type = event['type'];
            if (type) {
                var handlerName = 'on' + type + eventName;
                var handler = m[handlerName];
                if (handler) {
                    handler(e);
                    e.preventDefault();
                }
            }
        }
    },
    
    /*
     * showing and hiding parts of the interface
     */
    showReleaseTable: function() {
        $('#Main').show();
        $('#Forms').hide();
    },
    hideReleaseTable: function() {
        $('#Main').hide();
        $('#Forms').show();
    },

    /*
     * show error dialog (quite experiMENTAL)
     */
    showError: function(errorText, title) {
        var content = m.xml(['code', ['pre', errorText]]);
        $(content).dialog({
            title: title || 'Error',
            buttons: {
                'OK': function() { 
                    $(this)
                        .dialog('close')
                        .remove();
                }
            },
            modal: true,
            width: 600
        });
    },
    
    /*
     * initialize the JS stuff
     */
    init: function() {
        // show ajax errors 
        $.ajaxSetup({
            error: function(xhr, textStatus, errorThrown) {
                //alert(xhr.responseText); // a bit crummy
                var firstNewLine = xhr.responseText.indexOf('\n'),
                    title = xhr.responseText.substr(0, firstNewLine),
                    message = xhr.responseText.substr(firstNewLine+1);
                m.showError(message, title);
            }
        });

        // attach data to elements for use in event handlers
        m.initMenu();
        m.initMenuList();
        m.initArtistList();
        m.initLabelList();
        m.initFormatList();
        m.initReleaseTable();
        m.initBackForwardButtons();

        // attach event dispatchers
        $('body').click(m.dispatcher('Click'));

        // hide part of interface 
        $('#Forms').hide();
        
        // initialize location.hash
        if (!location.hash)
            location.hash = m.encodeGET({a:'showAll'});
            
        //m.showError('Just testing error dialogs!\n\nThis might be some useful information.\n\nThe quick brown fox jumps over the lazy dogs');
    }
}
$(m.init);

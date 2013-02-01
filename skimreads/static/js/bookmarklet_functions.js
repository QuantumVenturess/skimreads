(function() {
    // check to close iframe
    /*
    setTimeout(checkForClose, 1000);
    */
    
    // minimum version of jQuery
    var v = '1.3.2';
    if (window.jQuery === undefined || window.jQuery.fn.jquery < v) {
        var done = false;
        var script = document.createElement('script');
        script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
        script.onload = script.onreadystatechange = function() {
            if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) {
                done = true;
                gatherData();
            }
        };
        document.getElementsByTagName('head')[0].appendChild(script);
    }
    else {
        gatherData();
    };

    var receiveMessage = function(event) {
        if ('close-iframe' == event.data) {
            var iframe = document.getElementById('skimreadsBookmarkletNewReadingFrame');
            iframe.parentNode.removeChild(iframe);
        }
        console.log(event);
    }
    window.addEventListener('message', receiveMessage, false);

    function checkForClose() {
        if (window.location.hash == '#reading_saved' || window.location.hash == '#reading_canceled') {
            var iframe = document.getElementById('skimreadsBookmarkletNewReadingFrame');
            iframe.parentNode.removeChild(iframe);
        }
        else {
            setTimeout(checkForClose, 1000);
        }
    }

    // create iframe with a popup form inside it for saving reading
    function createFrame(link, note, title) {
        // remove hash in URL
        var pathName = window.location.pathname;
        window.history.replaceState(null, null, pathName);
        // change accordingly for development/production
        var host = 'skimreads.com';
        // var host = 'localhost:8000';
        var url = 'http://' + host + '/readings/new/bookmarklet?link=' + encodeURI(link) + '&title=' + encodeURI(title) + '&note=' + encodeURI(note);
        var f = document.createElement('iframe');
        var fname = 'skimreadsBookmarkletNewReadingFrame';
        f.setAttribute('name', fname);
        f.setAttribute('id', fname);
        f.setAttribute('src', url);
        f.setAttribute('style', 'border:none;bottom:0;height:395px;left:0;margin:0 auto;padding:0;position:fixed;right:0;top:100px;width:1000px;z-index:9999;');
        document.body.appendChild(f);
    }

    // create an iframe and place it in the center of the screen
    function createFrame1(l, n, t) {
        var f = document.createElement('iframe');
        var fname = (+(('' + Math.random()).substring(2))).toString(36);
        f.setAttribute('name', fname);
        f.setAttribute('id', fname);
        f.setAttribute('style', 'border:none;height:0;margin:0;padding:0;position:absolute;width:0;');
        document.body.appendChild(f);
        var note = getSelText();
        var frame = window.frames[fname];
        var doc   = frame.document;
        var script = doc.createElement('script');
        script.setAttribute('type', 'text/javascript');
        // change accordingly for development/production
        script.setAttribute('src', 'http://s3.amazonaws.com/skimreads/js/bookmarklet_frame_functions.js');
        // script.setAttribute('src', '/static/js/bookmarklet_frame_functions.js');
        var link  = doc.createElement('div');
        var note  = doc.createElement('div');
        var title = doc.createElement('div');
        link.setAttribute('id', 'link');
        link.appendChild(doc.createTextNode(l));
        note.setAttribute('id', 'note');
        note.appendChild(doc.createTextNode(n));
        title.setAttribute('id', 'title');
        title.appendChild(doc.createTextNode(t));
        doc.getElementsByTagName('head')[0].appendChild(script);
        doc.body.appendChild(link);
        doc.body.appendChild(note);
        doc.body.appendChild(title);
    };

    function gatherData() {
        var link = window.location;
        var note = getSelText();
        var title = document.title;
        if (note != undefined) {
            createFrame(link, note, title);
        }
    }

    function getSelText() {
        var selText = '';
        if (window.getSelection) {
            selText = window.getSelection();
        }
        else if (document.getSelection) {
            selText = document.getSelection();
        }
        else if (document.selection) {
            selText = document.selection.createRange().text;
        }
        else {
            return selText;
        }
    };
})();
(function() {
    // minimum version of jQuery
    var v = '1.3.2';
    if (window.jQuery === undefined || window.jQuery.fn.jquery < v) {
        var done = false;
        var script = document.createElement('script');
        script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
        script.onload = script.onreadystatechange = function() {
            if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) {
                done = true;
                initBookmarklet();
            }
        };
        document.getElementsByTagName('head')[0].appendChild(script);
    }
    else {
        initBookmarklet();
    };

    function initBookmarklet() {
        (window.myBookmarklet = function() {
            //var host = 'skimreads.com'
            var host = 'localhost:8000'
            var link = window.location;
            var note = '';
            var title = document.title;
            var url = 'http://' + host + '/readings/new/bookmarklet?link=' + encodeURI(link) + '&title=' + encodeURI(title) + '&note=' + encodeURI(note);
            if (note != undefined) {
                popUp(url, 'myWindow', '1000', '400', '100', '200', 'yes');
            }
        })();
    };

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
        if (selText == '') {
            alert('Select a text');
        }
        else {
            return selText;
        }
    };

    function popUp(url, winName, w, h, t, l, scroll) {
        settings = 'height=' + h + ', width=' + w + ', top=' + t + ', left=' + l + ', scrollbars=' + scroll + ', resizable';
        window.open(url, winName, settings);
    };
})();
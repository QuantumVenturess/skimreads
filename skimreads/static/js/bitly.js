$(document).ready(function() {
    $('.twitterShare').each(function() {
        var id = $(this).attr('id');
        var name = $(this).attr('name');
        var url = $(this).attr('url');
        bitly(id, name, url);
    })
})

function bitly(id, name, url) {
    var key = 'R_e50b00dad1da8f68d696f04a09e68f65';
    var username = 'quantumventuress';
    $.ajax({
        url: 'http://api.bit.ly/v3/shorten',
        data: { apiKey: key, login: username, longUrl: url },
        dataType: 'jsonp',
        success: function(results) {
            var shortUrl = results.data.url;
            var twitterUrl = 'https://twitter.com/intent/tweet?original_referer=&text='
            if (shortUrl != undefined) {
                var newUrl = twitterUrl + name + '%20' + shortUrl;
                $('#' + id).attr('href', newUrl);
            }
        }
    })

}
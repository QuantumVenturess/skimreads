$(document).ready(function() {
    var chosen = '';
    $('.searchForm input').live('keyup', function(e) {
        if (e.keyCode != 13 && e.keyCode != 37 && e.keyCode != 38 && e.keyCode != 39 && e.keyCode != 40) {
            var form = $('.searchForm form');
            $('.searchResults').show();
            $.ajax({
                data: { q: $(this).val() },
                type: form.attr('method'),
                url: form.attr('action'),
                success: function(results) {
                    $('.searchResults').html(results.results);
                    $('.searchResults li').removeClass('selected');
                    $('.searchResults ul li:first-child').addClass('selected');
                    chosen = 0;
                }
            })
        }
    })
    // Clicking enter will take you to selected reading
    $('.searchForm input').live('keydown', function(e) {
        if (e.keyCode == 13) {
            var selected = $('.searchResults li.selected');
            if (selected.length == 1) {
                var href = selected.children('a').attr('href');
                document.location.href = href;
            }
        }
    })
    // Clicking on the search form text field will not hide results
    $('.searchForm input').live('click', function() {
        return false;
    })
    // Hide search results
    $(document).live('click', function() {
        $('.searchResults').hide();
    })
    // Submitting the search form should do nothing
    $('.searchForm form').live('submit', function() {
        return false;
    })
    // Keyboard navigation for search results
    $(document).live('keydown', function(e) {
        if ($('.searchResults').is(':visible') && !$('.messageUserList').is(':visible')) {
            // If arrow down is pressed
            if (e.keyCode == 40) {
                if (chosen === '') {
                    chosen = 0;
                }
                else if ((chosen + 1) < $('.searchResults li').length) {
                    chosen++;
                }
                $('.searchResults li').removeClass('selected');
                $('.searchResults li:eq(' + chosen + ')').addClass('selected');
                return false;
            }
            // If arrow up is pressed
            if (e.keyCode == 38) {
                if (chosen === '') {
                    chosen = 0;
                }
                else if (chosen > 0) {
                    chosen--;
                }
                $('.searchResults li').removeClass('selected');
                $('.searchResults li:eq(' + chosen + ')').addClass('selected');
                return false;
            }
        }
    })
    // When hovering over a result, add selected class
    $('.searchResults li').live('mouseover', function() {
        var i = $(this).index();
        $('.searchResults li').removeClass('selected');
        $(this).addClass('selected');
        chosen = i;
    })
})
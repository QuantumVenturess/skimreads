$(document).ready(function() {
    var chosen = '';
    // click to show new message
    $('.newMessageButton, .skimShare').live('click', function() {
        $('#newMessageForm').show();
        $('#newMessageForm #to').focus();
        return false;
    })
    // clicking close closes the new message form
    $('#newMessageForm .action a').live('click', function() {
        $('#newMessageForm').hide();
        return false;
    })
    // when clicking on a list message, take them to detail
    $('.listMessage').live('click', function() {
        var url = $(this).attr('href');
        document.location.href = url;
    })
    // ajax new reply message
    $('.replyMessageForm form').live('submit', function() {
        var content = $('.replyMessageForm textarea');
        if (content.val().length > 0) {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(results) {
                    $('.userMessages').append(results.message);
                    $('.replyMessageForm').html(results.reply_message_form);
                    $('html, body').animate({ scrollTop: $(document).height() }, 0);
                }
            })
        }
        else {
            content.focus();
        }
        return false;
    })
    // do not send new message if to and content empty
    $('#newMessageForm form').live('submit', function() {
        var content = $('#newMessageForm .field textarea');
        var to = $('#newMessageForm .field input');
        if (to.val().length == 0) {
            to.focus();
            return false;
        }
        else if (content.text().length == 0) {
            content.focus();
            return false;
        }
    })
    // when typing recipient's name, show a list of existing users
    $('#newMessageForm #to').live('keyup', function(e) {
        if (e.keyCode != 37 && e.keyCode != 38 && e.keyCode != 39 && e.keyCode != 40) {
            var search = $('#searchUserList');
            var to = $(this).val();
            $('.messageUserList').show();
            $.ajax({
                data: { q: to },
                type: search.attr('method'),
                url: search.attr('action'),
                success: function(results) {
                    $('.messageUserList').html(results.results)
                    $('.messageUserList li').removeClass('selected');
                    $('.messageUserList li:first-child').addClass('selected');
                    chosen = 0;
                }
            })
        }
    })
    // hide search results
    $(document).live('click', function() {
        $('.messageUserList').hide();
    })
    $('.searchForm input').live('click focus', function() {
        $('.messageUserList').hide();
    })
    // when clicking on a recipient's name, load that into the to field
    $('.messageUserList li').live('click', function() {
        $('#to').hide();
        $('#to').val($(this).children('span').text());
        $('.messageUserList ul').remove();
        $('.messageUserInsert').replaceWith($(this))
        $('#newMessageForm .field textarea').focus();
        chosen = 0;
    })
    $('#newMessageForm .field input').live('keydown', function(e) {
        if (e.keyCode == 13) {
            var selected = $('.messageUserList .selected');
            if (selected.length > 0) {
                $('#to').hide();
                $('#to').val(selected.children('span').text());
                $('.messageUserList ul').remove();
                $('.messageUserInsert').replaceWith(selected);
                $('#newMessageForm .field textarea').focus();
                chosen = 0;
            }
            return false;
        }
    })
    // when clicking cancel on a recipient's name
    $('.messageUser a').live('click', function() {
        $(this).closest('.messageUser').replaceWith('<span class="messageUserInsert"></span>');
        $('#to').val('').show();
        $('#to').focus()
        return false;
    })
    // Keyboard navigation for search results
    $(document).live('keydown', function(e) {
        if ($('.messageUserList').is(':visible') && !$('.searchResults').is(':visible') && $('.tagListInsert').is(':visible')) {
            // If arrow down is pressed
            if (e.keyCode == 40) {
                if (chosen === '') {
                    chosen = 0;
                }
                else if ((chosen + 1) < $('.messageUserList li').length) {
                    chosen++;
                }
                $('.messageUserList li').removeClass('selected');
                $('.messageUserList li:eq(' + chosen + ')').addClass('selected');
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
                $('.messageUserList li').removeClass('selected');
                $('.messageUserList li:eq(' + chosen + ')').addClass('selected');
                return false;
            }
        }
    })
    // When hovering over a result, add selected class
    $('.messageUserList li').live('mouseover', function() {
        var i = $(this).index();
        $('.messageUserList li').removeClass('selected');
        $(this).addClass('selected');
        chosen = i;
    })
})
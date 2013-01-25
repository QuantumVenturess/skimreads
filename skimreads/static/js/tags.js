$(document).ready(function() {
    var chosen = '';
    // Autocomplete tag form with tag list
    $(document).on('keyup', '.tagForm #id_tag_name', function(e) {
        if (e.keyCode != 13 && e.keyCode != 37 && e.keyCode != 38 && e.keyCode != 39 && e.keyCode != 40) {
            var content = $(this).val();
            $('.tagListInsert').show();
            $.ajax({
                data: { term: content },
                type: 'GET',
                url: $(this).attr('data-autocomplete-source'),
                success: function(results) {
                    $('.tagListInsert').html(results.tag_list);
                    $('.tagListInsert ul li:first-child').addClass('selected');
                    chosen = 0;
                }
            })
        }
    })
    // Adding a tag
    $(document).on('submit', '.tagForm form', function() {
        /*
        var form = $('.tagForm form');
        var value = $('#id_tag_name').val();
        if (value.match(/^[A-Za-z]+$/) && !value.match(/ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/)) {
            $.ajax({
                data: form.serialize(),
                type: form.attr('method'),
                url: form.attr('action'),
                success: function(results) {
                    $('.tagForm form').remove();
                    $('.tags').html(results.ties)
                }
            })
        }
        else if (!value.match(/^[A-Za-z]+$/)) {
            $('#id_tag_name').focus();
            alert('Use only letters with no spaces')
        }
        else if (value.match(/ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/)) {
            $('#id_tag_name').val('');
            alert('Please use appropriate words');
        }
        */
        return false;
    })
    // pressing enter on an autocomplete option will submit the tie form
    $('.tagForm input').live('keyup', function(e) {
        if (e.keyCode == 13) {
            var form = $('.tagForm form');
            var selected = $('.tagListInsert .selected');
            var value = $('#id_tag_name').val();
            if (value.match(/^[A-Za-z]+$/) && !value.match(/ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/)) {
                if (selected.length == 1) {
                    var text = $.trim(selected.text());
                    $('.tagForm #id_tag_name').val(text);
                }
                $.ajax({
                    data: form.serialize(),
                    type: form.attr('method'),
                    url: form.attr('action'),
                    success: function(results) {
                        $('.tagForm form').remove();
                        $('.tags').html(results.ties)
                    }
                })
            }
            else if (!value.match(/^[A-Za-z]+$/)) {
                $('#id_tag_name').focus();
                alert('Use only letters with no spaces')
            }
            else if (value.match(/ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/)) {
                $('#id_tag_name').val('');
                alert('Please use appropriate words');
            }
            return false;
        }
    })
    // Clicking on an autocomplete option fills the tag form input
    $(document).on('click', '.tagListInsert a', function() {
        var form = $(this).closest('.tagForm form');
        var text = $.trim($(this).text());
        $('.tagForm #id_tag_name').val(text);
        $('.tagListInsert').hide();
        // then submits the form
        $.ajax({
            data: form.serialize(),
            type: form.attr('method'),
            url:  form.attr('action'),
            success: function(results) {
                $('.tagForm form').remove();
                $('.tags').html(results.ties)
            }
        })
    })
    // when hovering over an autocomplete option, add selected class
    $(document).on('mouseover', '.tagListInsert li', function() {
        var i = $(this).index();
        $('.tagListInsert li').removeClass('selected');
        $(this).addClass('selected');
        chosen = i;
    })
    // clicking on the document will hide autocomplete results
    $(document).on('click', document, function() {
        $('.tagListInsert').hide();
    })
    // Keyboard navigation for search results
    $(document).live('keydown', function(e) {
        if (!$('.messageUserList').is(':visible') && !$('.searchResults').is(':visible') && $('.tagListInsert').is(':visible')) {
            // If arrow down is pressed
            if (e.keyCode == 40) {
                if (chosen === '') {
                    chosen = 0;
                }
                else if ((chosen + 1) < $('.tagListInsert ul li').length) {
                    chosen++;
                }
                $('.tagListInsert ul li').removeClass('selected');
                $('.tagListInsert ul li:eq(' + chosen + ')').addClass('selected');
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
                $('.tagListInsert ul li').removeClass('selected');
                $('.tagListInsert ul li:eq(' + chosen + ')').addClass('selected');
                return false;
            }
        }
    })
    /*
    // Clicking on an autocomplete option will submit the tie form
    $('.ui-autocomplete .ui-menu-item a').live('click', function() {
        var form = $('.tagForm form');
        if (form.length > 0) {
            $('.tagForm .field input').val($(this).text());
            $.ajax({
                data: form.serialize(),
                type: form.attr('method'),
                url: form.attr('action'),
                success: function(results) {
                    $('.tagForm form').remove();
                    $('.tags').html(results.ties)
                }
            })
        }
    })
    */
    // Deleting a tag
    $('.tie form').live('submit', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                $('.tagForm').html(results.tag_form);
                $('#tie_' + results.tie_id).remove();
            }
        })
        return false;
    })
})
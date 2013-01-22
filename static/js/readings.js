$(document).ready(function() {
    // Scrape url from reading link
    var readingLinkTimer;
    var readingLinkTypingInterval = 1000;
    var link = $('.readingNew #id_link');
    readingLinkDoneTyping();
    // When finishing typing
    link.live('keyup', function() {
        readingLinkTimer = setTimeout(readingLinkDoneTyping, readingLinkTypingInterval);
    })
    link.live('keydown', function() {
        clearTimeout(readingLinkTimer);
    })
    // When clicking on an image, fill reading image_url
    $('.readingNewImage img').live('click', function() {
        var src = $(this).attr('src');
        $('#id_image').val(src);
        $('.readingNewImage img').removeClass('selected');
        $(this).addClass('selected');
    })
    // Add note to reading new form
    var note1 = $('.noteForms .field:nth-of-type(2)');
    var note2 = $('.noteForms .field:nth-of-type(3)');
    var note1Val = $('.noteForms .field:nth-of-type(2) textarea').val();
    var note2Val = $('.noteForms .field:nth-of-type(3) textarea').val();
    if (note1Val != '') {
        note1.show();
    }
    if (note2Val != '') {
        note2.show();
    }
    if (note1Val != '' && note2Val != '') {
        $('.addNote').hide();
    }
    $('.addNote a').live('click', function() {
        if (!note1.is(':visible') && note2.is(':visible')) {
            note1.show();
            $('.addNote').hide();
        }
        else if (!note1.is(':visible')) {
            note1.show();
        }
        else if (note1.is(':visible') && !note2.is(':visible')) {
            note2.show();
            $('.addNote').hide();
        }
        return false;
    })
    // Deleting a reading
    $('.readingDelete input').live('click', function() {
        var confirm = $('.confirmDelete');
        var form = $('.readingDelete form');
        confirm.dialog({
            height: 100,
            resizable: false,
            buttons: {
                'Delete': function() {
                    $(this).dialog('close');
                    form.submit();
                    return true
                },
                Cancel: function() {
                    $(this).dialog('close');
                }
            }
        })
        return false;
    })
    // social media share
    $('.facebookShare, .twitterShare').popupWindow({
        centerScreen:1,
        height: 375,
        resizable: 1,
        width: 675
    })
})

function readingLinkDoneTyping() {
    var regex = urlRegex()
    var images = $('.readingNewImages');
    var val = $('.readingNew #id_link').val();
    images.html('<p>Loading images...</p>');
    if (val && val.match(regex)) {
        $.ajax({
            data: { 'url': val },
            type: 'GET',
            url: '/readings/new/scrape',
            success: function(results) {
                // Insert scarped images into page
                images.html(results.imgs);
                // Add title to text input
                $('#id_title').val(results.html_title)
                // Masonry for images
                $('.grid img').imagesLoaded(function() {
                    $('.grid').masonry({
                        itemSelector: '.readingNewImage',
                        isFitWidth: true,
                        gutterWidth: 10
                    });
                });
            }
        })
    }
    else {
        images.html('')
    }
}

function urlRegex() {
    var regex = /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/
    return regex
}
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
    // saving a reading from a bookmarklet
    $(document).on('submit', '.bookmarklet .readingNew form', function() {
        var link = $('.bookmarklet .readingNew #id_link');
        var title = $('.bookmarklet .readingNew #id_title');
        if (link.val() == '') {
            link.focus();
        }
        else if (title.val() == '') {
            title.focus();
        }
        else {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url:  $(this).attr('action'),
                success: function(results) {
                    if (results.success == 1) {
                        // window.close();
                        window.parent.document.getElementById('skimreadsBookmarkletNewReadingFrame').parentNode.removeChild(window.parent.document.getElementById('skimreadsBookmarkletNewReadingFrame'));
                    }
                    else {
                        alert('Reading was not saved, please check your data');
                    }
                }
            })
        }
        return false;
    })
    // clicking on the skim it button from reading new page
    $(document).on('click', '.bookmarkletLink a', function() {
        alert('Drag me into your Bookmarks please');
        return false;
    })
})

function readingLinkDoneTyping() {
    var imgRegex = imageRegex();
    var regex = urlRegex()
    var images = $('.readingNewImages');
    var val = $('.readingNew #id_link').val();
    if (val && val.match(regex)) {
        if (val.match(imgRegex)) {
            var ext = val.match(imgRegex)[0];
            var title = val.split('/')[val.split('/').length - 1]
            $('#id_title').val(title.split(ext)[0]);
            $('#id_image').val(val);
            images.html(" \
                <div class='grid'> \
                    <div class='readingNewImage'> \
                        <img class='selected' src='" + val + "'> \
                    </div> \
                </div>")
        }
        else {
            images.html('<p>Loading images...</p>');
            $.ajax({
                data: { 'url': val },
                type: 'GET',
                url: '/readings/new/scrape',
                success: function(results) {
                    // Insert scarped images into page
                    images.html(results.imgs);
                    // Add title to text input if title is blank
                    var title = $('#id_title');
                    if (title.val() == '') {
                        title.val(results.html_title);
                    }
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
    }
    else {
        images.html('')
    }
}

function imageRegex() {
    return /(.jpg|.png|.gif)$/
}

function urlRegex() {
    return /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/
}
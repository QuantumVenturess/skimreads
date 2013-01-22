function moveDiscover() {
    var words = $('.discoverWords p');
    words.animate({ 'margin-left': '-=230' }, 5000, function() {
        words.animate({ 'margin-left': '+=230' }, 0, moveDiscover)
    });
}

function moveSkim() {
    var skim = $('.skim img');
    skim.animate({ 'margin-left': '+=87' }, 2000, function() {
        $(this).animate({ 'margin-left': '-=87' }, 200, moveSkim)
    });
}

function moveSave(obj, count) {
    var n = $('.saveWords span').length;
    if (count >= n) {
        $('.saveWords span').hide();
        setTimeout(function() {
            moveSave($('.saveWords span:first-child'), 0);
        }, 500)
    }
    else {
        obj.show();
        count++;
        setTimeout(function() {
            moveSave(obj.next('span'), count);
        }, 500)
    }
}
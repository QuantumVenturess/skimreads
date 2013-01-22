$(document).ready(function() {
    $('#id_tag_name').autocomplete({
        source: $('#id_tag_name').data('autocomplete-source')
    })
    $('#id_tag_name:not(.ui-autocomplete-input)').live('focus', function() {
        $('#id_tag_name').autocomplete({
            source: $('#id_tag_name').data('autocomplete-source')
        })
    })
})
$(function() {
    $("input[type='number']").keydown(function(event) {
        if (event.shiftKey == true) {
            event.preventDefault();
        }

        if ((event.keyCode >= 48 && event.keyCode <= 57) ||
            (event.keyCode >= 96 && event.keyCode <= 105) ||
            event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 37 ||
            event.keyCode == 39 || event.keyCode == 46 || event.keyCode == 190) {

        } else {
            event.preventDefault();
        }
        if ($(this).hasClass('only-number') && event.keyCode == 190) {
            event.preventDefault();
            //if only numbers disable the "."-button
        } else if ($(this).val().indexOf('.') !== -1 && event.keyCode == 190) {
            event.preventDefault();
            //if a decimal is not allowed, disable the "."-button
        }
    });
});

$(document).ready(function() {
    $('#id_subscription').on('change', function() {
        // Check if subscription video add limit exceed or not
        var $this = $(this);
        var $option = $this.find('option:selected');
        var value = $option.val();
        $.ajax({
            type: "GET",
            url: '/dashboard/vod/check-limit/<>/subs'.replace('<>', value),
            success: function(response) {
                if (!response.success) {
                    swal('Warning !', response.errors, 'warning');
                    $this.val('');
                }
            }
        });
    });

    var currentElement;
    $('.multiple-checkboxes').multiselect({
        includeSelectAllOption: true,
        nonSelectedText: "Select",
        enableFiltering: true,
        maxHeight: 250,
        enableCaseInsensitiveFiltering: true,
        onDropdownShown: function(even) {
          this.$filter.find('.multiselect-search').focus();
        },
        onChange: function(element, checked) {
            console.log('Dropdown closed.');
            var brands = $(this.$select, 'option:selected');
            var selected = [];
            $(brands).each(function(index, brand) {
                selected.push([$(this).val()]);
            });

            if (selected.length > 0) {
                this.$select.removeClass('error');
                this.$select.parent().find('label.error').remove()
            }
        },
        onSelectAll: function(options) {
            this.$select.removeClass('error');
            this.$select.parent().find('label.error').remove()
        }
    });
    
    $('.multiple-single').multiselect({
        nonSelectedText: "Select from list",
        enableFiltering: true,
        maxHeight: 250,
        numberDisplayed: 1,
        enableCaseInsensitiveFiltering: true,
        onDropdownShown: function(even) {
            this.$filter.find('.multiselect-search').focus();
          }
    });
        
    $('.single-withoutsearch').multiselect({
        nonSelectedText: "Select from list",
        maxHeight: 250,
    });
})
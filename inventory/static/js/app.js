$(document).ready(() => {
    returnAsset();    
});

function returnAsset() {
    // Query the button
    $('.return-btn').click(function() {
        event.preventDefault();
        alert('Return button clicked.');
        let clickedButton = $(this);
        let uid = clickedButton.data('uid');
        
        let updateData = {
            'borrower': null,
            'checked_out': false,
            'return_date': null
        };

        $.ajax({
            url: '/api/v1/asset/' + uid,
            type: 'PATCH',
            data: updateData,
            dataType: 'json',
            success: function(data) {
                console.log(data);
                // Remove the 'due back' element from the DOM
                $('#due-back-pg').remove();
                // Remove the 'Marked as Returned' button from the DOM
                $('.return-btn').remove();
                alert('Item has been marked as returned.');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('ERROR: Unable to send HTTPRequest to server.');
            }
        });
    });
}

// CSRF code
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
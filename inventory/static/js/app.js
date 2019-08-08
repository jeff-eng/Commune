$(document).ready(() => {
    getBorrowerList();
    returnAsset();
    deleteAsset();
    asyncAddBorrower();
    asyncAddAsset();
});

function getBorrowerList() {
    $.get('/api/v1/borrower', function(data, status) {
        // Iterate through the values of array
        for (x of data) {
            console.log(x.first_name + ' ' + x.last_name);
            let borrowerName = `${x.first_name} ${x.last_name}`;
            $('#borrower-table').append(`<tr><td>${borrowerName}<td></tr>`);
        }
    });
}

function asyncAddAsset() {
    $('#asset-create-form').submit(function(event) {
        event.preventDefault();

        $.post('/api/v1/asset/create', $('#asset-create-form').serialize(), function(data) {
            console.log('success');

            UIkit.notification('Successfully created new asset!', {pos: 'top-center', status: 'primary', timeout: 3000});
            location.href = '/dashboard';
        });
    });
}

function asyncAddBorrower() {
    let borrowerForm = $('#borrower-create-form');
    
    borrowerForm.submit(function(event) {
        event.preventDefault();
        let borrowerData = {
            'first_name': $('#first').val(),
            'last_name': $('#last').val(),
            'associated_user': $('#borrower-submit').data('pk')
        };

        $.ajax({
            url: '/api/v1/borrower/create',
            type: 'POST',
            data: borrowerData,
            dataType: 'json',
            success: function(data) {
                UIkit.notification('Borrower added!', {pos: 'top-center', status: 'primary', timeout: 3000});
                // Add row to table for the borrower added to database
                $('#borrower-table').append(`<tr><td>${borrowerData.first_name} ${borrowerData.last_name}<td></tr>`);
                // Clear the form
                borrowerForm[0].reset();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }
        });
    });
}

function returnAsset() {
    // Query the button
    $('.return-btn').click(function() {
        event.preventDefault();
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
                // Update text in tags
                $('#detail-borrower').html('None');
                $('#detail-returndate').html('N/A');
                UIkit.notification('Item has been marked as returned.', {pos: 'top-center', status: 'primary', timeout: 3000});
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('ERROR: Unable to send HTTPRequest to server.');
            }
        });
    });
}

function deleteAsset() {
    $('#delete-btn').click(function() {
        event.preventDefault();
        let deleteButton = $(this);
        let uid = deleteButton.data('uid');
        // User confirmation of delete
        event.target.blur();
        UIkit.modal.confirm('Are you sure you want to delete this asset from your inventory?').then(function () {
            console.log('Confirmed.');
            $.ajax({
                url: '/api/v1/asset/' + uid,
                type: 'DELETE',
                success: function(data) {
                    UIkit.notification('Asset has been removed from your inventory.', {pos: 'top-center', status: 'primary', timeout: 3000});
                    // Redirect to dashboard
                    location.href = '/dashboard';
                }
            });
        }, function() {
            console.log('Rejected.');
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
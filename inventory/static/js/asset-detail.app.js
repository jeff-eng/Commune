$(document).ready(() => {
    populateBorrowerDropdownSelect();
    toggleCheckoutAssetButton();
    returnAsset();
    checkOutAsset();
});

function populateBorrowerDropdownSelect() {
    $.get('/api/v1/borrower', function(borrowers) {
        for (borrower of borrowers) {
            $('#checkout-borrower-dropdown').append(`<option value="${borrower.pk}">${borrower.first_name} ${borrower.last_name}</option>`);
        }
    });
}

function toggleCheckoutAssetButton() {
    let uid = $('#asset-detail-header').data('uid');
    // Toggle checkout button based on asset checked out status
    $.get(`/api/v1/asset/${uid}`, function(data) {
        let checkedOut = data.checked_out;
        let checkoutModalBtn = $('#checkout-modal-btn');
        
        if (checkedOut) {
            checkoutModalBtn.prop('disabled', true);
        } else {
            checkoutModalBtn.prop('disabled', false);
        }
    });
}

function returnAsset() {
    // Query the button
    $('#return-btn').click(function() {
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
                // Remove the 'due back' element from the DOM
                $('#due-back-pg').remove();
                // Disable the 'Marked as Returned' button
                $('#return-btn').prop('disabled', true);
                // Re-enable the 'Check Out Asset' button
                $('#checkout-modal-btn').prop('disabled', false);
                // Update text in tags
                $('#detail-borrower').html('None');
                $('#detail-returndate').html('N/A');
                UIkit.notification('Item has been marked as returned.', {pos: 'top-center', status: 'primary', timeout: 3000});
            },
            error: function(jqXHR, textStatus, errorThrown) {
                UIkit.notification('Error encountered. Please try again.', {pos: 'top-center', status: 'danger', timeout: 3000});
            }
        });
    });
}

function checkOutAsset() {
    let checkoutAssetForm = $('#checkout-asset-form');
    checkoutAssetForm.submit(function() {
        event.preventDefault();
        const uid = $('#asset-detail-header').data('uid');
        const borrowerPK = parseInt($('#checkout-borrower-dropdown option:selected').val());
        const duration = parseInt($('#checkout-duration-dropdown option:selected').val());

        if (isNaN(borrowerPK) || isNaN(duration)) {
            UIkit.notification('You must select both a borrower and duration. Try again.', {pos: 'top-center', status: 'danger', timeout: 3000});
            checkoutAssetForm[0].reset();
            return;
        }

        // Calculate the return date using moment.js library based on the user's selected duration 
        let calculatedReturnDate = moment().add(duration, 'days').format('YYYY-MM-DD');

        let updateData = {
            'borrower': borrowerPK,
            'checked_out': true,
            'return_date': calculatedReturnDate
        }

        $.ajax({
            url: `/api/v1/asset/${uid}`,
            type: 'PATCH',
            data: updateData,
            dataType: 'json',
            success: function(asset) {
                // Show user notification
                UIkit.notification(`Successfully checked out ${asset.name}.`, {pos: 'top-center', status: 'success', timeout: 3000});
                
                setTimeout(function() {
                    location.reload();
                }, 3000);

                checkoutAssetForm[0].reset();
            },
            error: function() {
                UIkit.notification('Something went wrong. Unable to check out at this time.', {pos: 'top-center', status: 'danger', timeout: 3000});
                checkoutAssetForm[0].reset();
            }
        });
    });
}


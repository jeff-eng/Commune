$(document).ready(() => {
    asyncPopulateBorrowerList();
    asyncAddBorrower();
    deleteBorrower();
});

function asyncPopulateBorrowerList() {
    $.get('/api/v1/borrower', function(data, status) {
        // Create new array of objects with relevant info
        let borrowers = data.map(function(borrower, index, array) {
            return {
                'pk': borrower.pk,
                'name': `${borrower.first_name} ${borrower.last_name}`,
            };
        });

        if (borrowers.length > 0) {
            borrowers.sort((current, next) => {
                let currentBorrower = current.name.toLowerCase();
                let nextBorrower = next.name.toLowerCase();
                
                // Sort by name
                if (currentBorrower < nextBorrower) {
                    return -1;
                } else if (currentBorrower > nextBorrower) {
                    return 1;
                }
                // Names are equal
                return 0;
            });
            
            // Iterate through the sorted array and append item to unordered list
            for (borrower of borrowers) {
                $('#borrower-list').append($(`<li data-pk="${borrower.pk}">${borrower.name} <a class="delete-borrower-btn" uk-icon="icon: minus-circle" uk-tooltip="title: Delete Borrower; pos: right"></a></li>`));
            }
        } else {
            $('#borrower-list').append('<li>No borrowers to display</li>');
        }
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
            dataType: 'json'
        })
            .done(function(data) {
                UIkit.notification('Borrower added!', {pos: 'top-center', status: 'success', timeout: 3000});
                // Add borrower to the unordered list
                $('#borrower-list').append($(`<li data-pk="${data.pk}">${data.first_name} ${data.last_name} <a class="delete-borrower-btn" uk-icon="icon: minus-circle"></a></li>`));
                // Clear the form
                borrowerForm[0].reset();
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                UIkit.notification('Error: Unable to add borrower at this time. Try again.', {pos: 'top-center', status: 'danger', timeout: 3000});
                borrowerForm[0].reset();
            });
    });
}

function deleteBorrower() {
    $('#borrower-list').on('click', '.delete-borrower-btn', function() {
        event.preventDefault();
        let targetedListItem = $(this).parent()
        let borrowerPrimaryKey = targetedListItem.data('pk');

        UIkit.modal.confirm('Are you sure you want to delete this borrower from your list?').then(function () {
            $.ajax({
                url: '/api/v1/borrower/' + borrowerPrimaryKey,
                type: 'DELETE'
            })
                .done(function() {
                    UIkit.notification('Deleted borrower from your list.', {pos: 'top-center', status: 'success', timeout: 3000});
                    targetedListItem.remove();
                })
                .fail(function() {
                    UIkit.notification('Error: Unable to delete borrower at this time. Try again.', {pos: 'top-center', status: 'danger', timeout: 3000});
                });
        }, function() {
            UIkit.notification('Canceled borrower deletion.', {pos: 'top-center', status: 'warning', timeout: 3000});
        });
    });
}
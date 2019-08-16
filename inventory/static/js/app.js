$(document).ready(() => {
    populateAssetSelect();
    getBorrowerList();
    returnAsset();
    deleteAsset();
    asyncAddBorrower();
    asyncAddAsset();
    deleteBorrower();
});

function populateAssetSelect() {
    let assets;
    // GET request to REST API to retrieve array of asset objects
    $.get('api/v1/asset', function(data, status) {
 
        assets = data.map(function(asset, index, array) {
            return {
                'uid': asset.uid,
                'name': asset.name,
                'manufacturer': asset.manufacturer,
                'model': asset.model,
                'description': asset.description,
                "condition": asset.condition,
                "category": asset.category
            }
        });

        // Populate the select dropdown
        for (let [index, asset] of assets.entries()) {
            $('#manage-asset-select').append($(`<option data-order="${index}">${asset.name}</option>`));
        }
    });

    // Listen for the change event on the select dropdown
    $('#manage-asset-select').change(function() {
        event.preventDefault();
        // Get the UID of the selected option
        let assetIndex = $(this).find(':selected').data('order');
        // Get the object for the item user selected in dropdown
        let selectedAsset = assets[assetIndex];
        // Assign the array from category property in selectedAsset to a named variable
        let categories = selectedAsset.category;
        // Dynamically populate form fields on option selection
        $('#manage-asset-name-input').val(selectedAsset.name);
        $('#manage-asset-manufacturer-input').val(selectedAsset.manufacturer);
        $('#manage-asset-model-input').val(selectedAsset.model);
        $('#manage-asset-description-textarea').val(selectedAsset.description);
        $('#manage-asset-condition-select').val(selectedAsset.condition).change();
        // Iterate through the array of category keys and perform DOM manipulation
        for (category of categories) {
            $('#manage-asset-category-select').val(categories).change();
        }
    });
}

function getBorrowerList() {
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
                $('#borrower-list').append($(`<li data-pk="${borrower.pk}">${borrower.name} <a class="delete-borrower-btn" uk-icon="icon: minus-circle"></a></li>`));
            }
        } else {
            $('#borrower-list').append('<li>No borrowers to display</li>');
        }
    });
}

function asyncAddAsset() {
    $('#asset-create-form').submit(function(event) {
        event.preventDefault();

        $.post('/api/v1/asset/create', $('#asset-create-form').serialize(), function(data) {
            console.log('success');
            
            UIkit.notification('Successfully created new asset!', {pos: 'top-center', status: 'success', timeout: 3000});
            
            setTimeout(function() {
                location.href = '/dashboard';
            }, 4000);
        })
            .fail(function() {
                UIkit.notification('Error: Unable to create new asset.', {pos: 'top-center', status: 'danger', timeout: 3000});
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
            dataType: 'json'
        })
            .done(function(data) {
                UIkit.notification('Borrower added!', {pos: 'top-center', status: 'success', timeout: 3000});
                // Add borrower to the unordered list
                $('#borrower-list').append($(`<li data-pk="${borrowerData.pk}"> <a class="delete-borrower-btn" uk-icon="icon: minus-circle"></a></li>`).text(`${borrowerData.first_name} ${borrowerData.last_name}`));
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
        console.log(borrowerPrimaryKey);

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
            console.log('Cancelled deletion.');
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
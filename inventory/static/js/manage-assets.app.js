$(document).ready(() => {
    populateAssetSelect();
    saveAssetChanges();
});

function populateAssetSelect() {
    let assets;
    // GET request to REST API to retrieve array of asset objects
    $.get('/api/v1/asset', function(data, status) {
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
            $('#manage-asset-select').append($(`<option data-order="${index}" data-uid="${asset.uid}">${asset.name}</option>`));
        }
    });

    // Listen for the change event on the select dropdown
    $('#manage-asset-select').change(function() {
        event.preventDefault();
        // Get the UID of the selected option
        let assetIndex = $(this).find(':selected').data('order');
        // Get the object for the item user selected in dropdown
        let selectedAsset = assets[assetIndex];
        // Dynamically populate form fields on option selection
        $('#manage-asset-name-input').val(selectedAsset.name);
        $('#manage-asset-manufacturer-input').val(selectedAsset.manufacturer);
        $('#manage-asset-model-input').val(selectedAsset.model);
        $('#manage-asset-description-textarea').val(selectedAsset.description);
        $('#manage-asset-condition-select').val(selectedAsset.condition).change();
        $('#manage-asset-category-select').val(selectedAsset.category).change();
        // Insert UID
        $('#manage-asset-delete-btn').attr('data-uid', selectedAsset.uid);
    });
}

function saveAssetChanges() {
    $('#manage-asset-save-btn').click(function() {
        event.preventDefault();

        let uid = $('#manage-asset-select').find(':selected').data('uid');
        let editedAsset = {
            'name': $('input[name=name]').val(),
            'manufacturer': $('input[name=manufacturer]').val(),
            'model': $('input[name=model]').val(),
            'description': $('textarea[name=description]').val(),
            'condition': $('select[name=condition]').find(':selected').val(),
            'category': parseInt($('select[name=category]').find(':selected').val())
        };

        $.ajax({
            url: '/api/v1/asset/' + uid,
            type: 'PATCH',
            data: editedAsset,
            dataType: 'json'
        })
            .done(function(data) {
                UIkit.notification('Changes saved.', {pos: 'top-center', status: 'success', timeout: 3000});
            })
            .fail(function() {
                UIkit.notification('Unable to save changes at this time.', {pos: 'top-center', status: 'danger', timeout: 3000});
            });
    });
}
$(document).ready(() => {
    asyncAddAsset();
});

function asyncAddAsset() {
    $('#asset-create-btn').click(function(event) {
        event.preventDefault();

        let newAssetData = {
            'name': $('input[name=name]').val(),
            'manufacturer': $('input[name=manufacturer]').val(),
            'model': $('input[name=model]').val(),
            'description': $('textarea[name=description]').val(),
            'condition': $('select[name=condition] option:selected').val(),
            'checked_out': false,
            'return_date': null,
            'borrower': null,
            'category': $('select[name=category] option:selected').val()
        };

        $.post('/api/v1/asset/create', newAssetData, function(data) {
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
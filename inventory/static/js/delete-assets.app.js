$(document).ready(() => {
    deleteAsset();
});

function deleteAsset() {
    $('.delete-asset-btn').click(function() {
        event.preventDefault();
        let deleteButton = $(this);
        let uid = deleteButton.data('uid');
        // User confirmation of delete
        UIkit.modal.confirm('Are you sure you want to delete this asset from your inventory?').then(function () {
            $.ajax({
                url: `/api/v1/asset/${uid}`,
                type: 'DELETE',
                success: function(data) {
                    UIkit.notification('Asset has been removed from your inventory.', {pos: 'top-center', status: 'primary', timeout: 3000});
                    // Redirect to dashboard
                    setTimeout(function() {
                        location.href = '/dashboard';
                    }, 4000);
                }
            });
        }, function() {
            UIkit.notification('Delete action canceled.', {pos: 'top-center', status: 'warning', timeout: 3000});
        });
    });
}
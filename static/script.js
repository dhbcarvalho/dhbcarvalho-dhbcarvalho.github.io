$(document).ready(function() {
    $('#submit_button').on('click', function() {
        var form_data = new FormData();
        var file_data = $('#file').prop('files')[0];
        form_data.append('file', file_data);
        
        $.ajax({
            type: 'POST',
            url: '/plot',
            data: form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                document.getElementById('map').innerHTML = data;
            },
        });
    });
});

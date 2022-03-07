$(document).ready(() => {
    $('.file-upload').change(function() {
        const file = this.files[0];
        let $this = $(this);
        var content_name = $(this).attr('data-content');
        var content_type = $(this).attr('data-content-type');
        var action = $(this).attr('data-action');
        var accepted = $(this).attr('accept');
        var get_duration = $(this).attr('data-duration');
        if (accepted) {
            accepted = accepted.split(',');
        }
        var file_type = file.type;
        var file_size = file.size;

        console.log(file_size, file_type);
        if (content_type == 'image' && file_size > 5000000) {
            swal("Error", "Image file size is more than 5MB", "error");
            return;
        } else if (content_type == 'video' && file_size > 5000000) {
            swal("Error", "Video file size is more than 5MB", "error");
            return;
        } else if (file && accepted.indexOf(file_type) !== -1) {
            let reader = new FileReader();
            reader.onload = function(event) {
                var fileName = $this.closest('.file-container').find('.file_name');
                // Upload file to server
                var formData = new FormData();
                formData.append("content_name", content_name);
                formData.append("media_type", file_type);
                formData.append("file_size", file_size);
                formData.append("accepts", accepted);
                formData.append("media_file", file);

                $.ajax({
                    type: "POST",
                    url: action,
                    data: formData,
                    contentType: false,
                    processData: false,
                    beforeSend: function(xhr) {
                        fileName.html('<img src="/static/images/pleasewait.gif" width="100">');
                    },
                    success: function(response) {
                        response = JSON.parse(response);
                        if (response.success) {
                            fileName.html(file.name);
                            $this.closest('.file-container').find('.file-field').val(response.id)
                                // Remove error class and element
                            $this.closest('.file-container').find('.file-field').removeClass('error');
                            $this.closest('.file-container').find('label.error').remove();

                            if (content_type === 'video') {
                                fileName.html(file.name);
                                $this.closest('.form-field-video').find('img').attr('src', response.thumb);
                                if (get_duration === 'true') {
                                    var duration = response.duration.split(':', 2).join(':');
                                    $this.closest('form').find('.duration').val(duration);
                                }
                            } else {
                                fileName.html(response.errors);
                                $this.closest('.form-field-video').find('img').attr('src', event.target.result);
                            }

                        } else {
                            fileName.html(response.errors);
                            $this.closest('.file-container').find('.file-field').val('');
                        }
                    },
                    error: function(request, status, errorThrown) {
                        console.log(errorThrown, request, status);
                        fileName.html(errorThrown);
                    }
                });
            }
            reader.readAsDataURL(file);
        } else {
            swal("Error", "Invalid file type, Only accepts " + accepted, "error");
        }
    });

    $('.upload-box').on('click', function() {
        var src = $(this).find('img').attr('src');
        $('#primg').attr('src', src);
    })
});
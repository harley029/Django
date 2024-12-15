document.addEventListener('DOMContentLoaded', function () {
            const bodyField = document.getElementById('id_body');
            const previewArea = document.getElementById('comment-preview');
            const form = document.getElementById('comment_form');  // Ensure this matches your form's ID
            const errorsDiv = document.getElementById('form-errors');

            function updatePreview() {
                let content = bodyField.value;
                if (content.trim() === '') {
                    previewArea.innerHTML = '<p><em>Your comment will appear here...</em></p>';
                } else {
                    // Optional: Render Markdown here
                    // content = marked(content);
                    // For now, we'll escape HTML tags
                    content = content.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                    previewArea.innerHTML = '<p>' + content + '</p>';
                }
            }

            bodyField.addEventListener('input', updatePreview);
            // Initialize preview
            updatePreview();

            // Add event listener for form submission
            form.addEventListener('submit', function (event) {
                const submitter = event.submitter || document.activeElement;
                if (submitter.name === 'cancel') {
                    // Allow default form submission
                    return;
                }

                event.preventDefault();  // Prevent the default form submission
                const formData = new FormData(form);

                // Send AJAX request
                fetch(form.action, {  // Use form.action to get the correct URL
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Clear the form
                            form.reset();
                            // Reset the preview
                            previewArea.innerHTML = '<p><em>Your comment will appear here...</em></p>';
                            // Redirect to the post detail page or update the comments section
                            window.location.href = "{% url 'posts:post_detail' post.pk %}";
                        } else {
                            // Handle form errors
                            errorsDiv.innerHTML = data.errors_html;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        errorsDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
                    });
            });
        });
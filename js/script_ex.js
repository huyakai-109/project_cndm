document.getElementById('predictButton').addEventListener('click', function () {
    var formData = new FormData();
    var fileInput = document.getElementById('excelFile');
    if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        formData.append('excelFile', file);

        fetch('http://127.0.0.1:5000/predict_excel', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }
                return response.blob();
            })
            .then(blob => {
                // Create a download link for the blob
                var url = window.URL.createObjectURL(blob);
                var downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = 'predicted_results.xlsx';
                downloadLink.textContent = 'Click here to download the predicted results';
                downloadLink.style.display = 'block'; // Make sure the link is visible

                var resultDiv = document.getElementById('uploadResult');
                resultDiv.innerHTML = ''; // Clear previous results
                resultDiv.appendChild(downloadLink);

                // Automatically trigger download for the user
                downloadLink.click();

                // Delay revoking the URL for 30 seconds to ensure user has enough time to interact
                setTimeout(() => {
                    window.URL.revokeObjectURL(url);
                }, 30000);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('uploadResult').textContent = 'An error occurred.';
            });
    } else {
        alert('Please select a file to upload.');
    }
});

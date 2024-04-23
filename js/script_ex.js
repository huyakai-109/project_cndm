document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('predictButton').addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default form submission

        var fileInput = document.getElementById('excelFile');
        if (fileInput.files.length === 0) {
            alert('Please select a file to upload.');
            return;
        }

        var formData = new FormData();
        formData.append('excelFile', fileInput.files[0]);

        fetch('http://127.0.0.1:5000/predict_excel', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob();
            })
            .then(blob => {
                var url = window.URL.createObjectURL(blob);
                var resultDiv = document.getElementById('uploadResult');
                resultDiv.innerHTML = ''; // Clear current results

                var downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = 'predicted_results.xlsx';
                downloadLink.textContent = 'Download Predicted Results';
                resultDiv.appendChild(downloadLink);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                document.getElementById('uploadResult').textContent = 'Unable to download file.';
            });
    });
});

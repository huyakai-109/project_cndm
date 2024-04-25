document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định

    // Lấy giá trị từ form và chuyển đổi sang số khi cần
    const scheducedDate = new Date(document.getElementById('scheduced_date').value);
    const appointmentDate = new Date(document.getElementById('appointment_date').value);

    const formData = {
        Gender: document.getElementById('gender').value === 'Female' ? 1 : 0,
        DaysBetween: parseInt((appointmentDate - scheducedDate)), // Số ngày giữa hai ngày
        Age: parseInt(document.getElementById('age').value, 10),
        Scholarship: document.getElementById('scholarship').checked ? 1 : 0,
        Hipertension: document.getElementById('hypertension').checked ? 1 : 0,
        Diabetes: document.getElementById('diabetes').checked ? 1 : 0,
        Alcoholism: document.getElementById('alcoholism').checked ? 1 : 0,
        Handcap: parseInt(document.getElementById('handicap').value, 10)
    };

    // Gửi yêu cầu đến Flask API
    fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData) // Chuyển đổi data thành JSON
        })
        .then(response => response.json())
        .then(data => {
            // Hiển thị kết quả
            const resultElement = document.getElementById('predictionResult');
            resultElement.innerHTML = `Prediction: ${data.prediction}`;
        })
        .catch(error => {
            // Xử lý lỗi
            console.error('Error when calling the API:', error);
        });
});
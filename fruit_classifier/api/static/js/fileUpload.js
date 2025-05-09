document.addEventListener('DOMContentLoaded', function () {
    const uploadBtn = document.getElementById('upload-btn');
    const uploadForm = document.getElementById('upload-form');
    const cameraContainer = document.getElementById('camera-container');
    const featuresSection = document.getElementById('features-section');
    const fileUploadLabel = document.querySelector('.file-upload-label');
    const imageUpload = document.getElementById('image-upload');

    uploadBtn.addEventListener('click', function () {
        uploadForm.classList.remove('hidden');
        cameraContainer.classList.add('hidden');
        featuresSection.classList.add('hidden');
        if (typeof stopCamera === 'function') stopCamera();
    });

    fileUploadLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadLabel.classList.add('border-green-500', 'bg-green-100');
    });

    fileUploadLabel.addEventListener('dragleave', () => {
        fileUploadLabel.classList.remove('border-green-500', 'bg-green-100');
    });

    fileUploadLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadLabel.classList.remove('border-green-500', 'bg-green-100');
        if (e.dataTransfer.files.length) {
            imageUpload.files = e.dataTransfer.files;
            updateFileLabel();
        }
    });

    imageUpload.addEventListener('change', updateFileLabel);

    function updateFileLabel() {
        if (imageUpload.files.length) {
            const fileName = imageUpload.files[0].name;
            const fileNameDisplay = document.createElement('div');
            fileNameDisplay.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="h-14 w-14 text-green-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-lg font-medium text-gray-700 mb-2">${fileName}</span>
                <span class="text-sm text-gray-500">Click to change file</span>
            `;
            fileUploadLabel.innerHTML = '';
            fileUploadLabel.appendChild(fileNameDisplay);
            fileUploadLabel.appendChild(imageUpload);
        }
    }

    uploadForm.addEventListener('submit', function (e) {
        if (!imageUpload.files.length) {
            e.preventDefault();
            alert('Please select an image to upload');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const cameraBtn = document.getElementById('camera-btn');
    const cameraContainer = document.getElementById('camera-container');
    const uploadForm = document.getElementById('upload-form');
    const featuresSection = document.getElementById('features-section');
    const cameraFeed = document.getElementById('camera-feed');
    const captureBtn = document.getElementById('capture-btn');
    const cameraForm = document.getElementById('camera-form');
    const retakeBtn = document.getElementById('retake-btn');
    const cameraImage = document.getElementById('camera-image');
    let stream = null;

    cameraBtn.addEventListener('click', function () {
        uploadForm.classList.add('hidden');
        cameraContainer.classList.remove('hidden');
        featuresSection.classList.add('hidden');
        startCamera();
    });

    function startCamera() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'environment',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            })
            .then(function (mediaStream) {
                stream = mediaStream;
                cameraFeed.srcObject = mediaStream;
                cameraForm.classList.add('hidden');
                cameraFeed.play();
            })
            .catch(function (error) {
                console.error("Camera access error:", error);
                alert("Could not access the camera. Please check permissions.");
            });
        } else {
            alert("Camera not supported by your browser.");
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            cameraFeed.srcObject = null;
            stream = null;
        }
    }

    window.stopCamera = stopCamera; // expose globally so upload.js can use it

    captureBtn.addEventListener('click', function () {
        if (!stream) return;

        const canvas = document.createElement('canvas');
        canvas.width = cameraFeed.videoWidth;
        canvas.height = cameraFeed.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/jpeg');
        cameraImage.value = imageData;

        let previewImage = document.getElementById('preview-image');
        if (!previewImage) {
            previewImage = document.createElement('img');
            previewImage.id = 'preview-image';
            previewImage.className = 'w-full rounded-xl shadow-xl object-cover h-96 hidden';
            cameraContainer.insertBefore(previewImage, cameraForm);
        }
        previewImage.src = imageData;

        cameraFeed.classList.add('hidden');
        previewImage.classList.remove('hidden');
        cameraForm.classList.remove('hidden');
    });

    retakeBtn.addEventListener('click', function () {
        cameraForm.classList.add('hidden');
        const previewImage = document.getElementById('preview-image');
        if (previewImage) previewImage.classList.add('hidden');
        cameraFeed.classList.remove('hidden');
        cameraFeed.play();
    });

    cameraForm.addEventListener('submit', function (e) {
        if (!cameraImage.value) {
            e.preventDefault();
            alert('Please capture an image first');
        }
    });

    window.addEventListener('beforeunload', function () {
        stopCamera();
    });
});

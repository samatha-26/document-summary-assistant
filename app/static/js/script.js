// Enhanced JavaScript for modern UI interactions
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const fileInput = document.getElementById('file');
    const uploadArea = document.getElementById('uploadArea');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFile = document.getElementById('removeFile');
    const submitBtn = document.getElementById('submitBtn');

    // Drag and drop functionality
    if (uploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            uploadArea.classList.add('dragover');
        }

        function unhighlight(e) {
            uploadArea.classList.remove('dragover');
        }

        uploadArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            handleFiles(e.target.files);
        });
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            displayFileInfo(file);
        }
    }

    function displayFileInfo(file) {
        const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            showFlashMessage('Please upload a valid file type: PDF or image (PNG, JPG, JPEG, GIF).', 'error');
            return;
        }

        // Update file info display
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'flex';

        // Hide upload area text and show file info
        uploadArea.style.display = 'none';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Remove file handler
    if (removeFile) {
        removeFile.addEventListener('click', function() {
            fileInput.value = '';
            fileInfo.style.display = 'none';
            uploadArea.style.display = 'block';
        });
    }

    // Form submission handler
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!fileInput.files[0]) {
                showFlashMessage('Please select a file to upload.', 'error');
                e.preventDefault();
                return;
            }

            const file = fileInput.files[0];
            const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                showFlashMessage('Please upload a valid file type: PDF or image (PNG, JPG, JPEG, GIF).', 'error');
                e.preventDefault();
                return;
            }

            // Show loading state
            submitBtn.innerHTML = '<span class="btn-text">Processing...</span><span class="btn-icon">⏳</span>';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
        });
    }

    // Flash message function
    function showFlashMessage(message, type = 'error') {
        // Remove existing flash messages
        const existingFlashes = document.querySelectorAll('.flash-temp');
        existingFlashes.forEach(flash => flash.remove());

        // Create new flash message
        const flashDiv = document.createElement('div');
        flashDiv.className = `flash ${type} flash-temp`;
        flashDiv.innerHTML = `
            <span class="flash-icon">${type === 'error' ? '❌' : '✅'}</span>
            <span class="flash-text">${message}</span>
        `;

        const flashContainer = document.querySelector('.flash-messages') || document.querySelector('.upload-card');
        if (flashContainer) {
            flashContainer.insertBefore(flashDiv, flashContainer.firstChild);
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (flashDiv.parentNode) {
                flashDiv.remove();
            }
        }, 5000);
    }

    // Add smooth scrolling and animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Add loading animation for buttons
    document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });

        btn.addEventListener('mouseup', function() {
            this.style.transform = '';
        });

        btn.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
});

// LOGODETH - Metal Logo Recognition Engine JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImage = document.getElementById('previewImage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const chooseFileBtn = document.getElementById('chooseFileBtn');
    const chooseAnotherBtn = document.getElementById('chooseAnotherBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');

    // Mock database of metal band logos and their names
    const metalBands = [
        { name: 'Disentomb', confidence: 0.921, genre: 'Brutal Death Metal' },
        { name: 'Defeated Sanity', confidence: 0.884, genre: 'Technical Death Metal' },
        { name: 'Visceral Disgorge', confidence: 0.861, genre: 'Slam Death Metal' },
        { name: 'Cryptopsy', confidence: 0.847, genre: 'Technical Death Metal' },
        { name: 'Dying Fetus', confidence: 0.823, genre: 'Death Metal' },
        { name: 'Cannibal Corpse', confidence: 0.812, genre: 'Death Metal' },
        { name: 'Bloodbath', confidence: 0.798, genre: 'Death Metal' },
        { name: 'Suffocation', confidence: 0.785, genre: 'Death Metal' },
        { name: 'Necrophagist', confidence: 0.772, genre: 'Technical Death Metal' },
        { name: 'Gorguts', confidence: 0.759, genre: 'Technical Death Metal' },
        { name: 'Mayhem', confidence: 0.945, genre: 'Black Metal' },
        { name: 'Darkthrone', confidence: 0.923, genre: 'Black Metal' },
        { name: 'Emperor', confidence: 0.901, genre: 'Symphonic Black Metal' },
        { name: 'Burzum', confidence: 0.887, genre: 'Atmospheric Black Metal' },
        { name: 'Immortal', confidence: 0.874, genre: 'Black Metal' },
        { name: 'Bathory', confidence: 0.856, genre: 'Black Metal' },
        { name: 'Gorgoroth', confidence: 0.843, genre: 'Black Metal' },
        { name: 'Marduk', confidence: 0.829, genre: 'Black Metal' },
        { name: 'Watain', confidence: 0.815, genre: 'Black Metal' },
        { name: 'Behemoth', confidence: 0.802, genre: 'Blackened Death Metal' }
    ];

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // File selection buttons
    chooseFileBtn.addEventListener('click', () => fileInput.click());
    chooseAnotherBtn.addEventListener('click', showUploadArea);

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeImage);

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    }

    function handleFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showError('Please select a valid image file.');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showError('File size must be less than 10MB.');
            return;
        }

        // Display preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            uploadArea.style.display = 'none';
            previewArea.style.display = 'block';
            resultsSection.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    function showUploadArea() {
        // Reset file input
        fileInput.value = '';
        // Show upload area and hide preview
        uploadArea.style.display = 'block';
        previewArea.style.display = 'none';
        resultsSection.style.display = 'none';
    }

    function analyzeImage() {
        // Show loading state
        analyzeBtn.innerHTML = '<span class="loading"></span> ANALYZING...';
        analyzeBtn.disabled = true;

        // Simulate analysis delay
        setTimeout(() => {
            // Generate mock results
            const results = generateMockResults();
            displayResults(results);
            
            // Reset button
            analyzeBtn.innerHTML = '⚡ ANALYZE LOGO ⚡';
            analyzeBtn.disabled = false;
        }, 2000 + Math.random() * 2000); // 2-4 seconds
    }

    function generateMockResults() {
        // Randomly select 3-5 bands from the database
        const numResults = Math.floor(Math.random() * 3) + 3; // 3-5 results
        const shuffled = [...metalBands].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, numResults);
        
        // Add some randomness to confidence scores
        return selected.map((band, index) => ({
            ...band,
            confidence: Math.max(0.5, band.confidence - (index * 0.05) + (Math.random() * 0.1 - 0.05))
        })).sort((a, b) => b.confidence - a.confidence);
    }

    function displayResults(results) {
        resultsContainer.innerHTML = '';
        
        results.forEach((result, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            resultItem.innerHTML = `
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span class="result-rank">${index + 1}.</span>
                    <div style="flex: 1;">
                        <div class="result-band">${result.name}</div>
                        <div class="result-confidence">Confidence: ${(result.confidence * 100).toFixed(1)}% • ${result.genre}</div>
                    </div>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
                </div>
            `;
            
            resultsContainer.appendChild(resultItem);
        });
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #ff0000, #cc0000);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
            z-index: 1000;
            font-weight: bold;
            animation: slideIn 0.3s ease;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 3 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }

    // Add CSS animation for error notification
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);

    // Add some interactive effects
    addInteractiveEffects();
});

function addInteractiveEffects() {
    // Add hover effects to steps
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => {
        step.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        step.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click effect to logo title
    const logoTitle = document.querySelector('.logo-title');
    logoTitle.addEventListener('click', function() {
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'flicker 2s infinite alternate';
        }, 100);
    });

    // Add parallax effect to background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('body::before');
        // Subtle parallax effect through CSS custom properties
        document.documentElement.style.setProperty('--scroll', scrolled * 0.5 + 'px');
    });

    // Add typing effect to quote
    const quote = document.querySelector('.quote em');
    if (quote) {
        const text = quote.textContent;
        quote.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                quote.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        
        // Start typing when quote comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeWriter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(quote);
    }
}

// Add some brutal sound effects (optional - commented out to avoid autoplay issues)
/*
function playBrutalSound() {
    // You could add some metal sound effects here
    // const audio = new Audio('path/to/brutal-sound.mp3');
    // audio.volume = 0.1;
    // audio.play().catch(() => {}); // Ignore autoplay restrictions
}
*/

// Easter egg: Konami code for extra brutality
let konamiCode = [];
const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateBrutalMode();
        konamiCode = [];
    }
});

function activateBrutalMode() {
    document.body.style.animation = 'brutal-shake 0.5s ease-in-out';
    document.querySelector('.logo-title').textContent = 'LOGODETH 🔥💀🔥';
    
    // Add brutal mode CSS
    const brutalStyle = document.createElement('style');
    brutalStyle.textContent = `
        @keyframes brutal-shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
            20%, 40%, 60%, 80% { transform: translateX(2px); }
        }
        
        .brutal-mode {
            filter: contrast(1.2) saturate(1.3);
        }
    `;
    document.head.appendChild(brutalStyle);
    
    setTimeout(() => {
        document.body.style.animation = '';
        document.body.classList.add('brutal-mode');
    }, 500);
}
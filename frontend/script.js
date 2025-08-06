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

    // API configuration with environment detection
    const API_BASE_URL = (() => {
        // Check if we're in development or production
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000/api/v1';
        } else {
            // Production environment - use relative URLs
            return '/api/v1';
        }
    })();
    
    // Logo recognition API client
    class LogoRecognitionAPI {
        constructor(baseUrl) {
            this.baseUrl = baseUrl;
        }
        
        async recognizeLogo(file, options = {}) {
            const formData = new FormData();
            formData.append('file', file);
            
            // Add optional parameters
            if (options.provider_preference) {
                formData.append('provider_preference', JSON.stringify(options.provider_preference));
            }
            if (options.force_refresh) {
                formData.append('force_refresh', 'true');
            }
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
            
            try {
                const response = await fetch(`${this.baseUrl}/recognize`, {
                    method: 'POST',
                    body: formData,
                    signal: controller.signal,
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    let errorMessage;
                    try {
                        const errorData = await response.json();
                        errorMessage = errorData.detail?.message || errorData.message || errorData.detail;
                    } catch {
                        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
                    }
                    throw new Error(errorMessage);
                }
                
                return await response.json();
                
            } catch (error) {
                clearTimeout(timeoutId);
                if (error.name === 'AbortError') {
                    throw new Error('Request timeout - the analysis took too long. Please try again.');
                }
                throw error;
            }
        }
        
        async getHealth() {
            try {
                const response = await fetch(`${this.baseUrl.replace('/api/v1', '')}/health`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                if (!response.ok) {
                    return { status: 'unhealthy', error: `HTTP ${response.status}` };
                }
                
                return await response.json();
            } catch (error) {
                return { status: 'unreachable', error: error.message };
            }
        }
        
        async getCacheStats() {
            try {
                const response = await fetch(`${this.baseUrl}/cache/stats`);
                if (!response.ok) return null;
                return await response.json();
            } catch {
                return null;
            }
        }
    }
    
    // Initialize API client
    const logoAPI = new LogoRecognitionAPI(API_BASE_URL);
    
    // Store current file for analysis
    let currentFile = null;

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
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type.toLowerCase())) {
            showError('Please select a valid image file (JPG, PNG, GIF, WebP).');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showError('File size must be less than 10MB.');
            return;
        }

        // Store file for analysis
        currentFile = file;

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
        // Reset file input and current file
        fileInput.value = '';
        currentFile = null;
        // Show upload area and hide preview
        uploadArea.style.display = 'block';
        previewArea.style.display = 'none';
        resultsSection.style.display = 'none';
    }

    async function analyzeImage() {
        if (!currentFile) {
            showError('Please select an image file first.');
            return;
        }

        // Show loading state
        analyzeBtn.innerHTML = '<span class="loading"></span> ANALYZING...';
        analyzeBtn.disabled = true;
        
        // Add progress indicator
        showProgress('Checking API status...');

        try {
            // Check API health first
            const health = await logoAPI.getHealth();
            if (health.status !== 'healthy') {
                throw new Error(`API server is ${health.status}: ${health.error || 'Unknown error'}`);
            }
            
            // Show file upload progress
            updateProgress('Uploading image...');
            
            // Get analysis options from UI (could add provider selection UI later)
            const options = {
                provider_preference: getPreferredProviders(),
                force_refresh: false  // Could add "Refresh Cache" button later
            };
            
            updateProgress('Analyzing with AI...');
            
            const result = await logoAPI.recognizeLogo(currentFile, options);
            
            updateProgress('Processing results...');
            
            // Display results
            displayResults([result]);
            
            // Show success message with more details
            if (result._cache_metadata?.cached_at) {
                const cacheAge = getCacheAge(result._cache_metadata.cached_at);
                showSuccess(`✨ Result retrieved from cache (${cacheAge})!`);
            } else {
                showSuccess(`🤖 Analyzed using ${result.ai_model || 'AI'}!`);
            }
            
        } catch (error) {
            console.error('Logo recognition failed:', error);
            
            // Show user-friendly error message with better diagnostics
            if (error.message.includes('CORS')) {
                showError('❌ API server not accessible due to CORS policy. Please check server configuration.');
            } else if (error.message.includes('timeout') || error.message.includes('AbortError')) {
                showError('❌ Request timed out. The analysis is taking too long. Please try again.');
            } else if (error.message.includes('fetch') || error.message.includes('NetworkError')) {
                showError('❌ Cannot connect to API server. Please check if the backend is running.');
            } else if (error.message.includes('unreachable')) {
                showError('❌ API server is unreachable. Please check the server status.');
            } else {
                showError(`❌ Recognition failed: ${error.message}`);
            }
            
            // Hide results on error
            resultsSection.style.display = 'none';
            
        } finally {
            // Reset button state
            analyzeBtn.innerHTML = '⚡ ANALYZE LOGO ⚡';
            analyzeBtn.disabled = false;
            hideProgress();
        }
    }

    function displayResults(results) {
        resultsContainer.innerHTML = '';
        
        // Handle single result (from API) differently than multiple results
        results.forEach((result, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            // Format confidence (API returns 0-100, but display as percentage)
            const confidence = result.confidence || 0;
            const confidencePercent = confidence > 1 ? confidence : confidence * 100;
            
            // Extract cache info
            const isCached = result._cache_metadata?.cached_at;
            const cacheAge = isCached ? getCacheAge(result._cache_metadata.cached_at) : null;
            
            resultItem.innerHTML = `
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span class="result-rank">${index + 1}.</span>
                    <div style="flex: 1;">
                        <div class="result-band">${escapeHtml(result.band_name || result.name || 'Unknown')}</div>
                        <div class="result-confidence">
                            Confidence: ${confidencePercent.toFixed(1)}%
                            ${result.genre ? ` • ${escapeHtml(result.genre)}` : ''}
                            ${isCached ? ` • 💾 Cached (${cacheAge})` : ''}
                        </div>
                        ${result.description ? `<div class="result-description">${escapeHtml(result.description)}</div>` : ''}
                        <div class="result-metadata">
                            ${result.ai_model ? `<span class="result-model">Model: ${escapeHtml(result.ai_model)}</span>` : ''}
                            ${result.processing_time_ms ? `<span class="result-timing">• ${result.processing_time_ms}ms</span>` : ''}
                        </div>
                    </div>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                </div>
            `;
            
            resultsContainer.appendChild(resultItem);
        });
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Progress indicator
    let progressElement;
    
    function showProgress(message) {
        progressElement = document.createElement('div');
        progressElement.id = 'progress-indicator';
        progressElement.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(45deg, #8B0000, #DC143C);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(139, 0, 0, 0.4);
            z-index: 1001;
            font-weight: bold;
            animation: slideDown 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        
        progressElement.innerHTML = `
            <div class="progress-spinner"></div>
            <span>${message}</span>
        `;
        
        document.body.appendChild(progressElement);
    }
    
    function updateProgress(message) {
        if (progressElement) {
            const span = progressElement.querySelector('span');
            if (span) span.textContent = message;
        }
    }
    
    function hideProgress() {
        if (progressElement) {
            progressElement.remove();
            progressElement = null;
        }
    }

    function showError(message) {
        showNotification(message, 'error');
    }
    
    function showSuccess(message) {
        showNotification(message, 'success');
    }
    
    function showNotification(message, type = 'info') {
        const colors = {
            error: { bg: 'linear-gradient(45deg, #ff0000, #cc0000)', shadow: 'rgba(255, 0, 0, 0.3)' },
            success: { bg: 'linear-gradient(45deg, #008000, #006400)', shadow: 'rgba(0, 128, 0, 0.3)' },
            info: { bg: 'linear-gradient(45deg, #4169E1, #0000CD)', shadow: 'rgba(65, 105, 225, 0.3)' }
        };
        
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type].bg};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px ${colors[type].shadow};
            z-index: 1000;
            font-weight: bold;
            animation: slideIn 0.3s ease;
            max-width: 400px;
            word-wrap: break-word;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }

    // Add CSS animations and styles
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
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes slideDown {
            from {
                transform: translateX(-50%) translateY(-100%);
                opacity: 0;
            }
            to {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }
        }
        
        .progress-spinner {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top: 2px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-description {
            color: #ccc;
            font-size: 0.9em;
            margin-top: 5px;
            font-style: italic;
        }
        
        .result-metadata {
            color: #888;
            font-size: 0.8em;
            margin-top: 3px;
        }
        
        .result-model, .result-timing {
            margin-right: 10px;
        }
    `;
    document.head.appendChild(style);

    // Add some interactive effects
    addInteractiveEffects();
    
    // Initialize health monitoring
    initHealthMonitoring();
});

// Utility functions
function getPreferredProviders() {
    // Could be configured via UI settings later
    return ['openai', 'anthropic'];
}

function getCacheAge(cachedAt) {
    try {
        const cached = new Date(cachedAt);
        const now = new Date();
        const diffMs = now - cached;
        
        if (diffMs < 60000) {
            return 'just now';
        } else if (diffMs < 3600000) {
            return `${Math.floor(diffMs / 60000)}m ago`;
        } else if (diffMs < 86400000) {
            return `${Math.floor(diffMs / 3600000)}h ago`;
        } else {
            return `${Math.floor(diffMs / 86400000)}d ago`;
        }
    } catch {
        return 'unknown age';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function initHealthMonitoring() {
    // Check API health on page load
    setTimeout(async () => {
        try {
            const health = await logoAPI.getHealth();
            if (health.status !== 'healthy') {
                showNotification(`⚠️ API Status: ${health.status}`, 'info');
            }
        } catch (error) {
            console.warn('Health check failed:', error);
        }
    }, 1000);
}

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
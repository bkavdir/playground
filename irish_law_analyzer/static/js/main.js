document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const loadingIndicator = document.querySelector('.loading-indicator');
    const resultsSection = document.getElementById('results');
    const fileInput = document.querySelector('.file-input');

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultsSection.style.display = 'none';
        
        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the document.');
        } finally {
            loadingIndicator.style.display = 'none';
        }
    });

    function displayResults(data) {
        resultsSection.style.display = 'block';
        
        // Display risk score
        const riskScoreDiv = document.getElementById('riskScore');
        riskScoreDiv.innerHTML = `
            <div class="risk-score risk-${data.analysis.overall_risk_level.toLowerCase()}">
                Risk Score: ${data.analysis.risk_score}
                <div class="risk-level">${data.analysis.overall_risk_level}</div>
            </div>
        `;

        // Display findings
        const findingsDiv = document.getElementById('findings');
        findingsDiv.innerHTML = `
            <ul class="findings-list">
                ${data.analysis.findings.map(finding => `
                    <li class="finding-item ${finding.risk_level.toLowerCase()}">
                        <strong>${finding.category}:</strong> ${finding.keyword}
                        <div class="context">${finding.context}</div>
                        <div class="occurrences">Occurrences: ${finding.occurrences}</div>
                    </li>
                `).join('')}
            </ul>
        `;

        // Display recommendations
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = `
            <ul class="recommendations-list">
                ${data.analysis.recommendations.map(rec => `
                    <li class="recommendation-item">${rec}</li>
                `).join('')}
            </ul>
        `;
    }

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileInput.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileInput.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileInput.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        fileInput.classList.add('highlight');
    }

    function unhighlight(e) {
        fileInput.classList.remove('highlight');
    }

    fileInput.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        document.querySelector('input[type="file"]').files = files;
    }
});
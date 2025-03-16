document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            tabBtns.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
    
    // Generator form submission
    const generatorForm = document.getElementById('generator-form');
    generatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const goal = document.getElementById('goal').value.trim();
        if (!goal) {
            alert('Please enter your goal');
            return;
        }
        
        const targetModel = document.getElementById('target-model').value;
        const style = document.getElementById('style').value;
        const context = document.getElementById('context').value;
        
        // Get selected format options
        const formatCheckboxes = document.querySelectorAll('input[name="format"]:checked');
        const formats = Array.from(formatCheckboxes).map(cb => cb.value);
        
        try {
            // Show loading state (could add spinner here)
            const resultContainer = document.getElementById('generator-result');
            const promptOutput = document.getElementById('generated-prompt');
            promptOutput.textContent = "Generating prompt...";
            resultContainer.classList.remove('hidden');
            
            // API call to generate prompt
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    goal,
                    target_model: targetModel,
                    context,
                    style,
                    formats
                })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                promptOutput.textContent = data.prompt;
            } else {
                promptOutput.textContent = "Error generating prompt: " + data.detail;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating the prompt');
        }
    });
    
    // Optimizer form submission
    const optimizerForm = document.getElementById('optimizer-form');
    optimizerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const prompt = document.getElementById('existing-prompt').value.trim();
        if (!prompt) {
            alert('Please enter your existing prompt');
            return;
        }
        
        const targetModel = document.getElementById('opt-target-model').value;
        const optimizationLevel = document.getElementById('optimization-level').value;
        
        try {
            // Show loading state
            const resultContainer = document.getElementById('optimizer-result');
            const promptOutput = document.getElementById('optimized-prompt');
            promptOutput.textContent = "Optimizing prompt...";
            resultContainer.classList.remove('hidden');
            
            // API call to optimize prompt
            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt,
                    target_model: targetModel,
                    optimization_level: optimizationLevel
                })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                promptOutput.textContent = data.optimized_prompt;
                
                // Display optimization notes (placeholders for now)
                const notesList = document.getElementById('optimization-notes');
                notesList.innerHTML = '';
                
                const improvements = [
                    "Added clear structure and formatting",
                    "Enhanced clarity of instructions",
                    "Optimized for specific model capabilities",
                    "Added constraints for more focused output"
                ];
                
                improvements.forEach(note => {
                    const li = document.createElement('li');
                    li.textContent = note;
                    notesList.appendChild(li);
                });
            } else {
                promptOutput.textContent = "Error optimizing prompt: " + data.detail;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while optimizing the prompt');
        }
    });
    
    // Test prompt functionality
    const runTestBtn = document.getElementById('run-test');
    runTestBtn.addEventListener('click', async () => {
        const prompt = document.getElementById('test-prompt').value.trim();
        if (!prompt) {
            alert('Please enter a prompt to test');
            return;
        }
        
        const model = document.getElementById('test-model').value;
        
        try {
            // Show loading state
            const loadingContainer = document.getElementById('test-loading');
            loadingContainer.classList.remove('hidden');
            
            const resultContainer = document.getElementById('test-result');
            resultContainer.classList.add('hidden');
            
            // API call to test prompt
            const response = await fetch('/api/test-prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt,
                    target_model: model
                })
            });
            
            const data = await response.json();
            
            // Hide loading, show results
            loadingContainer.classList.add('hidden');
            resultContainer.classList.remove('hidden');
            
            if (data.status === 'success') {
                document.getElementById('test-response').textContent = data.result;
            } else {
                document.getElementById('test-response').textContent = "Error testing prompt: " + data.detail;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while testing the prompt');
            
            // Hide loading state on error
            document.getElementById('test-loading').classList.add('hidden');
        }
    });
    
    // Copy buttons functionality
    document.getElementById('copy-generator').addEventListener('click', () => {
        copyToClipboard('generated-prompt');
    });
    
    document.getElementById('copy-optimizer').addEventListener('click', () => {
        copyToClipboard('optimized-prompt');
    });
    
    document.getElementById('copy-test-result').addEventListener('click', () => {
        copyToClipboard('test-response');
    });
    
    function copyToClipboard(elementId) {
        const element = document.getElementById(elementId);
        const text = element.textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!');
        }).catch(err => {
            console.error('Could not copy text: ', err);
        });
    }
    
    // Save prompt functionality
    const saveModal = document.getElementById('save-modal');
    const saveButtons = [document.getElementById('save-generator'), document.getElementById('save-optimizer')];
    let currentPromptToSave = '';
    
    saveButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Get prompt from the appropriate container
            if (btn.id === 'save-generator') {
                currentPromptToSave = document.getElementById('generated-prompt').textContent;
            } else {
                currentPromptToSave = document.getElementById('optimized-prompt').textContent;
            }
            
            // Show save modal
            saveModal.classList.add('active');
        });
    });
    
    // Close modal functionality
    document.querySelector('.close-modal').addEventListener('click', () => {
        saveModal.classList.remove('active');
    });
    
    document.getElementById('cancel-save').addEventListener('click', () => {
        saveModal.classList.remove('active');
    });
    
    // Save prompt to library
    document.getElementById('confirm-save').addEventListener('click', () => {
        const name = document.getElementById('prompt-name').value.trim();
        if (!name) {
            alert('Please provide a name for your prompt');
            return;
        }
        
        const description = document.getElementById('prompt-description').value.trim();
        const tagsString = document.getElementById('prompt-tags').value.trim();
        const tags = tagsString ? tagsString.split(',').map(tag => tag.trim()) : [];
        
        // In a real app, we would save to the server/database
        // For now, we'll save to localStorage
        savePromptToLibrary(name, description, tags, currentPromptToSave);
        
        // Close modal and reset form
        saveModal.classList.remove('active');
        document.getElementById('prompt-name').value = '';
        document.getElementById('prompt-description').value = '';
        document.getElementById('prompt-tags').value = '';
        
        // Show success message
        showToast('Prompt saved to library!');
        
        // Update library display if we're on that tab
        if (document.getElementById('library-tab').classList.contains('active')) {
            loadLibrary();
        }
    });
    
    // Library functionality
    function savePromptToLibrary(name, description, tags, promptText) {
        // Get existing library or initialize new one
        const library = JSON.parse(localStorage.getItem('promptLibrary') || '[]');
        
        // Create new prompt entry
        const newPrompt = {
            id: Date.now(), // Simple unique ID
            name,
            description,
            tags,
            prompt: promptText,
            model: document.getElementById('target-model').value || document.getElementById('opt-target-model').value,
            date: new Date().toISOString()
        };
        
        // Add to library
        library.push(newPrompt);
        
        // Save back to localStorage
        localStorage.setItem('promptLibrary', JSON.stringify(library));
    }
    
    function loadLibrary() {
        const library = JSON.parse(localStorage.getItem('promptLibrary') || '[]');
        const promptCardsContainer = document.getElementById('prompt-cards');
        const libraryEmpty = document.querySelector('.library-empty');
        
        if (library.length === 0) {
            promptCardsContainer.innerHTML = '';
            libraryEmpty.style.display = 'block';
            return;
        }
        
        // Hide empty message, show cards
        libraryEmpty.style.display = 'none';
        
        // Sort by newest first
        library.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        // Create cards
        promptCardsContainer.innerHTML = '';
        library.forEach(prompt => {
            const card = createPromptCard(prompt);
            promptCardsContainer.appendChild(card);
        });
    }
    
    function createPromptCard(prompt) {
        const card = document.createElement('div');
        card.className = 'prompt-card';
        card.dataset.id = prompt.id;
        
        const modelSpan = document.createElement('span');
        modelSpan.className = 'prompt-card-model';
        modelSpan.textContent = prompt.model || 'ChatGPT'; // Default
        
        const title = document.createElement('h3');
        title.textContent = prompt.name;
        
        const description = document.createElement('p');
        description.className = 'prompt-card-description';
        description.textContent = prompt.description || 'No description provided';
        
        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'prompt-card-tags';
        
        if (prompt.tags && prompt.tags.length) {
            prompt.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'prompt-card-tag';
                tagSpan.textContent = tag;
                tagsContainer.appendChild(tagSpan);
            });
        }
        
        const actions = document.createElement('div');
        actions.className = 'prompt-card-actions';
        
        const useBtn = document.createElement('button');
        useBtn.className = 'btn sm';
        useBtn.innerHTML = '<i class="fas fa-external-link-alt"></i> Use';
        useBtn.addEventListener('click', () => {
            // Load this prompt to the test section
            document.getElementById('test-prompt').value = prompt.prompt;
            document.getElementById('test-model').value = prompt.model || 'chatgpt';
            
            // Switch to test tab
            document.querySelector('[data-tab="test"]').click();
        });
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn sm';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(prompt.prompt)
                .then(() => showToast('Prompt copied to clipboard!'))
                .catch(err => console.error('Could not copy text: ', err));
        });
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn sm';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i> Delete';
        deleteBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to delete this prompt?')) {
                deletePrompt(prompt.id);
            }
        });
        
        actions.appendChild(useBtn);
        actions.appendChild(copyBtn);
        actions.appendChild(deleteBtn);
        
        card.appendChild(modelSpan);
        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(tagsContainer);
        card.appendChild(actions);
        
        return card;
    }
    
    function deletePrompt(id) {
        // Get library
        const library = JSON.parse(localStorage.getItem('promptLibrary') || '[]');
        
        // Filter out the prompt to delete
        const updatedLibrary = library.filter(prompt => prompt.id !== id);
        
        // Save updated library
        localStorage.setItem('promptLibrary', JSON.stringify(updatedLibrary));
        
        // Reload library display
        loadLibrary();
        
        showToast('Prompt deleted');
    }
    
    // Load library when tab is clicked
    document.querySelector('[data-tab="library"]').addEventListener('click', loadLibrary);
    
    // Library search functionality
    document.getElementById('search-btn').addEventListener('click', performSearch);
    document.getElementById('library-search').addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    function performSearch() {
        const searchTerm = document.getElementById('library-search').value.toLowerCase().trim();
        const modelFilter = document.getElementById('library-filter').value;
        
        const library = JSON.parse(localStorage.getItem('promptLibrary') || '[]');
        
        let filteredLibrary = library;
        
        // Apply model filter if not "all"
        if (modelFilter !== 'all') {
            filteredLibrary = filteredLibrary.filter(prompt => 
                (prompt.model || '').toLowerCase() === modelFilter.toLowerCase());
        }
        
        // Apply search term if any
        if (searchTerm) {
            filteredLibrary = filteredLibrary.filter(prompt => {
                const nameMatch = (prompt.name || '').toLowerCase().includes(searchTerm);
                const descMatch = (prompt.description || '').toLowerCase().includes(searchTerm);
                const tagMatch = (prompt.tags || []).some(tag => tag.toLowerCase().includes(searchTerm));
                const promptMatch = (prompt.prompt || '').toLowerCase().includes(searchTerm);
                
                return nameMatch || descMatch || tagMatch || promptMatch;
            });
        }
        
        // Display filtered results
        const promptCardsContainer = document.getElementById('prompt-cards');
        const libraryEmpty = document.querySelector('.library-empty');
        
        if (filteredLibrary.length === 0) {
            promptCardsContainer.innerHTML = '';
            libraryEmpty.style.display = 'block';
            libraryEmpty.querySelector('p').innerHTML = 
                '<i class="fas fa-search"></i> No prompts found matching your criteria';
        } else {
            libraryEmpty.style.display = 'none';
            
            // Create cards
            promptCardsContainer.innerHTML = '';
            filteredLibrary.forEach(prompt => {
                const card = createPromptCard(prompt);
                promptCardsContainer.appendChild(card);
            });
        }
    }
    
    // Test buttons in generator and optimizer tabs
    document.getElementById('test-generator').addEventListener('click', () => {
        const prompt = document.getElementById('generated-prompt').textContent;
        document.getElementById('test-prompt').value = prompt;
        document.getElementById('test-model').value = document.getElementById('target-model').value;
        document.querySelector('[data-tab="test"]').click();
    });
    
    document.getElementById('test-optimizer').addEventListener('click', () => {
        const prompt = document.getElementById('optimized-prompt').textContent;
        document.getElementById('test-prompt').value = prompt;
        document.getElementById('test-model').value = document.getElementById('opt-target-model').value;
        document.querySelector('[data-tab="test"]').click();
    });
    
    // Toast notification function
    function showToast(message) {
        // Create toast element if it doesn't exist
        let toast = document.querySelector('.toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast';
            document.body.appendChild(toast);
            
            // Add style
            const style = document.createElement('style');
            style.textContent = `
                .toast {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background-color: var(--gray-800);
                    color: white;
                    padding: 12px 24px;
                    border-radius: var(--radius);
                    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                    opacity: 0;
                    transition: opacity 0.3s, transform 0.3s;
                    transform: translateY(20px);
                    z-index: 1000;
                }
                
                .toast.show {
                    opacity: 1;
                    transform: translateY(0);
                }
            `;
            document.head.appendChild(style);
        }
        
        // Set message and show toast
        toast.textContent = message;
        toast.classList.add('show');
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
        
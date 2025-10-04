// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// State Management
const state = {
    documents: [],
    selectedDocumentId: null,
    messages: []
};

// DOM Elements - will be initialized after DOM loads
let uploadBtn, uploadModal, closeModal, uploadArea, fileInput;
let documentList, chatInput, sendBtn, chatMessages;
let uploadProgress, progressFill, uploadStatus, scrollToBottomBtn;

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing app...');
    
    // Initialize DOM elements
    uploadBtn = document.getElementById('uploadBtn');
    uploadModal = document.getElementById('uploadModal');
    closeModal = document.querySelector('.close');
    uploadArea = document.getElementById('uploadArea');
    fileInput = document.getElementById('fileInput');
    documentList = document.getElementById('documentList');
    chatInput = document.getElementById('chatInput');
    sendBtn = document.getElementById('sendBtn');
    chatMessages = document.getElementById('chatMessages');
    uploadProgress = document.getElementById('uploadProgress');
    progressFill = document.getElementById('progressFill');
    uploadStatus = document.getElementById('uploadStatus');
    scrollToBottomBtn = document.getElementById('scrollToBottom');
    
    // Verify elements exist
    console.log('Upload button found:', !!uploadBtn);
    console.log('Upload modal found:', !!uploadModal);
    
    if (!uploadBtn || !uploadModal) {
        console.error('Required elements not found!');
        return;
    }
    
    initializeEventListeners();
    loadDocuments();
});

// Event Listeners
function initializeEventListeners() {
    console.log('Setting up event listeners...');
    
    // Upload button - open modal
    uploadBtn.addEventListener('click', (e) => {
        console.log('Upload button clicked');
        e.preventDefault();
        uploadModal.classList.add('active');
    });

    // Close modal
    closeModal.addEventListener('click', () => {
        uploadModal.classList.remove('active');
        resetUploadArea();
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === uploadModal) {
            uploadModal.classList.remove('active');
            resetUploadArea();
        }
    });

    // Upload area click - trigger file input
    uploadArea.addEventListener('click', (e) => {
        console.log('Upload area clicked');
        e.stopPropagation();
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        console.log('File selected:', e.target.files[0]?.name);
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
        
        console.log('File dropped:', e.dataTransfer.files[0]?.name);
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Send message
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !chatInput.disabled) {
            sendMessage();
        }
    });
    
    // Scroll to bottom button
    if (scrollToBottomBtn) {
        chatMessages.addEventListener('scroll', () => {
            const isScrolledUp = chatMessages.scrollHeight - chatMessages.scrollTop > chatMessages.clientHeight + 100;
            if (isScrolledUp) {
                scrollToBottomBtn.classList.add('visible');
            } else {
                scrollToBottomBtn.classList.remove('visible');
            }
        });
        
        scrollToBottomBtn.addEventListener('click', () => {
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
        });
    }
    
    console.log('Event listeners initialized');
}

// Load Documents from API
async function loadDocuments() {
    console.log('Loading documents...');
    try {
        const response = await fetch(`${API_BASE_URL}/api/documents/`);
        if (!response.ok) throw new Error('Failed to load documents');
        
        const documents = await response.json();
        console.log('Documents loaded:', documents);
        state.documents = documents;
        renderDocumentList();
        
        // Enable chat if we have documents
        if (documents.length > 0) {
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatInput.placeholder = 'Ask a question about your documents...';
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        showError('Failed to load documents. Make sure the backend server is running on port 8000.');
    }
}

// Render Document List
function renderDocumentList() {
    if (state.documents.length === 0) {
        documentList.innerHTML = '<p class="empty-state">No documents uploaded yet</p>';
        return;
    }

    documentList.innerHTML = state.documents.map(doc => `
        <div class="document-item ${doc.id === state.selectedDocumentId ? 'active' : ''}" 
             onclick="selectDocument(${doc.id})">
            <div class="document-name">${escapeHtml(doc.filename)}</div>
            <div class="document-meta">
                ${formatFileSize(doc.file_size)} • ${doc.chunk_count || 0} chunks
                ${doc.status === 'error' ? ' • ⚠️ Error' : ''}
            </div>
        </div>
    `).join('');
}

// Select Document
function selectDocument(documentId) {
    console.log('Document selected:', documentId);
    state.selectedDocumentId = documentId;
    renderDocumentList();
}

// Handle File Upload
async function handleFileUpload(file) {
    console.log('Handling file upload:', file.name);
    
    // Validate file
    const validTypes = ['.pdf', '.docx', '.txt'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(fileExt)) {
        showError(`Invalid file type. Please upload ${validTypes.join(', ')} files.`);
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError('File too large. Maximum size is 10MB.');
        return;
    }

    // Show progress
    uploadProgress.style.display = 'block';
    uploadArea.style.display = 'none';
    progressFill.style.width = '0%';
    uploadStatus.textContent = 'Uploading...';

    try {
        const formData = new FormData();
        formData.append('file', file);

        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            if (progress <= 90) {
                progressFill.style.width = progress + '%';
            }
        }, 200);

        console.log('Sending file to API...');
        const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const result = await response.json();
        console.log('Upload successful:', result);
        
        // Complete progress
        progressFill.style.width = '100%';
        uploadStatus.textContent = 'Processing complete!';

        // Wait a moment then close
        setTimeout(() => {
            uploadModal.classList.remove('active');
            resetUploadArea();
            loadDocuments();
            showSuccess(`Document "${file.name}" uploaded successfully!`);
        }, 1000);

    } catch (error) {
        console.error('Upload error:', error);
        uploadStatus.textContent = 'Upload failed: ' + error.message;
        
        setTimeout(() => {
            resetUploadArea();
        }, 3000);
    }
}

// Reset Upload Area
function resetUploadArea() {
    uploadProgress.style.display = 'none';
    uploadArea.style.display = 'block';
    fileInput.value = '';
    progressFill.style.width = '0%';
}

// Send Message
async function sendMessage() {
    const question = chatInput.value.trim();
    if (!question) return;

    console.log('Sending message:', question);

    // Disable input while processing
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message to chat
    addMessage('user', question);
    chatInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/api/chat/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                document_id: state.selectedDocumentId,
                n_results: 5
            })
        });

        removeTypingIndicator(typingId);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get answer');
        }

        const result = await response.json();
        console.log('Chat response:', result);
        
        // Add assistant message with sources
        addMessage('assistant', result.answer, result.sources);

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator(typingId);
        addMessage('assistant', `Error: ${error.message}`);
    } finally {
        // Re-enable input
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

// Add Message to Chat
function addMessage(role, content, sources = null) {
    // Remove welcome message if it exists
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="sources">
                <div class="sources-title">📚 Sources</div>
                ${sources.map(source => `
                    <div class="source-item">
                        <div class="source-meta">Document ${source.document_id} • Similarity: ${(source.similarity * 100).toFixed(0)}%</div>
                        <div class="source-text">${escapeHtml(source.text)}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    messageDiv.innerHTML = `
        <div class="message-label">${role === 'user' ? 'You' : 'Assistant'}</div>
        <div class="message-content">
            ${escapeHtml(content)}
            ${sourcesHtml}
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add Typing Indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant typing-indicator';
    typingDiv.id = 'typing-' + Date.now();
    typingDiv.innerHTML = `
        <div class="message-label">Assistant</div>
        <div class="message-content">Thinking...</div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv.id;
}

// Remove Typing Indicator
function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Scroll to Bottom
function scrollToBottom() {
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showError(message) {
    console.error(message);
    alert('Error: ' + message);
}

function showSuccess(message) {
    console.log(message);
    alert('Success: ' + message);
}

// Make selectDocument available globally for onclick
window.selectDocument = selectDocument;
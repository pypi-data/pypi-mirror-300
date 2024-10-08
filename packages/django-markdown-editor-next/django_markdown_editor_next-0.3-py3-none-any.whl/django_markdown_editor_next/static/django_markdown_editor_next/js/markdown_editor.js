document.addEventListener('DOMContentLoaded', function() {
    const editors = document.querySelectorAll('.markdown-editor');
    
    editors.forEach(editor => {
        const toolbar = createToolbar(editor.dataset.customToolbar);
        const previewPane = createPreviewPane();
        editor.parentNode.insertBefore(toolbar, editor);
        editor.parentNode.insertBefore(previewPane, editor.nextSibling);
        
        setupToolbarFunctionality(toolbar, editor, previewPane);
        setupKeyboardShortcuts(editor);
        setupRealTimePreview(editor, previewPane);
    });
});

function createToolbar(customToolbarString) {
    const defaultButtons = [
        {action: 'undo', icon: 'fas fa-undo', title: 'Undo'},
        {action: 'redo', icon: 'fas fa-redo', title: 'Redo'},
        {action: 'bold', icon: 'fas fa-bold', title: 'Bold'},
        {action: 'italic', icon: 'fas fa-italic', title: 'Italic'},
        {action: 'strikethrough', icon: 'fas fa-strikethrough', title: 'Strikethrough'},
        {action: 'code', icon: 'fas fa-code', title: 'Inline Code'},
        {action: 'ul', icon: 'fas fa-list-ul', title: 'Unordered List'},
        {action: 'ol', icon: 'fas fa-list-ol', title: 'Ordered List'},
        {action: 'quote', icon: 'fas fa-quote-right', title: 'Quote'},
        {action: 'code-block', icon: 'fas fa-file-code', title: 'Code Block'},
        {action: 'link', icon: 'fas fa-link', title: 'Link'},
        {action: 'image', icon: 'fas fa-image', title: 'Image'},
        {action: 'upload-image', icon: 'fas fa-upload', title: 'Upload Image'},
        {action: 'preview', icon: 'fas fa-eye', title: 'Toggle Preview'}
    ];

    const customButtons = customToolbarString ? JSON.parse(customToolbarString) : defaultButtons;

    const toolbar = document.createElement('div');
    toolbar.className = 'markdown-editor-toolbar';
    
    customButtons.forEach(button => {
        const btnElement = document.createElement('button');
        btnElement.type = 'button';
        btnElement.dataset.action = button.action;
        btnElement.title = button.title;
        btnElement.innerHTML = `<i class="${button.icon}"></i>`;
        toolbar.appendChild(btnElement);
    });

    return toolbar;
}

function createPreviewPane() {
    const previewPane = document.createElement('div');
    previewPane.className = 'markdown-preview';
    previewPane.style.display = 'none';
    return previewPane;
}

function setupToolbarFunctionality(toolbar, editor, previewPane) {
    toolbar.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON' || e.target.parentElement.tagName === 'BUTTON') {
            const button = e.target.tagName === 'BUTTON' ? e.target : e.target.parentElement;
            const action = button.getAttribute('data-action');
            handleAction(action, editor, previewPane);
        }
    });
}

function handleAction(action, editor, previewPane) {
    const actions = {
        // ... (previous actions)
        'upload-image': () => uploadImage(editor),
        'preview': () => togglePreview(editor, previewPane)
    };

    if (actions[action]) {
        actions[action]();
        editor.focus();
    }
}

function uploadImage(editor) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async function() {
        const file = input.files[0];
        if (file) {
            try {
                const formData = new FormData();
                formData.append('image', file);
                const response = await fetch('/markdown-editor/upload-image/', {
                    method: 'POST',
                    body: formData,
                });
                if (response.ok) {
                    const data = await response.json();
                    const imageMarkdown = `![${file.name}](${data.url})`;
                    editor.setRangeText(imageMarkdown, editor.selectionStart, editor.selectionEnd, 'select');
                } else {
                    alert('Image upload failed. Please try again.');
                }
            } catch (error) {
                console.error('Error uploading image:', error);
                alert('An error occurred while uploading the image.');
            }
        }
    };
    input.click();
}

function togglePreview(editor, previewPane) {
    if (previewPane.style.display === 'none') {
        previewPane.innerHTML = marked(editor.value);
        previewPane.style.display = 'block';
        editor.style.display = 'none';
    } else {
        previewPane.style.display = 'none';
        editor.style.display = 'block';
    }
}

function setupKeyboardShortcuts(editor) {
    editor.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'b':
                    e.preventDefault();
                    wrapText(editor, '**', '**');
                    break;
                case 'i':
                    e.preventDefault();
                    wrapText(editor, '_', '_');
                    break;
                case 'k':
                    e.preventDefault();
                    insertLink(editor);
                    break;
                // Add more shortcuts as needed
            }
        }
    });
}

function setupRealTimePreview(editor, previewPane) {
    let timeout;
    editor.addEventListener('input', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            if (previewPane.style.display !== 'none') {
                previewPane.innerHTML = marked(editor.value);
            }
        }, 300);
    });
}
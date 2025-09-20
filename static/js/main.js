// =================================================================
// static/js/main.js
// -----------------------------------------------------------------
// KEEPS THE SYSTEM INTEGRATED: This file is updated with crucial
// JavaScript logic to manage modal interactions for the SPA-like
// user management page, ensuring a smooth and professional UX.
// =================================================================

document.addEventListener("DOMContentLoaded", function() {
    // --- Sidebar toggle functionality ---
    const sidebarToggle = document.body.querySelector("#sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", event => {
            event.preventDefault();
            document.body.classList.toggle("sb-sidenav-toggled");
        });
    }

    // --- HTMX Toast Notification Listener ---
    const toastElement = document.getElementById('appToast');
    if (toastElement) {
        const appToast = new bootstrap.Toast(toastElement);
        document.body.addEventListener('showToast', function(event) {
            toastElement.querySelector('.toast-body').textContent = event.detail.message;
            appToast.show();
        });
    }
    
    // --- Logic for User Management Modals ---
    const userFormModalEl = document.getElementById('user-form-modal');
    if (userFormModalEl) {
        const userFormModal = new bootstrap.Modal(userFormModalEl);
        
        // When an HTMX request successfully completes (e.g., user saved),
        // hide the modal and trigger a toast.
        document.body.addEventListener('htmx:afterRequest', function(event) {
            if (event.detail.target.id === 'modal-content' && !event.detail.failed) {
                 // Check if the response is empty, which indicates success
                if (event.detail.xhr.responseText === "") {
                    userFormModal.hide();
                    const toastEvent = new CustomEvent('showToast', { detail: { message: 'User saved successfully!' } });
                    document.body.dispatchEvent(toastEvent);
                }
            }
        });
    }

    const deleteConfirmModalEl = document.getElementById('delete-confirm-modal');
    if (deleteConfirmModalEl) {
        // When the delete confirmation modal is shown, set the correct hx-post URL
        // on its form from the button that triggered it.
        deleteConfirmModalEl.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const deleteUrl = button.getAttribute('data-delete-url');
            const deleteForm = document.getElementById('delete-user-form');
            deleteForm.setAttribute('hx-post', deleteUrl);
        });
        
        // After a successful deletion, trigger a toast.
        const deleteForm = document.getElementById('delete-user-form');
        deleteForm.addEventListener('htmx:afterRequest', function(event) {
             if (!event.detail.failed) {
                const toastEvent = new CustomEvent('showToast', { detail: { message: 'User has been deleted.' } });
                document.body.dispatchEvent(toastEvent);
             }
        });
    }
});
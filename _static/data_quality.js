// Save users browser data
const browser = navigator.userAgent;

function saveBrowserData() {
    const browserField = document.getElementById('id_browser');
    if (browserField) {
        browserField.value = browser;
    }
}

// Blur data
function pageKey(n = 3) {
    const segments = window.location.pathname.split('/').filter(s => s);
    // e.g. ["p","4rwl1qr0","Introduction","Demographics","2"]
    return segments.slice(-n).join('/');
}

let blurDict = {};

document.addEventListener('DOMContentLoaded', () => {
    saveBrowserData();

    const stored = localStorage.getItem('dictionary');
    blurDict = stored ? JSON.parse(stored) : {};
    // ensure at least an empty object
    localStorage.setItem('dictionary', JSON.stringify(blurDict));
});

document.addEventListener('DOMContentLoaded', function() {
    const key = pageKey(3);  // e.g. "Introduction/Demographics/2"

    let blur_data = localStorage.getItem('dictionary'); // retrieve
    let myDictionary = blur_data ? JSON.parse(blur_data) : null; // parse

    if (!myDictionary) {
        // If it doesn't exist, create and save it
        myDictionary = {
            page: 0,
        };
        localStorage.setItem('dictionary', JSON.stringify(myDictionary));
    }
});

// Event listener for blur event
let warned = false;
const threshold = 1; // Number of blurs before the user is warned
let count = 0;

window.addEventListener('blur', function() {
    const warnedField = document.getElementById('id_blur_warned');
    if (warnedField && warnedField.value === '1') {
        warned = true;
    }

    count++;

    let blur_data = localStorage.getItem('dictionary'); // retrieve
    let myDictionary = blur_data ? JSON.parse(blur_data) : {};

    // Check if the 'page' key exists in the dictionary
    const key = pageKey(3);  // "Introduction/Demographics/2"
    if (key in myDictionary) {
        myDictionary[key]++;
    } else {
        myDictionary[key] = 1;
    }

    // Save the updated dictionary back to localStorage
    localStorage.setItem('dictionary', JSON.stringify(myDictionary));

    // Update hidden fields
    const logField = document.getElementById('id_blur_log');
    const countField = document.getElementById('id_blur_count');
    if (logField) logField.value = JSON.stringify(myDictionary);
    if (countField) countField.value = count;

    if (!warned && count >= threshold) {
        warned = true;
        if (warnedField) warnedField.value = '1';

        alert(
          "We noticed you switched tabs or windows. Please stay on our experiment page " +
          "to ensure your data is recorded correctly. If you switch tabs or windows again, we may have to reject your submission."
        );
    }
});

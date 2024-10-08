"use strict";
(self["webpackChunkcollabnotes"] = self["webpackChunkcollabnotes"] || []).push([["lib_index_js"],{

/***/ "./lib/api.js":
/*!********************!*\
  !*** ./lib/api.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   fetchData: () => (/* binding */ fetchData)
/* harmony export */ });
/**
 * Fetches data from a given URL.
 *
 * @param url The URL to fetch data from.
 * @returns A promise that resolves to the fetched data.
 */
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json(); // Assuming the server responds with JSON
        return data;
    }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return {};
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _style_collabnotes_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/collabnotes.css */ "./style/collabnotes.css");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");
/* harmony import */ var _ui__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ui */ "./lib/ui.js");
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api */ "./lib/api.js");
/* harmony import */ var _notes__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./notes */ "./lib/notes.js");







 // Import the setters from notes.ts
/**
 * Initialization data for the collabnotes extension.
 */
const plugin = {
    id: 'collabnotes:plugin',
    description: 'A JupyterLab extension to enable collaborative note taking.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: (app, notebooks, settingsRegistry) => {
        console.log('JupyterLab extension collabnotes is activated! xx');
        app.restored.then(() => {
            (0,_settings__WEBPACK_IMPORTED_MODULE_3__.checkSettings)(settingsRegistry);
            (0,_notes__WEBPACK_IMPORTED_MODULE_4__.ensureSettingsInitialized)(settingsRegistry);
            if (notebooks.currentWidget) {
                addNotesButtons(settingsRegistry, notebooks.currentWidget);
            }
            notebooks.currentChanged.connect((sender, panel) => {
                if (panel) {
                    addNotesButtons(settingsRegistry, panel);
                }
            });
        });
    }
};
async function addNotesButtons(settingsRegistry, panel) {
    var _a;
    const url = await (0,_settings__WEBPACK_IMPORTED_MODULE_3__.getSetting)('URL', settingsRegistry);
    const ac = await (0,_settings__WEBPACK_IMPORTED_MODULE_3__.getSetting)('AccessCode', settingsRegistry);
    const pi = await (0,_settings__WEBPACK_IMPORTED_MODULE_3__.getSetting)('PI', settingsRegistry);
    const nick = await (0,_settings__WEBPACK_IMPORTED_MODULE_3__.getSetting)('NickName', settingsRegistry);
    const fn = panel.context.path.split('/').pop(); // Assert that pop() will not return undefined // Get only the filename from the path
    console.log(fn);
    // Set the filename, URL, Nickname, and panel in the notes module so they can be accessed globally
    (0,_notes__WEBPACK_IMPORTED_MODULE_4__.setFilename)(fn);
    (0,_notes__WEBPACK_IMPORTED_MODULE_4__.setURL)(url);
    (0,_notes__WEBPACK_IMPORTED_MODULE_4__.setNickname)(nick);
    (0,_notes__WEBPACK_IMPORTED_MODULE_4__.setPanel)(panel);
    const ts = Date.now();
    const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&do=list`;
    const data = await (0,_api__WEBPACK_IMPORTED_MODULE_5__.fetchData)(qs);
    (_a = panel.content.widgets) === null || _a === void 0 ? void 0 : _a.forEach(cell => {
        if (cell.model.getMetadata('CID') !== undefined) {
            const cid = cell.model.getMetadata('CID');
            const newold = data[cid];
            if (newold !== undefined) {
                const newcomments = String(newold['new']);
                const totalcomments = String(newold['new'] + newold['old']);
                const noteSquare = (0,_ui__WEBPACK_IMPORTED_MODULE_6__.createNoteSquare)(newcomments, totalcomments, cid);
                noteSquare.onclick = () => (0,_ui__WEBPACK_IMPORTED_MODULE_6__.handleNoteSquareClick)(url, ac, pi, fn, ts, nick, cid, panel);
                cell.node.appendChild(noteSquare);
            }
            else {
                console.log('Unallowed cell: ' + cid);
            }
        }
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/notes.js":
/*!**********************!*\
  !*** ./lib/notes.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addEventListenersToReplyButtons: () => (/* binding */ addEventListenersToReplyButtons),
/* harmony export */   createNestedNotes: () => (/* binding */ createNestedNotes),
/* harmony export */   ensureSettingsInitialized: () => (/* binding */ ensureSettingsInitialized),
/* harmony export */   getAC: () => (/* binding */ getAC),
/* harmony export */   getFilename: () => (/* binding */ getFilename),
/* harmony export */   getNickname: () => (/* binding */ getNickname),
/* harmony export */   getPI: () => (/* binding */ getPI),
/* harmony export */   getPanel: () => (/* binding */ getPanel),
/* harmony export */   getURL: () => (/* binding */ getURL),
/* harmony export */   renderNotes: () => (/* binding */ renderNotes),
/* harmony export */   setFilename: () => (/* binding */ setFilename),
/* harmony export */   setNickname: () => (/* binding */ setNickname),
/* harmony export */   setPanel: () => (/* binding */ setPanel),
/* harmony export */   setURL: () => (/* binding */ setURL)
/* harmony export */ });
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./settings */ "./lib/settings.js");
/* harmony import */ var _ui__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ui */ "./lib/ui.js");
 // Import the getSetting function from settings.ts

/**
 * Function to render notes recursively.
 */
function renderNotes(note, level = 0) {
    const addedDate = new Date(note.added);
    const ukDate = `${addedDate.getDate().toString().padStart(2, '0')}/${(addedDate.getMonth() + 1).toString().padStart(2, '0')}/${addedDate.getFullYear()} ${addedDate.getHours().toString().padStart(2, '0')}:${addedDate.getMinutes().toString().padStart(2, '0')}:${addedDate.getSeconds().toString().padStart(2, '0')}`;
    // Update the regex to include optional http/https at the beginning
    const urlRegex = /((https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+)(\.(co\.|com|org|net|gov|edu|io|us|it|uk|ca|de|fr|ru|jp|cn|info|biz|me|tv|dev|xyz|site|club|online|app|shop|blog|tech|art|news|live|store|ai|design|space|world|academy|digital|systems|solutions|pro|today|name|cloud|zone|press|network|fun|games|studio|group|global|life|love|media|ventures|partners|capital|finance|insurance|services|events|city|fund|energy|expert|care|team|express|consulting|restaurant|coffee|hospital|education|software|tools|university|security|partners|agency|ac\.uk|be))([^\s]*))/gi;
    // Replace detected URLs with anchor tags, ensuring http/https is included in display
    const parsedNoteContent = note.note.replace(urlRegex, (match) => {
        let url = match;
        let displayText = match;
        // If the URL does not start with http/https, prepend "http://"
        if (!/^https?:\/\//i.test(url)) {
            url = `http://${url}`;
            displayText = `http://${displayText}`;
        }
        return `<a href="${url}" class="links-in-forms" target="_blank">${displayText}</a>`;
    });
    let noteHtml = `<div class="note" style="margin-left: ${level * 20}px;">`;
    if (note.stub !== 1) {
        noteHtml += `
      <div class="replies">
        <div class="metadata-reply">
          <span class="user">${note.NickName}</span>
          <span class="date">(Added: ${ukDate})</span>
        </div>
        <p class="message">${parsedNoteContent}</p>
        <strong><button class="reply-button" data-note-id="${note.noteID}">Reply</button></strong>
      </div>
    `;
    }
    else {
        noteHtml += `
      <form class="note-form">
        <textarea class="note-textarea" placeholder="Write your note here..."></textarea>
        <div class="buttons">
          <button type="button" class="create-note-button" data-note-id="${note.noteID}">Save</button>
        </div>
      </form>
    `;
    }
    noteHtml += '</div>';
    // Recursively render replies
    note.replies.forEach((reply) => {
        noteHtml += renderNotes(reply, level + 1);
    });
    return noteHtml;
}
/**
 * Add event listeners to reply buttons.
 */
function addEventListenersToReplyButtons() {
    document.querySelectorAll('.reply-button').forEach(button => {
        button.removeEventListener('click', handleReplyButtonClick);
        button.addEventListener('click', handleReplyButtonClick);
    });
    document.querySelectorAll('.create-note-button').forEach(button => {
        button.removeEventListener('click', handleCreateNoteButtonClick);
        button.addEventListener('click', handleCreateNoteButtonClick);
    });
}
/**
 * Handle reply button click event.
 */
function handleReplyButtonClick(event) {
    const noteID = event.target.getAttribute('data-note-id');
    console.log('reply to ' + noteID);
    const noteElement = event.target.closest('.note');
    if (!noteElement) {
        return;
    }
    ;
    const existingForm = noteElement.querySelector('.reply-form');
    if (existingForm) {
        existingForm.remove();
    }
    const form = document.createElement('form');
    form.className = 'reply-form';
    const textarea = document.createElement('textarea');
    textarea.placeholder = 'Enter your reply';
    textarea.className = 'reply-form-textarea';
    form.appendChild(textarea);
    const buttons = document.createElement('div');
    buttons.className = 'reply-buttons';
    form.appendChild(buttons);
    const submitButton = document.createElement('button');
    submitButton.type = 'button';
    submitButton.textContent = 'Submit';
    submitButton.className = 'reply-form-button';
    submitButton.onclick = (e) => {
        handleSubmitReplyButtonClick(e);
        form.remove();
    };
    buttons.appendChild(submitButton);
    submitButton.setAttribute('data-note-id', String(noteID));
    const cancelButton = document.createElement('button');
    cancelButton.type = 'button';
    cancelButton.textContent = 'Cancel';
    cancelButton.classList.add('reply-form-button');
    cancelButton.classList.add('cancel-form-button');
    cancelButton.onclick = (e) => {
        e.stopPropagation();
        form.remove();
    };
    buttons.appendChild(cancelButton);
    noteElement.appendChild(form);
}
async function handleSubmitReplyButtonClick(event) {
    const button = event.target;
    const noteID = button.getAttribute('data-note-id');
    const form = button.closest('.reply-form');
    if (!form) {
        console.error('Form not found for note ID:', noteID);
        return;
    }
    // Get the content of the note
    const textarea = form.querySelector('textarea');
    const noteContent = textarea === null || textarea === void 0 ? void 0 : textarea.value.trim();
    const displayDiv = document.getElementById('displayDiv');
    if (!noteContent) {
        alert('Please enter a note before saving.');
        return;
    }
    // Define constants similar to the second request
    const pi = getPI(); // Replace with actual logic to get PI
    const ac = getAC(); // Replace with actual logic to get Access Code
    const fn = getFilename(); // Replace with actual logic to get filename
    const cid = displayDiv === null || displayDiv === void 0 ? void 0 : displayDiv.getAttribute('data-cid'); // Hard-coded as in the second request
    const rid = noteID; // Reply ID, as in the second request
    const ts = Date.now();
    // Prepare the data for the POST request using URLSearchParams for x-www-form-urlencoded
    const postData = new URLSearchParams({
        do: 'addnote',
        pi: pi,
        ac: ac,
        fn: fn,
        cid: String(cid),
        rid: String(rid),
        content: noteContent, // Replace noteContent with 'test' as per the second request
    });
    try {
        // Send the POST request
        const response = await fetch('https://ictsoeasy.co.uk/collabnotes/index.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Specify the correct content type
            },
            body: postData.toString(), // Send the data as x-www-form-urlencoded
        });
        if (response.ok) {
            textarea.value = '';
            const newID = await response.text(); // Wait for the Promise to resolve
            const panel = getPanel();
            if (panel) {
                await (0,_ui__WEBPACK_IMPORTED_MODULE_0__.updateUI)(getURL(), ac, pi, fn, ts, getNickname(), Number(cid), panel);
                // scroll to the reply button that added the new message
                const lastMessage = document.querySelector(`button[data-note-id="${newID}"]`);
                const parentDiv = lastMessage.closest('div');
                parentDiv.scrollIntoView({ behavior: 'smooth' });
            }
            else {
                console.error('Panel is null, cannot update UI.');
                // Handle the null case appropriately (e.g., show an error or fallback UI)
            }
        }
        else {
            throw new Error('Failed to save note');
        }
    }
    catch (error) {
        console.error('Error saving note:', error);
        alert('An error occurred while saving the note. Please try again.');
    }
}
/**
 * Handle create note button click event.
 */
async function handleCreateNoteButtonClick(event) {
    const button = event.target;
    const noteID = button.getAttribute('data-note-id');
    const form = button.closest('.note-form');
    if (!form) {
        console.error('Form not found for note ID:', noteID);
        return;
    }
    // Get the content of the note
    const textarea = form.querySelector('.note-textarea');
    const noteContent = textarea === null || textarea === void 0 ? void 0 : textarea.value.trim();
    const displayDiv = document.getElementById('displayDiv');
    if (!noteContent) {
        alert('Please enter a note before saving.');
        return;
    }
    // Define constants similar to the second request
    const pi = getPI(); // Replace with actual logic to get PI
    const ac = getAC(); // Replace with actual logic to get Access Code
    const fn = getFilename(); // Replace with actual logic to get filename
    const cid = displayDiv === null || displayDiv === void 0 ? void 0 : displayDiv.getAttribute('data-cid'); // Hard-coded as in the second request
    const rid = noteID; // Reply ID, as in the second request
    const ts = Date.now();
    // Prepare the data for the POST request using URLSearchParams for x-www-form-urlencoded
    const postData = new URLSearchParams({
        do: 'addnote',
        pi: pi,
        ac: ac,
        fn: fn,
        cid: String(cid),
        rid: String(rid),
        content: noteContent, // Replace noteContent with 'test' as per the second request
    });
    try {
        // Send the POST request
        const response = await fetch('https://ictsoeasy.co.uk/collabnotes/index.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Specify the correct content type
            },
            body: postData.toString(), // Send the data as x-www-form-urlencoded
        });
        if (response.ok) {
            textarea.value = '';
            const panel = getPanel();
            if (panel) {
                await (0,_ui__WEBPACK_IMPORTED_MODULE_0__.updateUI)(getURL(), ac, pi, fn, ts, getNickname(), Number(cid), panel);
                // scroll to new message
                const displayDiv = document.querySelector('#displayDiv');
                if (displayDiv) {
                    displayDiv.scroll({
                        top: displayDiv.scrollHeight,
                        behavior: 'smooth'
                    });
                }
            }
            else {
                console.error('Panel is null, cannot update UI.');
                // Handle the null case appropriately (e.g., show an error or fallback UI)
            }
        }
        else {
            throw new Error('Failed to save note');
        }
    }
    catch (error) {
        console.error('Error saving note:', error);
        alert('An error occurred while saving the note. Please try again.');
    }
}
/**
 * Function to create a nested structure for the notes.
 */
function createNestedNotes(notes) {
    const notesMap = {};
    notes.forEach((note) => {
        notesMap[note.noteID] = { ...note, replies: [] };
    });
    let rootNote = null;
    notes.forEach((note) => {
        if (note.replyID === null) {
            rootNote = notesMap[note.noteID];
        }
        else {
            notesMap[note.replyID].replies.push(notesMap[note.noteID]);
        }
    });
    let finalHtml = '';
    if (rootNote) {
        finalHtml = renderNotes(rootNote);
    }
    return finalHtml;
}
// Create a cache object to store PI and AccessCode values.
let piCache = null;
let acCache = null;
/**
 * Initialize and cache the PI and AccessCode settings.
 * This function is only called once when the module is loaded.
 */
async function initializeSettings(settingsRegistry) {
    try {
        piCache = await (0,_settings__WEBPACK_IMPORTED_MODULE_1__.getSetting)('PI', settingsRegistry);
        acCache = await (0,_settings__WEBPACK_IMPORTED_MODULE_1__.getSetting)('AccessCode', settingsRegistry);
    }
    catch (error) {
        console.error('Error initializing settings:', error);
        piCache = '';
        acCache = '';
    }
}
/**
 * Retrieve the cached PI value.
 */
function getPI() {
    if (piCache === null) {
        console.warn('PI is not initialized yet.');
        return '';
    }
    return piCache;
}
/**
 * Retrieve the cached AccessCode value.
 */
function getAC() {
    if (acCache === null) {
        console.warn('AccessCode is not initialized yet.');
        return '';
    }
    return acCache;
}
/**
 * Ensure the settings are initialized only once.
 * This should be called when the module is loaded or in the plugin's activation function.
 */
async function ensureSettingsInitialized(settingsRegistry) {
    if (piCache === null || acCache === null) {
        await initializeSettings(settingsRegistry);
    }
}
// Create a variable to store the current notebook's filename (fn)
let fnCache = null;
/**
 * Set the filename (fn) in the cache.
 * This should be called whenever the notebook is changed or opened.
 */
function setFilename(fn) {
    fnCache = fn;
}
/**
 * Get the cached filename (fn).
 */
function getFilename() {
    if (fnCache === null) {
        console.warn('Filename (fn) is not initialized yet.');
        return '';
    }
    return fnCache;
}
// Cache variables for URL, Nickname, and Notebook Panel
let urlCache = null;
let nickCache = null;
let panelCache = null;
/**
 * Set the URL in the cache.
 */
function setURL(url) {
    urlCache = url;
}
/**
 * Get the cached URL.
 */
function getURL() {
    if (urlCache === null) {
        console.warn('URL is not initialized yet.');
        return '';
    }
    return urlCache;
}
/**
 * Set the Nickname in the cache.
 */
function setNickname(nick) {
    nickCache = nick;
}
/**
 * Get the cached Nickname.
 */
function getNickname() {
    if (nickCache === null) {
        console.warn('Nickname is not initialized yet.');
        return '';
    }
    return nickCache;
}
/**
 * Set the NotebookPanel in the cache.
 */
function setPanel(panel) {
    panelCache = panel;
}
/**
 * Get the cached NotebookPanel.
 */
function getPanel() {
    if (panelCache === null) {
        console.warn('Panel is not initialized yet.');
        return null;
    }
    return panelCache;
}


/***/ }),

/***/ "./lib/settings.js":
/*!*************************!*\
  !*** ./lib/settings.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   checkSettings: () => (/* binding */ checkSettings),
/* harmony export */   getSetting: () => (/* binding */ getSetting)
/* harmony export */ });
/**
 * Check an individual setting has been set.
 */
async function checkSetting(setting, settings) {
    let s = settings.get(setting).composite;
    if (s === '' || s === undefined) {
        s = prompt("Enter setting for '" + setting + "': ");
        if (s === null) {
            s = '';
        }
        if (s === '') {
            alert('You must enter a setting for ' + setting + ' for collabnotes to work. You will be prompted every time you open a notebook.');
        }
        else {
            await settings.set(setting, s);
        }
    }
}
/**
 * Check all settings have been set.
 */
async function checkSettings(settingsRegistry) {
    try {
        const settings = await settingsRegistry.load('collabnotes:settings');
        await checkSetting('PI', settings);
        await checkSetting('NickName', settings);
        await checkSetting('AccessCode', settings);
        await checkSetting('URL', settings);
    }
    catch (error) {
        console.error('Error getting settings:', error);
    }
}
/**
 * Retrieve an individual setting.
 */
async function getSetting(setting, settingsRegistry) {
    try {
        const settings = await settingsRegistry.load('collabnotes:settings');
        const s = settings.get(setting).composite;
        if (s === '' || s === undefined || s === null) {
            return '';
        }
        else {
            return s;
        }
    }
    catch (error) {
        console.error('Error getting setting ' + setting + ':', error);
        return '';
    }
}


/***/ }),

/***/ "./lib/ui.js":
/*!*******************!*\
  !*** ./lib/ui.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createNoteSquare: () => (/* binding */ createNoteSquare),
/* harmony export */   handleNoteSquareClick: () => (/* binding */ handleNoteSquareClick),
/* harmony export */   updateUI: () => (/* binding */ updateUI)
/* harmony export */ });
/* harmony import */ var _notes__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./notes */ "./lib/notes.js");
/* harmony import */ var _api__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./api */ "./lib/api.js");


/**
 * Create a note square element.
 */
function createNoteSquare(newComments, totalComments, cid) {
    const noteSquare = document.createElement('div');
    noteSquare.id = `collabnotes_${cid}`;
    noteSquare.classList.add('square');
    const newCommentsNum = Number(newComments);
    const totalCommentsNum = Number(totalComments);
    if (newCommentsNum > 0) {
        // There are unread messages - red
        noteSquare.style.backgroundColor = '#c10031';
    }
    else if (totalCommentsNum === 0) {
        // There are 0 messages - blue
        noteSquare.style.backgroundColor = '#00b0ac';
    }
    else {
        // Messages are already read - green
        noteSquare.style.backgroundColor = '#a4a400';
    }
    noteSquare.textContent = totalComments;
    return noteSquare;
}
/**
 * Create a display div element.
 */
function createDisplayDiv(cid) {
    const displayDiv = document.createElement('div');
    displayDiv.id = 'displayDiv';
    console.log(cid);
    displayDiv === null || displayDiv === void 0 ? void 0 : displayDiv.setAttribute('data-cid', cid);
    return displayDiv;
}
/**
 * Handle note square click event.
 */
async function handleNoteSquareClick(url, ac, pi, fn, ts, nick, cid, panel) {
    const existingDisplayDiv = document.getElementById('displayDiv');
    if (existingDisplayDiv) {
        existingDisplayDiv.remove();
        return;
    }
    // update color of note counter
    const noteCounter = document.getElementById(`collabnotes_${cid}`);
    if (noteCounter !== null && noteCounter !== undefined) {
        if (parseInt(noteCounter.innerText) > 0) {
            noteCounter.style.backgroundColor = '#a4a400';
        }
        console.log('yo');
    }
    console.log('yo222');
    const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&cid=${cid}&do=getnotes`;
    const notes = await (0,_api__WEBPACK_IMPORTED_MODULE_0__.fetchData)(qs);
    const displayDiv = createDisplayDiv(String(cid));
    const nestedNotes = (0,_notes__WEBPACK_IMPORTED_MODULE_1__.createNestedNotes)(notes);
    displayDiv.innerHTML = nestedNotes;
    panel.node.appendChild(displayDiv);
    (0,_notes__WEBPACK_IMPORTED_MODULE_1__.addEventListenersToReplyButtons)();
    document.addEventListener('click', handleClickOutside);
}
/**
 * Handle click outside of display div to remove it.
 */
function handleClickOutside(event) {
    const displayDiv = document.getElementById('displayDiv');
    if (!displayDiv) {
        document.removeEventListener('click', handleClickOutside);
        return;
    }
    const target = event.target;
    if (!displayDiv.contains(target)) {
        displayDiv.remove();
        document.removeEventListener('click', handleClickOutside);
    }
}
/**
 * Update ui.
 */
async function updateUI(url, ac, pi, fn, ts, nick, cid, panel) {
    // update the displayDiv
    const existingDisplayDiv = document.getElementById('displayDiv');
    if (existingDisplayDiv) {
        existingDisplayDiv.remove();
    }
    const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&cid=${cid}&do=getnotes`;
    const notes = await (0,_api__WEBPACK_IMPORTED_MODULE_0__.fetchData)(qs);
    const displayDiv = createDisplayDiv(String(cid));
    const nestedNotes = (0,_notes__WEBPACK_IMPORTED_MODULE_1__.createNestedNotes)(notes);
    displayDiv.innerHTML = nestedNotes;
    panel.node.appendChild(displayDiv);
    (0,_notes__WEBPACK_IMPORTED_MODULE_1__.addEventListenersToReplyButtons)();
    document.addEventListener('click', handleClickOutside);
    // update the note counter button
    const noteCounter = document.getElementById(`collabnotes_${cid}`);
    const qs2 = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&do=list`;
    const data = await (0,_api__WEBPACK_IMPORTED_MODULE_0__.fetchData)(qs2);
    if (noteCounter !== null && noteCounter !== undefined) {
        // Safe to use noteCounter
        noteCounter.innerText = data[cid].new;
        noteCounter.style.backgroundColor = '#a4a400';
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/collabnotes.css":
/*!*********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/collabnotes.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.noNotes {
  background-color: #86bffc;
}

/* Add this to your stylesheet */
.divWithTriangle {
  position: relative;
}

.divWithTriangle::after {
  content: 'Notes';
  width: 0;
  height: 0;
  position: absolute;
  top: 0;
  right: 0;
  border-left: 20px solid transparent;
  border-bottom: 20px solid transparent;
  border-top: 20px solid yellow;
  /* Adjust the color and size as needed */
}

.square {
  position: absolute;
  bottom: 10px;
  right: -25px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  width: 18px;
  height: 18px;
}

#displayDiv {
  width: 80%;
  font-family: Tahoma, "Lucida Grande", Arial, Helvetica, sans-serif;
  ;
  height: 80%;
  position: absolute;
  left: 10%;
  top: 10%;
  color: black;
  background-color: white;
  padding: 20px;
  border: 5px solid #296e8f;
  overflow-y: auto;
}

.jp-Notebook-cell {
  margin-right: 30px;
}

.note-form {
  display: flex;
  flex-direction: column;
}

textarea {
  margin-bottom: 20px;
  height: 130px;
}

.reply-button {
  margin-right: 20px;
  border: none;
  background: none;
  cursor: pointer;
  color: #296e8f;
  font-weight: bold;
  padding: 0;
}

.create-note-button,
.reply-form-button {
  background-color: #296e8f;
  text-shadow: none;
  border: none;
  color: #fff;
  font-weight: 500;
  height: 30px;
  width: 100px;
  border-radius: 10px;
  cursor: pointer;
}

.buttons {
  margin-bottom: 20px;
}

.replies {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.message {
  font-size: 1em;
}

.user {
  font-weight: 700;
}

.date {
  font-size: 0.8em;
  color: #add0e1;
  margin-left: 10px;
}

.reply-form {
  display: flex;
  flex-direction: column;
}

.reply-buttons {
  margin-bottom: 15px;
}

.cancel-form-button {
  margin-left: 15px;
}

.links-in-forms {
  color: #296e8f;
  text-decoration: underline !important;
}`, "",{"version":3,"sources":["webpack://./style/collabnotes.css"],"names":[],"mappings":"AAAA;EACE,yBAAyB;AAC3B;;AAEA,gCAAgC;AAChC;EACE,kBAAkB;AACpB;;AAEA;EACE,gBAAgB;EAChB,QAAQ;EACR,SAAS;EACT,kBAAkB;EAClB,MAAM;EACN,QAAQ;EACR,mCAAmC;EACnC,qCAAqC;EACrC,6BAA6B;EAC7B,wCAAwC;AAC1C;;AAEA;EACE,kBAAkB;EAClB,YAAY;EACZ,YAAY;EACZ,aAAa;EACb,mBAAmB;EACnB,uBAAuB;EACvB,YAAY;EACZ,WAAW;EACX,YAAY;AACd;;AAEA;EACE,UAAU;EACV,kEAAkE;;EAElE,WAAW;EACX,kBAAkB;EAClB,SAAS;EACT,QAAQ;EACR,YAAY;EACZ,uBAAuB;EACvB,aAAa;EACb,yBAAyB;EACzB,gBAAgB;AAClB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,aAAa;EACb,sBAAsB;AACxB;;AAEA;EACE,mBAAmB;EACnB,aAAa;AACf;;AAEA;EACE,kBAAkB;EAClB,YAAY;EACZ,gBAAgB;EAChB,eAAe;EACf,cAAc;EACd,iBAAiB;EACjB,UAAU;AACZ;;AAEA;;EAEE,yBAAyB;EACzB,iBAAiB;EACjB,YAAY;EACZ,WAAW;EACX,gBAAgB;EAChB,YAAY;EACZ,YAAY;EACZ,mBAAmB;EACnB,eAAe;AACjB;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,mBAAmB;EACnB,aAAa;EACb,sBAAsB;AACxB;;AAEA;EACE,cAAc;AAChB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;EAChB,cAAc;EACd,iBAAiB;AACnB;;AAEA;EACE,aAAa;EACb,sBAAsB;AACxB;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,iBAAiB;AACnB;;AAEA;EACE,cAAc;EACd,qCAAqC;AACvC","sourcesContent":[".noNotes {\n  background-color: #86bffc;\n}\n\n/* Add this to your stylesheet */\n.divWithTriangle {\n  position: relative;\n}\n\n.divWithTriangle::after {\n  content: 'Notes';\n  width: 0;\n  height: 0;\n  position: absolute;\n  top: 0;\n  right: 0;\n  border-left: 20px solid transparent;\n  border-bottom: 20px solid transparent;\n  border-top: 20px solid yellow;\n  /* Adjust the color and size as needed */\n}\n\n.square {\n  position: absolute;\n  bottom: 10px;\n  right: -25px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: white;\n  width: 18px;\n  height: 18px;\n}\n\n#displayDiv {\n  width: 80%;\n  font-family: Tahoma, \"Lucida Grande\", Arial, Helvetica, sans-serif;\n  ;\n  height: 80%;\n  position: absolute;\n  left: 10%;\n  top: 10%;\n  color: black;\n  background-color: white;\n  padding: 20px;\n  border: 5px solid #296e8f;\n  overflow-y: auto;\n}\n\n.jp-Notebook-cell {\n  margin-right: 30px;\n}\n\n.note-form {\n  display: flex;\n  flex-direction: column;\n}\n\ntextarea {\n  margin-bottom: 20px;\n  height: 130px;\n}\n\n.reply-button {\n  margin-right: 20px;\n  border: none;\n  background: none;\n  cursor: pointer;\n  color: #296e8f;\n  font-weight: bold;\n  padding: 0;\n}\n\n.create-note-button,\n.reply-form-button {\n  background-color: #296e8f;\n  text-shadow: none;\n  border: none;\n  color: #fff;\n  font-weight: 500;\n  height: 30px;\n  width: 100px;\n  border-radius: 10px;\n  cursor: pointer;\n}\n\n.buttons {\n  margin-bottom: 20px;\n}\n\n.replies {\n  margin-bottom: 20px;\n  display: flex;\n  flex-direction: column;\n}\n\n.message {\n  font-size: 1em;\n}\n\n.user {\n  font-weight: 700;\n}\n\n.date {\n  font-size: 0.8em;\n  color: #add0e1;\n  margin-left: 10px;\n}\n\n.reply-form {\n  display: flex;\n  flex-direction: column;\n}\n\n.reply-buttons {\n  margin-bottom: 15px;\n}\n\n.cancel-form-button {\n  margin-left: 15px;\n}\n\n.links-in-forms {\n  color: #296e8f;\n  text-decoration: underline !important;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/collabnotes.css":
/*!*******************************!*\
  !*** ./style/collabnotes.css ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_collabnotes_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./collabnotes.css */ "./node_modules/css-loader/dist/cjs.js!./style/collabnotes.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_collabnotes_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_collabnotes_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_collabnotes_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_collabnotes_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.d4138ac1068df589f97b.js.map
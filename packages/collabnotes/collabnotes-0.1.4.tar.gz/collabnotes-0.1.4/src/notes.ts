import { Note } from './types';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getSetting } from './settings'; // Import the getSetting function from settings.ts
import { NotebookPanel } from '@jupyterlab/notebook';
import { updateUI } from './ui';

/**
 * Function to render notes recursively.
 */
export function renderNotes(note: any, level: number = 0): string {
  const addedDate = new Date(note.added);
  const ukDate = `${addedDate.getDate().toString().padStart(2, '0')}/${(addedDate.getMonth() + 1).toString().padStart(2, '0')}/${addedDate.getFullYear()} ${addedDate.getHours().toString().padStart(2, '0')}:${addedDate.getMinutes().toString().padStart(2, '0')}:${addedDate.getSeconds().toString().padStart(2, '0')}`;

  // Update the regex to include optional http/https at the beginning
  const urlRegex = /((https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+)(\.(co\.|com|org|net|gov|edu|io|us|it|uk|ca|de|fr|ru|jp|cn|info|biz|me|tv|dev|xyz|site|club|online|app|shop|blog|tech|art|news|live|store|ai|design|space|world|academy|digital|systems|solutions|pro|today|name|cloud|zone|press|network|fun|games|studio|group|global|life|love|media|ventures|partners|capital|finance|insurance|services|events|city|fund|energy|expert|care|team|express|consulting|restaurant|coffee|hospital|education|software|tools|university|security|partners|agency|ac\.uk|be))([^\s]*))/gi;

  // Replace detected URLs with anchor tags, ensuring http/https is included in display
  const parsedNoteContent = note.note.replace(urlRegex, (match: string) => {
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
  } else {
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
  note.replies.forEach((reply: any) => {
    noteHtml += renderNotes(reply, level + 1);
  });

  return noteHtml;
}

/**
 * Add event listeners to reply buttons.
 */
export function addEventListenersToReplyButtons() {
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
function handleReplyButtonClick(event: Event) {
  const noteID = (event.target as HTMLElement).getAttribute('data-note-id');
  console.log('reply to ' + noteID);

  const noteElement = (event.target as HTMLElement).closest('.note');
  if (!noteElement) {
    return
  };

  const existingForm = noteElement.querySelector('.reply-form');
  if (existingForm) {
    existingForm.remove();
  }

  const form = document.createElement('form');
  form.className = 'reply-form';

  const textarea = document.createElement('textarea');
  textarea.placeholder = 'Enter your reply';
  textarea.className = 'reply-form-textarea'
  form.appendChild(textarea);

  const buttons = document.createElement('div');
  buttons.className = 'reply-buttons';
  form.appendChild(buttons);

  const submitButton = document.createElement('button');
  submitButton.type = 'button';
  submitButton.textContent = 'Submit';
  submitButton.className = 'reply-form-button';
  submitButton.onclick = (e) => {
    handleSubmitReplyButtonClick(e)
    form.remove();
  };
  buttons.appendChild(submitButton);
  submitButton.setAttribute('data-note-id', String(noteID))
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


async function handleSubmitReplyButtonClick(event: Event) {
  const button = event.target as HTMLElement;
  const noteID = button.getAttribute('data-note-id');
  const form = button.closest('.reply-form');
  if (!form) {
    console.error('Form not found for note ID:', noteID);
    return;
  }

  // Get the content of the note
  const textarea = form.querySelector('textarea') as HTMLTextAreaElement;
  const noteContent = textarea?.value.trim();
  const displayDiv = document.getElementById('displayDiv');
  if (!noteContent) {
    alert('Please enter a note before saving.');
    return;
  }

  // Define constants similar to the second request
  const pi = getPI(); // Replace with actual logic to get PI
  const ac = getAC(); // Replace with actual logic to get Access Code
  const fn = getFilename(); // Replace with actual logic to get filename
  const cid = displayDiv?.getAttribute('data-cid') // Hard-coded as in the second request
  const rid = noteID; // Reply ID, as in the second request

  const ts = Date.now();

  // Prepare the data for the POST request using URLSearchParams for x-www-form-urlencoded
  const postData = new URLSearchParams({
    do: 'addnote',    // Action to add note
    pi: pi,           // User PI
    ac: ac,           // Access Code
    fn: fn,           // Filename
    cid: String(cid),    // Cell ID (convert to string because URLSearchParams expects strings)
    rid: String(rid),    // Reply ID (convert to string)
    content: noteContent,  // Replace noteContent with 'test' as per the second request
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
        await updateUI(getURL(), ac, pi, fn, ts, getNickname(), Number(cid), panel);
        // scroll to the reply button that added the new message
        const lastMessage = document.querySelector(`button[data-note-id="${newID}"]`) as HTMLButtonElement;
        const parentDiv = lastMessage.closest('div') as HTMLDivElement;
        parentDiv.scrollIntoView({ behavior: 'smooth' });
      } else {
        console.error('Panel is null, cannot update UI.');
        // Handle the null case appropriately (e.g., show an error or fallback UI)
      }
    } else {
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
async function handleCreateNoteButtonClick(event: Event) {
  const button = event.target as HTMLElement;
  const noteID = button.getAttribute('data-note-id');
  const form = button.closest('.note-form');
  if (!form) {
    console.error('Form not found for note ID:', noteID);
    return;
  }

  // Get the content of the note
  const textarea = form.querySelector('.note-textarea') as HTMLTextAreaElement;
  const noteContent = textarea?.value.trim();
  const displayDiv = document.getElementById('displayDiv');
  if (!noteContent) {
    alert('Please enter a note before saving.');
    return;
  }

  // Define constants similar to the second request
  const pi = getPI(); // Replace with actual logic to get PI
  const ac = getAC(); // Replace with actual logic to get Access Code
  const fn = getFilename(); // Replace with actual logic to get filename
  const cid = displayDiv?.getAttribute('data-cid') // Hard-coded as in the second request
  const rid = noteID; // Reply ID, as in the second request

  const ts = Date.now();

  // Prepare the data for the POST request using URLSearchParams for x-www-form-urlencoded
  const postData = new URLSearchParams({
    do: 'addnote',    // Action to add note
    pi: pi,           // User PI
    ac: ac,           // Access Code
    fn: fn,           // Filename
    cid: String(cid),    // Cell ID (convert to string because URLSearchParams expects strings)
    rid: String(rid),    // Reply ID (convert to string)
    content: noteContent,  // Replace noteContent with 'test' as per the second request
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
        await updateUI(getURL(), ac, pi, fn, ts, getNickname(), Number(cid), panel);
        // scroll to new message
        const displayDiv = document.querySelector('#displayDiv');
        if (displayDiv) {
          displayDiv.scroll({
            top: displayDiv.scrollHeight,
            behavior: 'smooth'
          });
        }
      } else {
        console.error('Panel is null, cannot update UI.');
        // Handle the null case appropriately (e.g., show an error or fallback UI)
      }
    } else {
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
export function createNestedNotes(notes: any): string {
  const notesMap: { [key: number]: Note & { replies: Note[] } } = {};
  notes.forEach((note: Note) => {
    notesMap[note.noteID] = { ...note, replies: [] };
  });

  let rootNote: (Note & { replies: Note[] }) | null = null;

  notes.forEach((note: Note) => {
    if (note.replyID === null) {
      rootNote = notesMap[note.noteID];
    } else {
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
let piCache: string | null = null;
let acCache: string | null = null;

/**
 * Initialize and cache the PI and AccessCode settings.
 * This function is only called once when the module is loaded.
 */
async function initializeSettings(settingsRegistry: ISettingRegistry): Promise<void> {
  try {
    piCache = await getSetting('PI', settingsRegistry);
    acCache = await getSetting('AccessCode', settingsRegistry);
  } catch (error) {
    console.error('Error initializing settings:', error);
    piCache = '';
    acCache = '';
  }
}

/**
 * Retrieve the cached PI value.
 */
export function getPI(): string {
  if (piCache === null) {
    console.warn('PI is not initialized yet.');
    return '';
  }
  return piCache;
}

/**
 * Retrieve the cached AccessCode value.
 */
export function getAC(): string {
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
export async function ensureSettingsInitialized(settingsRegistry: ISettingRegistry): Promise<void> {
  if (piCache === null || acCache === null) {
    await initializeSettings(settingsRegistry);
  }
}

// Create a variable to store the current notebook's filename (fn)
let fnCache: string | null = null;

/**
 * Set the filename (fn) in the cache.
 * This should be called whenever the notebook is changed or opened.
 */
export function setFilename(fn: string): void {
  fnCache = fn;
}

/**
 * Get the cached filename (fn).
 */
export function getFilename(): string {
  if (fnCache === null) {
    console.warn('Filename (fn) is not initialized yet.');
    return '';
  }
  return fnCache;
}

// Cache variables for URL, Nickname, and Notebook Panel
let urlCache: string | null = null;
let nickCache: string | null = null;
let panelCache: NotebookPanel | null = null;

/**
 * Set the URL in the cache.
 */
export function setURL(url: string): void {
  urlCache = url;
}

/**
 * Get the cached URL.
 */
export function getURL(): string {
  if (urlCache === null) {
    console.warn('URL is not initialized yet.');
    return '';
  }
  return urlCache;
}

/**
 * Set the Nickname in the cache.
 */
export function setNickname(nick: string): void {
  nickCache = nick;
}

/**
 * Get the cached Nickname.
 */
export function getNickname(): string {
  if (nickCache === null) {
    console.warn('Nickname is not initialized yet.');
    return '';
  }
  return nickCache;
}

/**
 * Set the NotebookPanel in the cache.
 */
export function setPanel(panel: NotebookPanel): void {
  panelCache = panel;
}

/**
 * Get the cached NotebookPanel.
 */
export function getPanel(): NotebookPanel | null {
  if (panelCache === null) {
    console.warn('Panel is not initialized yet.');
    return null;
  }
  return panelCache;
}
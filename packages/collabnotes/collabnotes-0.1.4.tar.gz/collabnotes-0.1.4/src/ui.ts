import { NotebookPanel } from '@jupyterlab/notebook';
import { createNestedNotes, addEventListenersToReplyButtons } from './notes';
import { fetchData } from './api';

/**
 * Create a note square element.
 */
export function createNoteSquare(newComments: string, totalComments: string, cid: number): HTMLDivElement {
  const noteSquare = document.createElement('div');
  noteSquare.id = `collabnotes_${cid}`;
  noteSquare.classList.add('square');

  const newCommentsNum = Number(newComments);
  const totalCommentsNum = Number(totalComments);

  if (newCommentsNum > 0) {
    // There are unread messages - red
    noteSquare.style.backgroundColor = '#c10031';
  } else if (totalCommentsNum === 0) {
    // There are 0 messages - blue
    noteSquare.style.backgroundColor = '#00b0ac';
  } else {
    // Messages are already read - green
    noteSquare.style.backgroundColor = '#a4a400';
  }

  noteSquare.textContent = totalComments;
  return noteSquare;
}

/**
 * Create a display div element.
 */
function createDisplayDiv(cid: string): HTMLDivElement {
  const displayDiv = document.createElement('div');
  displayDiv.id = 'displayDiv';
  console.log(cid)
  displayDiv?.setAttribute('data-cid', cid)
  return displayDiv;
}

/**
 * Handle note square click event.
 */
export async function handleNoteSquareClick(
  url: string,
  ac: string,
  pi: string,
  fn: string,
  ts: number,
  nick: string,
  cid: number,
  panel: NotebookPanel
) {
  const existingDisplayDiv = document.getElementById('displayDiv');
  if (existingDisplayDiv) {
    existingDisplayDiv.remove();
    return;
  }

  // update color of note counter
  const noteCounter = document.getElementById(`collabnotes_${cid}`)
  if (noteCounter !== null && noteCounter !== undefined) {
    if (parseInt(noteCounter.innerText) > 0) {
      noteCounter.style.backgroundColor = '#a4a400';
  }
    console.log('yo')
  }
  console.log('yo222')

  const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&cid=${cid}&do=getnotes`;
  const notes = await fetchData(qs);
  const displayDiv = createDisplayDiv(String(cid));
  const nestedNotes = createNestedNotes(notes);
  displayDiv.innerHTML = nestedNotes;
  panel.node.appendChild(displayDiv);


  addEventListenersToReplyButtons();

  document.addEventListener('click', handleClickOutside);
}

/**
 * Handle click outside of display div to remove it.
 */
function handleClickOutside(event: MouseEvent) {
  const displayDiv = document.getElementById('displayDiv');
  if (!displayDiv) {
    document.removeEventListener('click', handleClickOutside);
    return;
  }
  const target = event.target as HTMLElement;
  if (!displayDiv.contains(target)) {
    displayDiv.remove();
    document.removeEventListener('click', handleClickOutside);
  }
}

/**
 * Update ui.
 */
export async function updateUI(
  url: string,
  ac: string,
  pi: string,
  fn: string,
  ts: number,
  nick: string,
  cid: number,
  panel: NotebookPanel
) {
  // update the displayDiv
  const existingDisplayDiv = document.getElementById('displayDiv');
  if (existingDisplayDiv) {
    existingDisplayDiv.remove();
  }

  const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&cid=${cid}&do=getnotes`;
  const notes = await fetchData(qs);
  const displayDiv = createDisplayDiv(String(cid));
  const nestedNotes = createNestedNotes(notes);
  displayDiv.innerHTML = nestedNotes;
  panel.node.appendChild(displayDiv);

  addEventListenersToReplyButtons();
  document.addEventListener('click', handleClickOutside);

  // update the note counter button
  const noteCounter = document.getElementById(`collabnotes_${cid}`)
  const qs2 = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&do=list`;
  const data = await fetchData(qs2);
  if (noteCounter !== null && noteCounter !== undefined) {
    // Safe to use noteCounter
    noteCounter.innerText = data[cid].new
    noteCounter.style.backgroundColor = '#a4a400';
  }
}
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

import '../style/collabnotes.css';
import { checkSettings, getSetting } from './settings';
import { createNoteSquare, handleNoteSquareClick } from './ui';
import { fetchData } from './api';
import { ensureSettingsInitialized } from './notes';
import { setFilename, setURL, setNickname, setPanel } from './notes'; // Import the setters from notes.ts




/**
 * Initialization data for the collabnotes extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'collabnotes:plugin',
  description: 'A JupyterLab extension to enable collaborative note taking.',
  autoStart: true,
  requires: [INotebookTracker, ISettingRegistry],
  activate: (app: JupyterFrontEnd, notebooks: INotebookTracker, settingsRegistry: ISettingRegistry) => {
    console.log('JupyterLab extension collabnotes is activated! xx');
    app.restored.then(() => {
      checkSettings(settingsRegistry);
      ensureSettingsInitialized(settingsRegistry);
      if (notebooks.currentWidget) {
        addNotesButtons(settingsRegistry, notebooks.currentWidget);
      }
      notebooks.currentChanged.connect((sender, panel: NotebookPanel | null) => {
        if (panel) {
          addNotesButtons(settingsRegistry, panel);
        }
      });
    });
  }
};

async function addNotesButtons(settingsRegistry: ISettingRegistry, panel: NotebookPanel) {
  const url = await getSetting('URL', settingsRegistry);
  const ac = await getSetting('AccessCode', settingsRegistry);
  const pi = await getSetting('PI', settingsRegistry);
  const nick = await getSetting('NickName', settingsRegistry);

  const fn = panel.context.path.split('/').pop()!; // Assert that pop() will not return undefined // Get only the filename from the path
  console.log(fn)

  // Set the filename, URL, Nickname, and panel in the notes module so they can be accessed globally
  setFilename(fn);
  setURL(url);
  setNickname(nick);
  setPanel(panel);

  const ts = Date.now();
  const qs = `${url}?ac=${ac}&pi=${pi}&fn=${fn}&ts=${ts}&nick=${nick}&do=list`;
  const data = await fetchData(qs);

  panel.content.widgets?.forEach(cell => {
    if (cell.model.getMetadata('CID') !== undefined) {
      const cid = cell.model.getMetadata('CID');
      const newold = data[cid];
      if (newold !== undefined) {
        const newcomments = String(newold['new']);
        const totalcomments = String(newold['new'] + newold['old']);
        const noteSquare = createNoteSquare(newcomments, totalcomments, cid);
        noteSquare.onclick = () => handleNoteSquareClick(url, ac, pi, fn, ts, nick, cid, panel);
        cell.node.appendChild(noteSquare);
      } else {
        console.log('Unallowed cell: ' + cid);
      }
    }
  });
}

export default plugin;
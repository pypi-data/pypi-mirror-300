import { ISettingRegistry } from '@jupyterlab/settingregistry';

/**
 * Check an individual setting has been set.
 */
async function checkSetting(setting: string, settings: ISettingRegistry.ISettings) {
  let s = settings.get(setting).composite;
  if (s === '' || s === undefined) {
    s = prompt("Enter setting for '" + setting + "': ");
    if (s === null) { s = ''; }
    if (s === '') {
      alert('You must enter a setting for ' + setting + ' for collabnotes to work. You will be prompted every time you open a notebook.');
    } else {
      await settings.set(setting, s);
    }
  }
}

/**
 * Check all settings have been set.
 */
export async function checkSettings(settingsRegistry: ISettingRegistry) {
  try {
    const settings = await settingsRegistry.load('collabnotes:settings');
    await checkSetting('PI', settings);
    await checkSetting('NickName', settings);
    await checkSetting('AccessCode', settings);
    await checkSetting('URL', settings);
  } catch (error) {
    console.error('Error getting settings:', error);
  }
}

/**
 * Retrieve an individual setting.
 */
export async function getSetting(setting: string, settingsRegistry: ISettingRegistry): Promise<string> {
  try {
    const settings = await settingsRegistry.load('collabnotes:settings');
    const s = settings.get(setting).composite as string;
    if (s === '' || s === undefined || s === null) {
      return '';
    } else {
      return s;
    }
  } catch (error) {
    console.error('Error getting setting ' + setting + ':', error);
    return '';
  }
}
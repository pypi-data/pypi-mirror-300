// An interface for the Note
export interface Note {
  noteID: number;
  note: string;
  added: string;
  replyID: number | null;
  NickName: string;
  stub: number;
}
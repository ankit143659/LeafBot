
import { Dexie, type Table } from 'dexie';

export interface LocalUser {
  id?: number;
  name: string;
  email: string;
  password: string; 
  createdAt: Date;
}

export interface LocalSession {
  id: string;
  userId: string;
  title: string;
  createdAt: Date;
}

export interface LocalMessage {
  id: string;
  sessionId: string;
  role: 'user' | 'assistant';
  content: string;
  imageUrl?: string; 
  timestamp: Date;
}

// Fix: Use named import for Dexie to ensure proper class inheritance and recognition of inherited methods like 'version'.
export class BotanicalDB extends Dexie {
  users!: Table<LocalUser, number>;
  sessions!: Table<LocalSession, string>;
  messages!: Table<LocalMessage, string>;

  constructor() {
    super('BotanicalIntelligenceDB');
    // Fix: Inherited method 'version' is now correctly recognized from the Dexie base class after switching to named import.
    this.version(1).stores({
      users: '++id, &email',
      sessions: 'id, userId, createdAt',
      messages: 'id, sessionId, timestamp'
    });
  }
}

export const db = new BotanicalDB();

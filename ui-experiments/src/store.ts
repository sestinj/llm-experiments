import { writable } from 'svelte/store';
export let taskQueue = writable<any[]>([]);
export let logs = writable<string[]>([]);
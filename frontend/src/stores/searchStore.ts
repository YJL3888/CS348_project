import { writable } from 'svelte/store';

const searchResults = writable([]);

function setSearchResults(newResults) {
  searchResults.set(newResults);
}

export { searchResults, setSearchResults };

<script lang="ts">
	import RestaurantsList from '$lib/RestaurantsList.svelte';
	import type { PageData } from './$types';
	import { searchResults } from '../stores/searchStore';
	import { currentPage } from '../stores/paginationStore';

	export let data: PageData;

	let results = [];

	function updateResults(newResults) {
		results = newResults;
	}

	// subscribes to search results (to display h1 if no results)
	searchResults.subscribe((value) => {
		results = value;
		currentPage.set(1); // Reset to the first page on new search results
	});
</script>

{#if results.length === 0}
	<h1 class="mb-6 text-2xl font-bold text-gray-900 dark:text-gray-100">
		Welcome to GooseGooseGo! Search a restaurant to get started
	</h1>
{/if}

<div class="flex h-full w-full">
	<div class="flex-1">
		{#if results.length !== 0}
			<h1 class="mb-6 text-2xl font-bold text-gray-900 dark:text-gray-100">Search Results</h1>
		{/if}
		<RestaurantsList {results} {data} />
	</div>
</div>

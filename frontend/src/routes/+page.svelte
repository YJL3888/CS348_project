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
    searchResults.subscribe(value => {
        results = value;
        currentPage.set(1); // Reset to the first page on new search results
    });
</script>

{#if results.length === 0}
    <h1 class="text-2xl font-bold mb-6"> Welcome to GooseGooseGo! Search a restaurant to get started</h1>
{/if}

<div class="flex w-full h-full">
    <div class="flex-1">
        {#if results.length !== 0}
            <h1 class="text-2xl font-bold mb-6">Search Results</h1> 
        {/if}
        <RestaurantsList {results} {data} />
    </div>
</div>

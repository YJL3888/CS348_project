<script>
    import RestaurantsList from '$lib/RestaurantsList.svelte';
    import { searchResults } from '../stores/searchStore';

    export let data;

    let results = [];

    function updateResults(newResults) {
        results = newResults;
    }

    // subscribes to search results (to display h1 if no results)
    searchResults.subscribe(value => {
        results = value;
    });
</script>

{#if results.length === 0}
    <h1 class="text-2xl font-bold mb-6"> Welcome to GooseGooseGo! Search a restaurant to get started</h1>
{/if}

<div class="flex w-full h-full">
    <div class="w-1/6 h-full bg-gray-100">
        <!-- Saved space for filters. Althought it might go in Restaurant list -->
    </div>
    <div class="flex-1">
        {#if results.length !== 0}
            <h1 class="text-2xl font-bold mb-6">Search Results</h1> 
        {/if}
        <RestaurantsList {results} user={data.user} />
    </div>
</div>
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
    <h1>Welcome to GooseGooseGo! Search a restaurant to get started</h1>
{/if}

<RestaurantsList {results} user={data.user} />

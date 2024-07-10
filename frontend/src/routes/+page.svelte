<script>
    import SearchBar from '$lib/SearchBar.svelte';
    import RestaurantsList from '$lib/RestaurantsList.svelte';

    let searchQuery = '';
    let searchFields = ['name', 'cuisine'];
    let results = [];

    function updateResults(newResults) {
        results = newResults;
    }
</script>

<h1>Welcome to GooseGooseGo</h1>
<p>Check <a href="https://diep.io" target="_blank" rel="noreferrer">this</a> out.</p>

<SearchBar {searchQuery} {searchFields} on:results={event => updateResults(event.detail.results)} />

<RestaurantsList {results} />

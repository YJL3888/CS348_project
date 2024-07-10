<script>
    import RestaurantsList from '$lib/RestaurantsList.svelte';

    let searchQuery = '';
    let searchFields = ['name', 'cuisine'];
    let results = [];

    function updateResults(newResults) {
        results = newResults;
    }
</script>

<h1>Welcome to GooseGooseGo</h1>

<RestaurantsList {results} />

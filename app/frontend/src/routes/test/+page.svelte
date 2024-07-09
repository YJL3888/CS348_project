<script>
    let items = [];

    async function fetchItems() {
        const response = await fetch('http://localhost:5000/items');
        items = await response.json();
    }
</script>

<h1>Welcome to GooseGooseGo</h1>
<p>Check <a href="https://diep.io" target="_blank" rel="noreferrer">this</a> out.</p>
<button on:click={fetchItems}>Fetch Items</button>

{#if items.length > 0}
    <ul>
        {#each items as item}
            <li>{JSON.stringify(item)}</li>
        {/each}
    </ul>
{/if}

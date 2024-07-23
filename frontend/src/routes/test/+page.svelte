<script>
	let items = [];

	async function fetchItems() {
		const response = await fetch('http://localhost:5000/items');
		items = await response.json();
	}
</script>

<h1 class="text-gray-900 dark:text-gray-100">Welcome to GooseGooseGo</h1>
<p class="text-gray-900 dark:text-gray-100">
	Check <a
		href="https://diep.io"
		target="_blank"
		rel="noreferrer"
		class="text-blue-600 dark:text-blue-400">this</a
	> out.
</p>
<button
	on:click={fetchItems}
	class="rounded bg-blue-500 p-2 text-white dark:bg-blue-700 dark:text-gray-100">Fetch Items</button
>

{#if items.length > 0}
	<ul class="text-gray-900 dark:text-gray-100">
		{#each items as item}
			<li>{JSON.stringify(item)}</li>
		{/each}
	</ul>
{/if}

<script>
	import { createEventDispatcher } from 'svelte';
	import { Button } from 'flowbite-svelte';

	let searchQuery = '';
	let searchFields = ['name', 'cuisine'];
	let results = [];

	const dispatch = createEventDispatcher();

	async function performSearch() {
		const params = new URLSearchParams({
			query: searchQuery,
			fields: searchFields.join(',')
		});

		const response = await fetch(`http://localhost:5000/search_restaurants?${params.toString()}`);
		results = await response.json();
		dispatch('results', { results });
	}
</script>

<div class="search-bar">
	<input
		type="text"
		bind:value={searchQuery}
		placeholder="Search..."
		class="p-2 border border-gray-300 rounded"
	/>
	<div class="checkbox-group">
		<label>
			<input type="checkbox" value="name" bind:group={searchFields} checked /> Name
		</label>
		<label>
			<input type="checkbox" value="cuisine" bind:group={searchFields} checked /> Cuisine
		</label>
	</div>
	<Button
		on:click={performSearch}
		style="background-color: #4C8C2B; color: white; padding: 0.5rem 1rem; border-radius: 0.375rem;"
		>Search</Button
	>
</div>

<div class="results">
	{#if results.length > 0}
		<ul>
			{#each results as result}
				<li>
					<strong>{result[1]}</strong>
					<!-- restaurant_name -->
					<div>{result[2]}</div>
					<!-- description -->
					<div><strong>Cuisine:</strong> {result[6]}</div>
					<!-- cuisine -->
					<div><strong>Contact:</strong> {result[4]}</div>
					<!-- contact -->
					<div><strong>Address:</strong> {result[3]}</div>
					<!-- address -->
					<div>
						<strong>Website:</strong>
						<a href={result[5]} target="_blank" rel="noreferrer">{result[5]}</a>
					</div>
					<!-- website -->
					<div><strong>Rating:</strong> {result[7]}</div>
					<!-- rating -->
					<div>
						<strong>Hours:</strong>
						{Object.entries(JSON.parse(result[8]))
							.map(([day, hours]) => `${day}: ${hours}`)
							.join(', ')}
					</div>
					<!-- hours -->
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.search-bar {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.checkbox-group {
		display: flex;
		gap: 1rem;
	}

	.results ul {
		list-style-type: none;
		padding: 0;
	}

	.results li {
		margin-bottom: 1rem;
		padding: 1rem;
		border: 1px solid #ccc;
		border-radius: 0.5rem;
	}
</style>

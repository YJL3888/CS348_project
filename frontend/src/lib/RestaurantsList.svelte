<script lang="ts">
	import { onMount } from 'svelte';

	type Restaurant = {
		id: number;
		name: string;
		description: string;
		address: string;
		contact: string;
		website: string;
		type: string;
		rating: number;
		hours: { [key: string]: string };
		price_range: number;
	};

	type MenuItem = {
		name: string;
		price: number;
	};

	let restaurants: Restaurant[] = [];
	let menu: { [key: number]: MenuItem[] } = {};
	let searchQuery: string = '';
	let searchFields: string[] = ['name', 'cuisine'];

	async function fetchRestaurants(): Promise<void> {
		const response = await fetch('http://localhost:5000/restaurants');
		const data = await response.json();
		restaurants = data.map((restaurant: any) => ({
			id: restaurant[0],
			name: restaurant[1],
			description: restaurant[2],
			address: restaurant[3],
			contact: restaurant[4],
			website: restaurant[5],
			type: restaurant[6],
			price_range: restaurant[7],
			hours: JSON.parse(restaurant[8])
		}));
	}

	async function fetchMenu(restaurantId: number): Promise<void> {
		const response = await fetch(`http://localhost:5000/restaurants/${restaurantId}/menu`);
		if (!response.ok) {
			console.error(`Failed to fetch menu: ${response.statusText}`);
			return;
		}
		const data = await response.json();
		menu[restaurantId] = data;
	}

	async function toggleMenu(restaurant: Restaurant): Promise<void> {
		if (menu[restaurant.id]) {
			delete menu[restaurant.id];
		} else {
			await fetchMenu(restaurant.id);
		}
	}

	async function performSearch(): Promise<void> {
		const params = new URLSearchParams({
			query: searchQuery,
			fields: searchFields.join(',')
		});

		const response = await fetch(`http://localhost:5000/search_restaurants?${params.toString()}`);
		const data = await response.json();
		restaurants = data.map((restaurant: any) => ({
			id: restaurant[0],
			name: restaurant[1],
			description: restaurant[2],
			address: restaurant[3],
			contact: restaurant[4],
			website: restaurant[5],
			type: restaurant[6],
			price_range: restaurant[7],
			hours: JSON.parse(restaurant[8])
		}));
	}

	onMount((): void => {
		fetchRestaurants();
	});
</script>

<div class="search-bar">
	<input type="text" bind:value={searchQuery} placeholder="Search..." />
	<div>
		<label>
			<input type="checkbox" value="name" bind:group={searchFields} checked /> Name
		</label>
		<label>
			<input type="checkbox" value="cuisine" bind:group={searchFields} checked /> Cuisine
		</label>
	</div>
	<button on:click={performSearch} class="search-button bg-green-600 text-white py-2 px-4 rounded"
		>Search</button
	>
</div>

<div class="restaurant-list">
	{#each restaurants as restaurant}
		<div class="restaurant-card" on:click={() => toggleMenu(restaurant)}>
			<div class="restaurant-name">{restaurant.name}</div>
			<div class="restaurant-info">
				<div><strong>Price Range:</strong> {'$'.repeat(restaurant.price_range)}</div>
				<div><strong>Reviews:</strong> {restaurant.reviews || 'N/A'} reviews</div>
			</div>
			<div><strong>Contact Info:</strong> {restaurant.contact}</div>
			<div><strong>Address:</strong> {restaurant.address}</div>
			<div>
				<strong>Hours:</strong>
				{Object.entries(restaurant.hours)
					.map(([day, hours]) => `${day}: ${hours}`)
					.join(', ')}
			</div>

			{#if menu[restaurant.id]}
				<div class="menu">
					<div class="menu-title">Menu:</div>
					{#each menu[restaurant.id] as menuItem}
						<div class="menu-item">{menuItem.name}: {menuItem.price}</div>
					{/each}
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.restaurant-list {
		justify-content: center;
		display: flex;
		flex-wrap: wrap;
		gap: 16px;
	}

	.restaurant-card {
		border: 1px solid #ccc;
		padding: 16px;
		border-radius: 8px;
		width: 300px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.restaurant-card:hover {
		cursor: pointer;
		background-color: #f9f9f9;
	}

	.restaurant-name {
		font-size: 1.5em;
		margin-bottom: 8px;
	}

	.restaurant-info {
		display: flex;
		justify-content: space-between;
		margin-bottom: 8px;
	}

	.menu-title {
		font-size: 1.25em;
		margin-top: 16px;
		font-weight: bold;
	}

	.menu-item {
		margin-left: 16px;
	}

	.search-bar {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.search-button {
		background-color: #4c8c2b;
		color: white;
		padding: 0.5rem 1rem;
		border-radius: 0.375rem;
	}

	.checkbox-group {
		display: flex;
		gap: 1rem;
	}
</style>

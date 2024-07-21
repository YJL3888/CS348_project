<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let restaurantId: number;
	let restaurant: any;
	let menu: any[] = [];

	$: restaurantId = +$page.params.restaurant_id;

	async function fetchRestaurantDetails() {
		const response = await fetch(`http://localhost:5000/restaurants/${restaurantId}`);
		restaurant = await response.json();
	}

	async function fetchMenu() {
		const response = await fetch(`http://localhost:5000/restaurants/${restaurantId}/menu`);
		menu = await response.json();
	}

	onMount(() => {
		fetchRestaurantDetails();
		fetchMenu();
	});
</script>

<div>
	{#if restaurant}
		<h1>{restaurant.name}</h1>
		<p>{restaurant.description}</p>
		<p><strong>Address:</strong> {restaurant.address}</p>
		<p><strong>Contact:</strong> {restaurant.contact}</p>
		<p>
			<strong>Website:</strong>
			<a href={restaurant.website} target="_blank">{restaurant.website}</a>
		</p>
		<p><strong>Type:</strong> {restaurant.type}</p>
		<p><strong>Rating:</strong> {restaurant.rating}</p>
		<p>
			<strong>Hours:</strong>
			{Object.entries(restaurant.hours)
				.map(([day, hours]) => `${day}: ${hours}`)
				.join(', ')}
		</p>

		<h2>Menu</h2>
		<ul>
			{#each menu as menuItem}
				<li>{menuItem.name}: ${menuItem.price}</li>
			{/each}
		</ul>
	{/if}
</div>

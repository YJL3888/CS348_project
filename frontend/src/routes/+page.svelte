<script lang="ts">
	import RestaurantsList from '$lib/RestaurantsList.svelte';
	import type { PageData } from './$types';
	import { currentPage } from '../stores/paginationStore';
	import { onMount } from 'svelte';
	import { PUBLIC_BACKEND_BASE } from '$env/static/public';
	import { searchResults, setSearchResults } from '../stores/searchStore';
	import { get } from 'svelte/store';

	export let data: PageData;

	let results = [];
	let fresh = true;

	onMount(async () => {
		// Check if searchResults store already has data
		if (get(searchResults).length === 0) {
			let favoriteRestaurantIds = [];
			if (data.user && data.user.sub) {
				const favoritesResponse = await fetch('/api/favorites', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
				});
				favoriteRestaurantIds = await favoritesResponse.json();
			}
			const response = await fetch(`${PUBLIC_BACKEND_BASE}/recommendations`);
			const recommendations = await response.json();

			const formattedRecommendations = recommendations.map((restaurant) => ({
				id: restaurant.restaurant_id,
				name: restaurant.restaurant_name,
				description: restaurant.description,
				address: restaurant.address,
				contact: restaurant.phone_number,
				website: restaurant.website,
				type: restaurant.cuisine,
				price_range: restaurant.price_range,
				hours: JSON.parse(restaurant.hours_range),
				has_discount: restaurant.discount,
				review_count: restaurant.review_count,
				rating: restaurant.average_rating,
				favorite: favoriteRestaurantIds.includes(restaurant.restaurant_id)
			}));
			setSearchResults(formattedRecommendations);
			fresh = true;
		} else {
			// If searchResults store is not empty, set fresh to false
			fresh = false;
		}
	});

	// Subscribe to search results (to display h1 if no results)
	searchResults.subscribe((value) => {
		results = value;
		if (value.length > 0) {
			fresh = false;
		}
		currentPage.set(1); // Reset to the first page on new search results
	});
</script>

{#if fresh}
	<h1 class="mb-6 text-2xl font-bold text-gray-900 dark:text-gray-100">
		Welcome to GooseGooseGo! Search a restaurant to get started!
	</h1>
	<p class="text-gray-600 dark:text-gray-400 mb-8">
		Here are some top rated GooseGooseGo recommendations to get you started:
	</p>
{/if}

<div class="flex h-full w-full">
	<div class="flex-1">
		{#if !fresh && results.length !== 0}
			<h1 class="mb-6 text-2xl font-bold text-gray-900 dark:text-gray-100">Search Results</h1>
		{/if}
		<RestaurantsList {results} {data} />
	</div>
</div>

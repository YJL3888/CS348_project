<script lang="ts">
	import { Section, HeroHeader } from 'flowbite-svelte-blocks';
	import { Button } from 'flowbite-svelte';
	import { ArrowRightOutline, SearchOutline } from 'flowbite-svelte-icons';
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
					}
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

	// subscribes to search results (to display h1 if no results)
	searchResults.subscribe((value) => {
		results = value;
		if (value.length > 0) {
			fresh = false;
		}
		currentPage.set(1); // Reset to the first page on new search results
	});
</script>

<Section name="heroVisual" sectionClass="py-0">
	<div class="mb-8 mr-40 mr-auto place-self-center lg:col-span-7">
		<HeroHeader
			h1Class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
			pClass="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400"
		>
			<svelte:fragment slot="h1">
				Discover Your Next Favorite Meal with GooseGooseGo!
			</svelte:fragment>
			<svelte:fragment slot="paragraph">
				GooseGooseGo is your ultimate restaurant discovery app, designed to help food lovers find
				the best dining experiences nearby. Whether you're craving a cozy café, a bustling bistro,
				or a gourmet dinner, GooseGooseGo offers personalized recommendations, reviews, and menus to
				guide you to your perfect meal. Register now and embark on a culinary adventure!
			</svelte:fragment>
			{#if !data.user}
				<Button
					href="/register"
					size="xl"
					color="red"
					class="mr-3 inline-flex items-center justify-center"
				>
					Get started<ArrowRightOutline size="md" class="-mr-1 ml-2" />
				</Button>
			{/if}
			<Button
				color={data.user ? 'red' : 'light'}
				size="xl"
				class="inline-flex items-center justify-center"
				on:click={(e) => document.getElementById('nav-restaurant-search')?.focus()}
			>
				Start Your Search <SearchOutline size="md" class="-mr-1 ml-2" />
			</Button>
		</HeroHeader>
	</div>
	<div class="aspect-ratio-container relative hidden w-full lg:col-span-5 lg:mt-0 lg:flex">
		<img
			src="/images/food.jpg"
			alt="picture of food"
			class="absolute left-0 top-0 h-full w-full object-cover"
		/>
	</div>
</Section>

{#if fresh}
	<p class="mb-8 text-gray-600 dark:text-gray-400">
		Here are some top rated GooseGooseGo recommendations to get you started:
	</p>
{/if}

<div class="search-results-container flex h-full w-full">
	<div class="flex-1">
		{#if !fresh && results.length !== 0}
			<h1 class="mb-6 text-2xl font-bold text-gray-900 dark:text-gray-100">Search Results</h1>
		{/if}
		<RestaurantsList {results} {data} hidePagination={fresh} />
		{#if fresh}
			<br />
		{/if}
	</div>
</div>

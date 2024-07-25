<script lang="ts">
	import type { PageData } from './$types';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { RatingComment } from 'flowbite-svelte';
	export let data: PageData;

	let { restaurant } = data;

	function formatPrice(price: number) {
		return price.toFixed(2);
	}

	function formatReview(review) {
		return {
			id: review.review_id,
			user: {
				name: review.username,
				img: {
					src: '/images/goose.png', // Placeholder image, replace with actual user images if available
					alt: 'User profile image'
				},
				joined: new Date(review.timestamp).toLocaleString() // Placeholder, replace with actual user joined date if available
			},
			total: 5,
			rating: review.rating
			//heading: review.comments // Use comments as heading
			//address: 'N/A', // Placeholder, replace with actual user address if available
			//datetime: review.timestamp // Use review timestamp
		};
	}

	console.log(restaurant);
</script>

<div class="container mx-auto p-6">
	<!-- Restaurant Details -->
	<h1 class="mb-4 text-3xl font-bold text-gray-900 dark:text-gray-100">
		{restaurant.restaurant_name}
	</h1>
	<p class="mb-6 text-lg text-gray-700 dark:text-gray-300">{restaurant.description}</p>

	<h2 class="mb-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Menu</h2>
	<Table hoverable={true}>
		<TableHead>
			<TableHeadCell>Item Name</TableHeadCell>
			<TableHeadCell>Price</TableHeadCell>
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each restaurant.menu as item}
				<TableBodyRow>
					<TableBodyCell>{item.item_name}</TableBodyCell>
					<TableBodyCell>${formatPrice(item.Price)}</TableBodyCell>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>

	<h2 class="mb-4 mt-8 text-2xl font-semibold text-gray-900 dark:text-gray-100">Reviews</h2>
	{#if restaurant.reviews.length > 0}
		{#each restaurant.reviews as review}
			<div class="mb-8">
				<RatingComment comment={formatReview(review)}>
					<p class="mb-2 font-light text-gray-500 dark:text-gray-400">{review.comments}</p>
				</RatingComment>
			</div>
		{/each}
	{:else}
		<p class="text-gray-700 dark:text-gray-300">No reviews yet. Be the first to leave a review!</p>
	{/if}
</div>

<style>
	.container {
		max-width: 800px;
	}
</style>

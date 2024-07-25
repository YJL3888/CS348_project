<script lang="ts">
	import { Card, Rating, Badge } from 'flowbite-svelte';
	import { HeartOutline, HeartSolid } from 'flowbite-svelte-icons';
	import type { PageData } from '../routes/$types';
	export let restaurant: {
		id: number;
		name: string;
		description: string;
		address: string;
		contact: string;
		website: string;
		type: string;
		price_range: number;
		hours: { [key: string]: string };
		has_discount: boolean;
		review_count: number;
		rating: number;
		hover?: boolean;
		favorite?: boolean;
	};

	let isHovering = false;

	export let toggleFavorite: (restaurantId: number) => void;
	export let toggleMenu: (restaurant: typeof restaurant) => void;
	export let toggleHover: (restaurantId: number, isHovering: boolean) => void;
	export let data: PageData;
	console.log('WTF',restaurant.rating);
</script>

<Card href="/" horizontal size="lg" class="relative">
	{#if data?.user?.sub}
		<button
			type="button"
			class="absolute right-4 top-4"
			on:click={() => toggleFavorite(restaurant.id)}
			on:mouseenter={() => (isHovering = true)}
			on:mouseleave={() => (isHovering = false)}
			aria-label={restaurant.favorite ? 'Remove from favorites' : 'Add to favorites'}
			style="pointer-events: auto;"
		>
			{#if restaurant.favorite || isHovering}
				<HeartSolid class="text-red-500" />
			{:else}
				<HeartOutline class="text-red-500" />
			{/if}
		</button>
	{/if}
	<div style="pointer-events: none;">
		<div class="mb-2 flex items-center justify-between space-x-4">
			<h5 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
				{restaurant.name}
			</h5>
		</div>
		<Rating
			class="mb-2"
			id="example-3"
			total={5}
			rating={restaurant.rating !== null && restaurant.rating !== undefined ? restaurant.rating : 0}
		>
			<p slot="text" class="ms-2 text-sm font-medium text-black">
                {restaurant.rating ? (+restaurant.rating).toFixed(2): 'N/A'}
				<span class="text-gray-600">({restaurant.review_count} reviews)</span>
			</p>
		</Rating>
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-2">
				<Badge rounded border color="red">{Array(restaurant.price_range).fill('$').join('')}</Badge>
				<Badge rounded border>{restaurant.type}</Badge>
			</div>
		</div>
	</div>
	{#if restaurant.has_discount}
		<div class="absolute bottom-4 right-4">
			<Badge rounded border color="green">{'Discount available!'}</Badge>
		</div>
	{/if}
</Card>

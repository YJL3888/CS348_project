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
		rating: number;
		hours: { [key: string]: string };
		price_range: number;
		hover?: boolean;
		favorite?: boolean;
	};

	let isHovering = false;
    // <$: roundedRating = rating.toFixed(2)>;

	export let toggleFavorite: (restaurantId: number) => void;
	export let toggleMenu: (restaurant: typeof restaurant) => void;
	export let toggleHover: (restaurantId: number, isHovering: boolean) => void;
	export let data: PageData
</script>

<Card href="/" horizontal size="lg" class="relative">
	{#if data?.user?.sub}
	<button
		type="button"
		class="absolute top-4 right-4"
		on:click={() => toggleFavorite(restaurant.id)}
		on:mouseenter={() => isHovering = true}
		on:mouseleave={() => isHovering = false}
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
		<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{restaurant.name}</h5>
        <Rating id="example-3" total={5} rating={3.4}>
            <p slot="text" class="text-sm font-medium text-black ms-2">
                3.4 
                <span class="text-gray-600">(12 reviews)</span>
              </p>        
        </Rating>
        <div class="flex items-center space-x-2">
			<Badge color="green">{Array(restaurant.price_range).fill('$').join('')}</Badge>
			<Badge color="red">{restaurant.type}</Badge>
		</div>
	</div>
</Card>

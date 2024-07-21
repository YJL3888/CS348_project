<script lang="ts">
	import { Card, Badge, Button } from 'flowbite-svelte';
	import { StarOutline, StarSolid, ArrowRightOutline } from 'flowbite-svelte-icons';

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

	export let toggleFavorite: (restaurantId: number) => void;
	export let toggleMenu: (restaurant: typeof restaurant) => void;
	export let toggleHover: (restaurantId: number, isHovering: boolean) => void;
</script>

<Card href="/" horizontal size="lg">
	<h5 class="text-xl font-semibold mt-2">{restaurant.name}</h5>
</Card>
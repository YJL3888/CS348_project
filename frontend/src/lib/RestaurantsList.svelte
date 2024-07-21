<script lang="ts">
    import RestaurantCard from './RestaurantCard.svelte';
	import { searchResults } from '../stores/searchStore'; 

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
        hover?: boolean;
        favorite?: boolean;
    };

    type MenuItem = {
        name: string;
        price: number;
    };

    export let results: Restaurant[] = [];
    let menu: { [key: number]: MenuItem[] } = {};
    export let user; // Assuming user data is passed to this component

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

    function toggleHover(restaurantId: number, isHovering: boolean) {
        const restaurantIndex = results.findIndex((r) => r.id === restaurantId);
        if (restaurantIndex !== -1) {
            results[restaurantIndex].hover = isHovering;
        }
    }

    async function toggleFavorite(restaurantId: number) {
        try {
            const response = await fetch('http://localhost:5000/toggle_favorites', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: user?.sub, restaurant_id: restaurantId })
            });

            if (!response.ok) {
                throw new Error('Failed to toggle favorite');
            }

            // Find the restaurant in the results array and toggle its favorite status
            const restaurantIndex = results.findIndex((r) => r.id === restaurantId);
            if (restaurantIndex !== -1) {
                results[restaurantIndex].favorite = !results[restaurantIndex].favorite;
            }

            console.log(`Toggled favorite for restaurant: ${restaurantId}, User ID: ${user?.sub}`);
        } catch (error) {
            console.error('Error toggling favorite:', error);
        }
    }
	searchResults.subscribe(value => {
        results = value;
    });
</script>

<style>
	.restaurant-list {
		display: flex;
		flex-direction: column;
		gap: 16px; /* Adjust this value to set the padding between cards */
	}
</style>

<div class="restaurant-list">
	{#each results as restaurant}
		<RestaurantCard {restaurant} {toggleFavorite} {toggleMenu} {toggleHover} />
	{/each}
</div>

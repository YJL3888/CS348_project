<script lang="ts">
    import { StarOutline, StarSolid } from 'flowbite-svelte-icons';
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

<div class="restaurant-list">
    {#each results as restaurant}
        <div class="restaurant-card" on:click={() => toggleMenu(restaurant)}>
            <div class="restaurant-name">
                {restaurant.name}
                {#if user}
                    <!-- Show favorite button only if user is logged in -->
                    <button
                        on:click|stopPropagation={() => toggleFavorite(restaurant.id)}
                        on:mouseenter={() => toggleHover(restaurant.id, true)}
                        on:mouseleave={() => toggleHover(restaurant.id, false)}
                    >
                        {#if restaurant.hover || restaurant.favorite}
                            <StarSolid color="yellow" />
                        {:else}
                            <StarOutline strokeWidth="2" />
                        {/if}
                    </button>
                {/if}
            </div>
            <div class="restaurant-info">
                <div><strong>Price Range:</strong> {'$'.repeat(restaurant.price_range)}</div>
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
	.checkbox-group {

		display: flex;
		gap: 1rem;
	}
	.restaurant-name {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
</style>

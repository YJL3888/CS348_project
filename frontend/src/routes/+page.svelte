<script>
    import { onMount } from 'svelte';

    let restaurants = [];

    async function fetchRestaurants() {
        const response = await fetch('http://localhost:5000/restaurants');
        const data = await response.json();
        restaurants = data.map(restaurant => ({
            id: restaurant[0],
            name: restaurant[1],
            description: restaurant[2],
            address: restaurant[3],
            contact: restaurant[4],
            website: restaurant[5],
            type: restaurant[6],
            rating: restaurant[7],
            hours: JSON.parse(restaurant[8])
        }));
    }

    async function fetchItems() {
        const response = await fetch('http://localhost:5000/items');
        items = await response.json();
    }

    onMount(() => {
        fetchRestaurants();
    });
</script>

<style>
    .restaurant-list {
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

    .restaurant-name {
        font-size: 1.5em;
        margin-bottom: 8px;
    }

    .restaurant-info {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
</style>

<h1>Welcome to GooseGooseGo</h1>
<p>Check <a href="https://diep.io" target="_blank" rel="noreferrer">this</a> out.</p>

<div class="restaurant-list">
    {#each restaurants as restaurant}
        <div class="restaurant-card">
            <div class="restaurant-name">{restaurant.name}</div>
            <div class="restaurant-info">
                <div><strong>Rating:</strong> {restaurant.rating} ⭐</div>
                <div><strong>Reviews:</strong> {restaurant.reviews || 'N/A'} reviews</div>
            </div>
            <div><strong>Contact Info:</strong> {restaurant.contact}</div>
            <div><strong>Address:</strong> {restaurant.address}</div>
            <div><strong>Hours:</strong> {Object.entries(restaurant.hours).map(([day, hours]) => `${day}: ${hours}`).join(', ')}</div>
        </div>
    {/each}
</div>

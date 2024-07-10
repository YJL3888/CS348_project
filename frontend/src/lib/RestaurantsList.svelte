<script>
  import { onMount } from 'svelte';
  import Modal from './Modal.svelte';

  let restaurants = [];
  let selectedRestaurant = null;
  let menu = [];
  let isModalOpen = false;

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

  async function fetchMenu(restaurantId) {
    const response = await fetch(`http://localhost:5000/restaurants/${restaurantId}/menu`);
    if (!response.ok) {
      console.error(`Failed to fetch menu: ${response.statusText}`);
      return [];
    }
    return response.json();
  }

  async function showMenu(restaurant) {
    selectedRestaurant = restaurant;
    menu = await fetchMenu(restaurant.id);
    isModalOpen = true;
  }

  function closeModal() {
    isModalOpen = false;
    selectedRestaurant = null;
    menu = [];
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
</style>

<div class="restaurant-list">
  {#each restaurants as restaurant}
    <div class="restaurant-card" on:click={() => showMenu(restaurant)}>
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

<Modal isOpen={isModalOpen} closeModal={closeModal}>
  <h2>{selectedRestaurant ? selectedRestaurant.name : ''}</h2>
  <ul>
    {#each menu as menuItem}
      <li>{menuItem.name}: {menuItem.price}</li>
    {/each}
  </ul>
</Modal>

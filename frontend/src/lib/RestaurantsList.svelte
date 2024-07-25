<script lang="ts">
    import RestaurantCard from './RestaurantCard.svelte';
    import { searchResults } from '../stores/searchStore';
    import { currentPage } from '../stores/paginationStore';
    import { PaginationItem } from 'flowbite-svelte';
    import { ArrowLeftOutline, ArrowRightOutline } from 'flowbite-svelte-icons';
    import { writable } from 'svelte/store';
    import { PUBLIC_BACKEND_BASE } from '$env/static/public';

	type Restaurant = {
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

	type MenuItem = {
		name: string;
		price: number;
	};

	export let results: Restaurant[] = [];
	let menu = writable<{ [key: number]: MenuItem[] }>({});
	export let data: PageData; // Assuming user data is passed to this component

    async function fetchMenu(restaurantId: number): Promise<void> {
        const response = await fetch(PUBLIC_BACKEND_BASE + `/restaurants/${restaurantId}/menu`);
        if (!response.ok) {
            console.error(`Failed to fetch menu: ${response.statusText}`);
            return;
        }
        const newData = await response.json();
        menu.update(currentMenu => {
            currentMenu[restaurantId] = newData;
            return currentMenu;
        });
    }

    async function toggleMenu(restaurant: Restaurant): Promise<void> {
        menu.update(currentMenu => {
            if (currentMenu[restaurant.id]) {
                const { [restaurant.id]: _, ...rest } = currentMenu;
                return rest;
            } else {
                return currentMenu;
            }
        });

        if (!(await $menu)[restaurant.id]) {
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
            const response = await fetch('/api/favorites/toggle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ restaurant_id: restaurantId })
            });

			if (!response.ok) {
				throw new Error('Failed to toggle favorite');
			}

			// Find the restaurant in the results array and toggle its favorite status
			const restaurantIndex = results.findIndex((r) => r.id === restaurantId);
			if (restaurantIndex !== -1) {
				results[restaurantIndex].favorite = !results[restaurantIndex].favorite;
			}
			console.log(`Toggled favorite for restaurant: ${restaurantId}, User ID: ${data?.user?.sub}`);
		} catch (error) {
			console.error('Error toggling favorite:', error);
		}
	}

	searchResults.subscribe((value) => {
		results = value;
	});

    // Pagination logic
    let itemsPerPage = 10;
    let totalPages = 0;
    $: totalPages = Math.ceil(results.length / itemsPerPage);

    let paginatedResults = [];
    $: {
        const start = ($currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        paginatedResults = results.slice(start, end);
    }

	function setPage(page: number) {
		currentPage.set(page);
	}

	function previousPage() {
		if ($currentPage > 1) {
			setPage($currentPage - 1);
		}
	}

    function nextPage() {
        if ($currentPage < totalPages) {
            setPage($currentPage + 1);
        }
    }
</script>

{#if results.length > 0}
	<div class="restaurant-list">
		{#each $paginatedResults as restaurant}
			<RestaurantCard {restaurant} {toggleFavorite} {toggleMenu} {toggleHover} {data} />
		{/each}
	</div>

	<!-- Pagination Controls -->
	<div class="pagination-controls mb-10 mt-10">
		<PaginationItem
			pill
			class="mr-20 flex items-center"
			on:click={previousPage}
			disabled={$currentPage === 1}
		>
			<ArrowLeftOutline class="me-2 h-3.5 w-3.5" />
			Previous
		</PaginationItem>
		<PaginationItem
			pill
			class="flex items-center"
			on:click={nextPage}
			disabled={$currentPage === $totalPages}
		>
			Next
			<ArrowRightOutline class="ms-2 h-3.5 w-3.5" />
		</PaginationItem>
	</div>
{/if}



{#if results.length > 0}
    <div class="restaurant-list">
        {#each paginatedResults as restaurant}
            <RestaurantCard {restaurant} {toggleFavorite} {toggleMenu} {toggleHover} {data}/>
        {/each}
    </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls mt-10 mb-10">
        <PaginationItem pill class="flex items-center mr-20" on:click={previousPage} disabled={$currentPage === 1}>
            <ArrowLeftOutline class="me-2 w-3.5 h-3.5" />
            Previous
        </PaginationItem>
        <PaginationItem pill class="flex items-center" on:click={nextPage} disabled={$currentPage === totalPages}>
            Next
            <ArrowRightOutline class="ms-2 w-3.5 h-3.5" />
        </PaginationItem>
    </div>
{/if}

<style>
	.restaurant-list {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
	}

	.pagination-controls {
		display: flex;
		justify-content: space-around;
		margin-top: 20px;
	}
</style>

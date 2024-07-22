<script lang="ts">
    import type { LayoutData } from './$types';
    import '../app.css';
    import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button, Avatar, Dropdown, DropdownHeader, DropdownItem, DropdownDivider, Checkbox } from 'flowbite-svelte';
    import { Search, Button as SearchButton, Dropdown as SearchDropdown, DropdownItem as SearchDropdownItem } from 'flowbite-svelte';
    import { SearchOutline, ChevronDownOutline } from 'flowbite-svelte-icons';
    import { createEventDispatcher } from 'svelte';
	import { searchResults, setSearchResults } from '../stores/searchStore';

    export let data: LayoutData;

    const items = [
        { label: 'All categories' },
        { label: 'Name' },
        { label: 'Cuisine' }
    ];

    let selectCategory = 'All categories';
    let searchQuery = '';
    let showFavourites = false;  // Variable to store the state of the checkbox

    const dispatch = createEventDispatcher();

    async function handleSearch() {
		console.log("max handleSearch triggered");
        const searchFields = selectCategory === 'All categories' ? ['name', 'cuisine'] : [selectCategory.toLowerCase()];
        const params = new URLSearchParams({
            query: searchQuery,
            fields: searchFields.join(',')
        });

        let favoriteRestaurantIds = [];
        if (data.user && data.user.sub) {
            const favoritesResponse = await fetch(`http://localhost:5000/favorites?user_id=${data.user.sub}`);
            favoriteRestaurantIds = await favoritesResponse.json();
        }

        const response = await fetch(`http://localhost:5000/search_restaurants?${params.toString()}`);
        const resultData = await response.json();
        const searchResults = resultData.map((restaurant) => ({
            id: restaurant[0],
            name: restaurant[1],
            description: restaurant[2],
            address: restaurant[3],
            contact: restaurant[4],
            website: restaurant[5],
            type: restaurant[6],
            price_range: restaurant[9],
            hours: JSON.parse(restaurant[8]),
            favorite: favoriteRestaurantIds.includes(restaurant[0]) // Set favorite status
        }));

        // Filter by favourites if the checkbox is checked
        const filteredResults = showFavourites
            ? searchResults.filter(restaurant => restaurant.favorite)
            : searchResults;

		console.log("max search results:", filteredResults);

		setSearchResults(filteredResults); // Update the store with filtered results
    }
</script>

<!-- Header -->
<Navbar rounded color="form">
    <NavBrand href="/">
        <img
            src="https://i.imgur.com/u7ESt9S.png"
            class="h-16 w-16 rounded-full ml-2 mr-2"
            alt="Logo"
        />
        <span class="text-[#4C8C2B] text-xl font-semibold font-sans">GooseGooseGo</span>
    </NavBrand>
    <!-- Search Bar -->
    <form class="flex w-2/5 justify-start mr-6">
        <div class="relative">
            <SearchButton pill class="rounded-e-none whitespace-nowrap border border-e-0 bg-[#4C8C2B]">
                {selectCategory}
                <ChevronDownOutline class="w-2.5 h-2.5 ms-2.5" />
            </SearchButton>
            <SearchDropdown classContainer="w-40">
                {#each items as { label }}
                    <SearchDropdownItem
                        on:click={() => {
                            selectCategory = label;
                        }}
                        class={selectCategory === label ? 'underline' : ''}
                    >
                        {label}
                    </SearchDropdownItem>
                {/each}
            </SearchDropdown>
        </div>
        <Search bind:value={searchQuery} size="md" class="rounded-none py-2.5 flex-grow" placeholder="Search by Name, Cuisine..." />
        <SearchButton pill style="height: 42px" class="!p-2.5 rounded-s-none bg-[#4C8C2B] text-white" on:click={handleSearch}>
            <SearchOutline class="w-6 h-6" />
        </SearchButton>
        <!-- Add Checkbox for Favourites -->
        <div class="flex items-center ml-2">
            <Checkbox id="favourites-checkbox" bind:checked={showFavourites} />
            <label for="favourites-checkbox" class="ml-1 text-sm text-gray-700">Favourites</label>
        </div>
    </form>
    <div class="flex md:order-2">
        {#if data.user}
            <Avatar id="user-drop" class="cursor-pointer" dot={{ color: 'green' }} />
            <Dropdown triggeredBy="#user-drop">
            <DropdownHeader>
                <span class="block text-sm">{data.user.username}</span>
                <span class="block truncate text-sm font-medium">{data.user.email}</span>
            </DropdownHeader>
            <DropdownDivider />
            <DropdownItem href="/logout">Log out</DropdownItem>
            </Dropdown>
        {:else}
            <Button pill
                size="sm"
                class="bg-[#4C8C2B] text-white py-2 px-4 mr-4"
                href="/login"
            >
                Log In
            </Button>
            <Button pill
                size="sm"
                class="bg-[#4C8C2B] text-white py-2 px-4 mr-6"
                href="/register"
            >
                Sign Up
            </Button>
        {/if}
        <NavHamburger />
    </div>
    <NavUl>
        <NavLi href="/" class="mr-4">Home</NavLi>
        <NavLi href="/about" class="mr-4">About</NavLi>
        <NavLi href="/contact-us" class="mr-4">Contact Us</NavLi>
    </NavUl>
</Navbar>
<div class="mx-48">
    <br />
    <slot></slot>
</div>

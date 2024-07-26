<script lang="ts">
	import type { LayoutData } from './$types';
	import '../app.css';
	import {
		Navbar,
		NavBrand,
		NavLi,
		NavUl,
		NavHamburger,
		Button,
		Avatar,
		Dropdown,
		DropdownHeader,
		DropdownItem,
		Checkbox,
		DarkMode,
		P
	} from 'flowbite-svelte';
	import {
		Search,
		Button as SearchButton,
		Dropdown as SearchDropdown,
		DropdownItem as SearchDropdownItem
	} from 'flowbite-svelte';
	import { SearchOutline, ChevronDownOutline } from 'flowbite-svelte-icons';
	import { createEventDispatcher } from 'svelte';
	import { searchResults, setSearchResults } from '../stores/searchStore';
	import {
		Footer,
		FooterCopyright,
		FooterLinkGroup,
		FooterBrand,
		FooterLink
	} from 'flowbite-svelte';
	import { goto } from '$app/navigation';

	export let data: LayoutData;

	const items = [{ label: 'All categories' }, { label: 'Name' }, { label: 'Cuisine' }];

	let selectCategory = 'All categories';
	let searchQuery = '';
	let showFavourites = false; // Variable to store the state of the checkbox

	const dispatch = createEventDispatcher();

	async function handleSearch() {
		const searchFields =
			selectCategory === 'All categories' ? ['name', 'cuisine'] : [selectCategory.toLowerCase()];
		const params = new URLSearchParams({
			query: searchQuery,
			fields: searchFields.join(',')
		});

		let favoriteRestaurantIds = [];
		if (data.user && data.user.sub) {
			const favoritesResponse = await fetch('/api/favorites', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});
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
			price_range: restaurant[7],
			hours: JSON.parse(restaurant[8]),
			has_discount: restaurant[9],
			review_count: restaurant[10],
			rating: restaurant[11],
			favorite: favoriteRestaurantIds.includes(restaurant[0]) // Set favorite status
		}));

		// Filter by favourites if the checkbox is checked
		const filteredResults = showFavourites
			? searchResults.filter((restaurant) => restaurant.favorite)
			: searchResults;

		setSearchResults(filteredResults); // Update the store with filtered results

		goto('/').then(() => {
			const searchResultsContainer = document.querySelector<HTMLElement>(
				'.search-results-container'
			);
			if (searchResultsContainer)
				window.scrollTo(
					0,
					searchResultsContainer.offsetTop - document.getElementById('top-nav')!.offsetHeight - 20
				);
		});
	}

	function reloadPage() {
		goto('/').then(() => {
			window.location.reload();
		});
	}
</script>

<!-- Header -->
<Navbar
	rounded
	color="form"
	class="sticky start-0 top-0 z-20 w-full px-2 py-2.5 sm:px-4"
	id="top-nav"
>
	<NavBrand href="/" on:click={reloadPage}>
		<img
			src="https://i.imgur.com/u7ESt9S.png"
			class="ml-2 mr-2 h-16 w-16 rounded-full"
			alt="Logo"
		/>
		<P class="font-sans text-xl font-semibold text-[#4C8C2B]">GooseGooseGo</P>
	</NavBrand>
	<!-- Search Bar -->
	<form class="mr-6 flex w-2/5 justify-start" on:submit|preventDefault={handleSearch}>
		<div class="relative">
			<SearchButton pill class="whitespace-nowrap rounded-e-none border border-e-0 bg-[#4C8C2B]">
				{selectCategory}
				<ChevronDownOutline class="ms-2.5 h-2.5 w-2.5" />
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
		<Search
			bind:value={searchQuery}
			size="md"
			class="flex-grow rounded-none py-2.5"
			placeholder="Search by Name, Cuisine..."
			id="nav-restaurant-search"
		/>
		<SearchButton
			pill
			style="height: 42px"
			class="rounded-s-none bg-[#4C8C2B] !p-2.5 text-white"
			type="submit"
		>
			<SearchOutline class="h-6 w-6" />
		</SearchButton>
		<!-- Add Checkbox for Favourites -->
		<div class="ml-2 flex items-center">
			<Checkbox id="favourites-checkbox" bind:checked={showFavourites} />
			<P for="favourites-checkbox" class="ml-1 text-sm text-gray-700">Favourites</P>
		</div>
	</form>
	<div class="flex md:order-2">
		{#if data.user}
			<Avatar
				id="user-drop"
				class="cursor-pointer"
				src="/images/goose.png"
				dot={{ color: 'green' }}
			/>
			<Dropdown triggeredBy="#user-drop">
				<DropdownHeader>
					<span class="block text-sm">{data.user.username}</span>
					<span class="block truncate text-sm font-medium">{data.user.email}</span>
				</DropdownHeader>
				<DropdownItem href="/logout">Log out</DropdownItem>
			</Dropdown>
		{:else}
			<Button pill size="sm" class="mr-4 bg-[#4C8C2B] px-4 py-2 text-white" href="/login">
				Log In
			</Button>
			<Button pill size="sm" class="mr-6 bg-[#4C8C2B] px-4 py-2 text-white" href="/register">
				Sign Up
			</Button>
		{/if}
		<!-- Add Dark Mode Toggle Here -->
		<DarkMode />
		<NavHamburger />
	</div>
	<NavUl>
		<NavLi href="/" class="mr-4" on:click={reloadPage}>Home</NavLi>
		<NavLi href="/about" class="mr-4">About</NavLi>
		<NavLi href="/contact-us" class="mr-4">Contact Us</NavLi>
	</NavUl>
</Navbar>
<div class="mx-48">
	<br />
	<slot></slot>
</div>

<!-- Footer -->
<footer class="mt-auto flex items-center justify-center bg-gray-100 py-4 dark:bg-gray-800">
	<Footer>
		<div class="flex items-center justify-center">
			<p class="text-sm text-gray-500 dark:text-gray-400">© 2024 GooseGooseGuys.</p>
			<FooterLinkGroup
				ulClass="flex flex-wrap items-center ml-2 mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0 underline"
			>
				<FooterLink href="https://github.com/YJL3888/GooseGooseGo_CS348"
					>See Our Source Code</FooterLink
				>
			</FooterLinkGroup>
		</div>
	</Footer>
</footer>

<style lang="postcss">
	:global(body) {
		@apply flex min-h-screen flex-col bg-white dark:bg-gray-900;
	}

	:global(#app) {
		@apply flex min-h-screen flex-col;
	}

	:global(main) {
		@apply flex flex-grow flex-col;
	}
</style>

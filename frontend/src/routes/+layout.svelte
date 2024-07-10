<script lang="ts">
	import type { LayoutData } from './$types';
	import '../app.css';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button, Avatar, Dropdown, DropdownHeader, DropdownItem, DropdownDivider } from 'flowbite-svelte';

	export let data: LayoutData;
</script>

<!-- Header -->
<Navbar>
	<NavBrand href="/">
		<img
			src="https://i.imgur.com/u7ESt9S.png"
			style="margin-right: 1rem; height: 36px;"
			alt="Logo"
		/>
		<span style="color: #4C8C2B; font-size: 1.25rem; font-weight: bold;"> GooseGooseGo </span>
	</NavBrand>
	<div class="flex md:order-2">
		{#if data.user}
			<Avatar id="user-drop" class="cursor-pointer" dot={{ color: 'green' }} />
			<Dropdown triggeredBy="#user-drop">
			<DropdownHeader>
				<span class="block text-sm">{data.user.username}</span>
				<span class="block truncate text-sm font-medium">{data.user.email}</span>
			</DropdownHeader>
			<DropdownDivider />
			<DropdownItem>Sign out</DropdownItem>
			</Dropdown>
		{:else}
			<Button
				size="sm"
				style="background-color: #4C8C2B; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem;"
				href="/register"
			>
				Get started
			</Button>
		{/if}
		<NavHamburger />
	</div>
	<NavUl>
		<NavLi href="/" style="color: #4C8C2B; margin-right: 1rem;">Home</NavLi>
		<NavLi href="/about" style="color: #4C8C2B; margin-right: 1rem;">About</NavLi>
		<NavLi href="/contact-us" style="color: #4C8C2B; margin-right: 1rem;">Contact Us</NavLi>
	</NavUl>
</Navbar>
<div style="margin-left: 12rem; margin-right: 12rem;">
	<br />
	<slot></slot>
</div>

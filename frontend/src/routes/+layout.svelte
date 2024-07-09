<script>
	import '../app.css';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button } from 'flowbite-svelte';
</script>

<!-- Header -->
<Navbar color="form">
	<NavBrand href="/">
		<img src="https://via.placeholder.com/50" class="me-3 h-6 sm:h-9" alt="Logo" /> <!-- Put logo here -->
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			GooseGooseGo
		</span>
	</NavBrand>
	<div class="flex md:order-2">
		<Button size="sm">Get started</Button>
		<NavHamburger />
	</div>
	<NavUl>
		<!-- Other nav links -->
		<NavLi href="/">Home</NavLi>
		<NavLi href="/about">About</NavLi>
		<NavLi href="/contact-us">Contact Us</NavLi>
	</NavUl>
</Navbar>
<slot></slot>

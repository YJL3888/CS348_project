<script>
	import '../app.css';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Button } from 'flowbite-svelte';
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
		<Button
			size="sm"
			style="background-color: #4C8C2B; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem;"
		>
			Get started
		</Button>
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

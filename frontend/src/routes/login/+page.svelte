<script lang="ts">
	import { Section, Register } from 'flowbite-svelte-blocks';
	import { Button, Checkbox, Label, Input, DarkMode } from 'flowbite-svelte';
</script>

<div class="bg-white dark:bg-gray-900">
	<Section name="login">
		<Register>
			<div class="space-y-4 rounded-md bg-white p-6 shadow-md sm:p-8 md:space-y-6 dark:bg-gray-800">
				<form class="flex flex-col space-y-6" method="POST">
					<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Login</h3>
					<Label class="space-y-2">
						<span>Email:</span>
						<Input type="email" name="email" placeholder="name@company.com" required />
					</Label>
					<Label class="space-y-2">
						<span>Password:</span>
						<Input type="password" name="password" placeholder="••••••••" required />
					</Label>
					<div class="flex items-start">
						<Checkbox>Remember me</Checkbox>
						<a
							href="/password-reset"
							class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500"
						>
							Forgot password?
						</a>
					</div>
					<Button type="submit" class="w-full">Sign in</Button>
					<p class="text-sm font-light text-gray-500 dark:text-gray-400">
						Don't have an account yet?
						<a
							href="/register"
							class="text-primary-600 dark:text-primary-500 font-medium hover:underline"
						>
							Register!
						</a>
					</p>
				</form>
			</div>
		</Register>
	</Section>
</div>

<style>
	:global(body) {
		@apply min-h-screen bg-white dark:bg-gray-900;
	}
</style>

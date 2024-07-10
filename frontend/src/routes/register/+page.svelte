<script lang="ts">
	import { Section, Register } from 'flowbite-svelte-blocks';
	import { Button, Checkbox, Label, Input } from 'flowbite-svelte';
</script>

<Section name="register">
	<Register>
		<div class="space-y-4 p-6 sm:p-8 md:space-y-6">
			<form class="flex flex-col space-y-6" method="POST">
				<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Register</h3>
				<Label class="space-y-2">
					<span>Username:</span>
					<Input type="text" name="username" placeholder="a named tank" required />
				</Label>
				<Label class="space-y-2">
					<span>Email:</span>
					<Input type="email" name="email" placeholder="name@company.com" required />
				</Label>
				<Label class="space-y-2">
					<span>Password:</span>
					<Input type="password" name="password" placeholder="••••••••" required />
				</Label>
				<div class="flex items-start">
					<Checkbox
						>I accept the&nbsp;
						<a
							class="text-primary-600 dark:text-primary-500 font-medium hover:underline"
							href="/terms"
						>
							Terms and Conditions</a
						></Checkbox
					>
				</div>
				<Button type="submit" class="w-full1">Create Account</Button>
				<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
					Already have an account? <a
						href="/login"
						class="text-primary-600 dark:text-primary-500 font-medium hover:underline">Login here</a
					>.
				</div>
			</form>
		</div>
	</Register>
</Section>

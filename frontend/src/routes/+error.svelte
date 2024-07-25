<script lang="ts">
	import { page } from '$app/stores';
	import { Section, Page404 } from 'flowbite-svelte-blocks';
	import { Button } from 'flowbite-svelte';
</script>

{#if $page.status == 404}
	<Section name="page404">
		<Page404>
			<svelte:fragment slot="h1">404</svelte:fragment>
			<svelte:fragment slot="paragraph">
				<p class="mb-4 text-3xl font-bold tracking-tight text-gray-900 md:text-4xl dark:text-white">
					Something's missing.
				</p>
				<p class="mb-4 text-lg font-light text-gray-500 dark:text-gray-400">
					Sorry, we can't find that page. You'll find lots to explore on the home page.
				</p>
				<Button href="/" size="lg" color="red">Back to Homepage</Button>
			</svelte:fragment>
		</Page404>
	</Section>
{:else}
	<h1>{$page.status}: {$page.error.message}</h1>
{/if}

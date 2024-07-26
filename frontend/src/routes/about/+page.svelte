<script>
	import { A } from 'flowbite-svelte';
	import { Section, Faq, FaqItem } from 'flowbite-svelte-blocks';
	import { HeartSolid } from 'flowbite-svelte-icons';
</script>

<p class="about-text">
	GooseGooseGo is an application designed to enhance the dining experience for students and food
	enthusiasts at Waterloo. It uses a custom dataset collected primarily from restaurants near campus
	(either scraped from the web or inputted manually) to track their menus, prices, and discounts to
	create the best application experience for users.
</p>
<br />
<p class="about-text">
	For example, they would be able to see that Gol’s Noodles has a 15% storewide discount every
	Tuesday which is information that is typically quite hard to access. Users can also view detailed
	information about restaurant items and leave reviews to rate their dining experiences to help
	others users when choosing their next gastronomic experience.
</p>
<br />
<p class="about-text">
	The application also provides personalized recommendations and generates reports on popular
	restaurants based on the users’ reviews and history on them. The development team (GooseGooseGuys)
	serves as the administrators, ensuring data integrity and performing necessary updates.
</p>

<Section name="faq" sectionClass="py-0 [&>div]:py-8">
	<h2 class="mb-8 text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">
		Frequently asked questions
	</h2>
	<Faq>
		<div>
			<FaqItem>
				<svelte:fragment slot="h3">What is GooseGooseGo?</svelte:fragment>
				<p class="text-gray-500 dark:text-gray-400">
					GooseGooseGo is a restaurant discovery app that helps users find the best dining
					experiences near them. It provides personalized recommendations, reviews, menus, and more
					to make choosing a restaurant easy and enjoyable.
				</p>
			</FaqItem>
			<FaqItem>
				<svelte:fragment slot="h3">How do I leave a review on GooseGooseGo?</svelte:fragment>
				<p class="text-gray-500 dark:text-gray-400">
					You must be logged in to leave a review. After visiting a restaurant, you can leave a
					review by navigating to the restaurant's page in the site and clicking the "Write a
					Review!" button. Share your dining experience to help other users make informed decisions.
				</p>
			</FaqItem>
			<FaqItem>
				<svelte:fragment slot="h3"
					>How does GooseGooseGo ensure the accuracy of its information?</svelte:fragment
				>
				<p class="text-gray-500 dark:text-gray-400">
					GooseGooseGo regularly updates its database with information directly from restaurants and
					user feedback. However, we are not liable for ensuring the most current information.
				</p>
			</FaqItem>
		</div>
		<div>
			<FaqItem>
				<svelte:fragment slot="h3">Is GooseGooseGo free to use?</svelte:fragment>
				<p class="text-gray-500 dark:text-gray-400">
					Yes, GooseGooseGo is free to use and always will be. We believe that everyone should have
					access to the best dining experiences (in Waterloo), and we want to make it as easy as
					possible for you to find them. Simply <A href="/register">register</A> to get access to all
					features.
				</p>
			</FaqItem>
			<FaqItem>
				<svelte:fragment slot="h3"
					>What if I have a problem with a restaurant I found?</svelte:fragment
				>
				<p class="text-gray-500 dark:text-gray-400">
					If you encounter any issues with a restaurant, please contact the restaurant directly. For
					feedback about the app or its recommendations, you can reach out to GooseGooseGo's support
					team through the <A href="/contact-us">Contact Us page</A>.
				</p>
			</FaqItem>
			<FaqItem>
				<svelte:fragment slot="h3"
					>Can I save my favorite restaurants on GooseGooseGo?</svelte:fragment
				>
				<p class="text-gray-500 dark:text-gray-400">
					Yes, you can save your favorite restaurants to your profile for easy access later. Just
					click the heart <HeartSolid
						class="inline-block align-text-bottom text-red-500"
						size="md"
					/> button on any restaurant card.
				</p>
			</FaqItem>
		</div>
	</Faq>
</Section>

<style>
	.about-text {
		@apply text-gray-900 dark:text-gray-100;
	}
</style>
